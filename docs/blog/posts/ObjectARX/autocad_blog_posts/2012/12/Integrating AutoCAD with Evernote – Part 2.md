---
title: "Integrating AutoCAD with Evernote – Part 2"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plugin
description: "In Part 1, I created a plug-in that accessed my own Evernote account using my developer token. Now its time to add OAuth authentication, so other u..."
author: Autodesk
---
# Integrating AutoCAD with Evernote – Part 2

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/integrating-autocad-with-evernote-part-2.html

## 文章内容

By Stephen Preston
In Part 1, I created a plug-in that accessed my own Evernote account using my developer token. Now its time to add OAuth authentication, so other users can use it with their own Evernote accounts.
OAuth comes in three flavors – 1.0, 1.0a and 2.0. Evernote uses OAuth 1.0a, as do the majority of web service providers at the moment. OAuth 2.0 is still in ‘internet draft’ mode. OAuth allows the user of my AutoCAD plug-in to grant my plug-in access to their Evernote account without having to enter their username and password into the plug-in (where it could be misused). Instead, they sign into their Evernote account and are asked by the Evernote server to grant access to my plug-in.
The general workflow for OAuth authentication is well documented with this example, so I’ll just quickly summarize the steps here:
When I registered my plug-in with Evernote, they gave me two keys – my consumer key and my consumer secret key.
My plug-in uses those keys to request temporary credentials from the Evernote server.
My plug-in sends the user to the Evernote website, passing the temporary credentials and a callback address. The user logs in and clicks a button to grant permission to my plug-in to access their account.
When permission is granted by the user, Evernote sends my plug-in an authorization token (via the callback address I provided) that it can use to access the user’s account for up to one year.
The URLs and parameters you create during the OAuth process are quite straightforward, but they can be difficult to debug when things go wrong. Therefore most people make use of one of the many open source OAuth libraries or samples available. Here are a few links:
oauth-dot-net
DotNetOpenAuth
DevDefined.OAuth
This StackOverflow post
Reactive OAuth
The first three are quite large (and complicated) because they also include server side support. The StackOverflow code looks pretty straightforward, but I ended up using ReactiveOAuth because of the quirk in the Evernote implementation I mentioned in Part 1, and because I found this working example posted which made my life much easier :-).
The Evernote OAuth quirk is this:
The OAuth protocol specifies that you can send ‘oob’ (‘out of band’) as the callback URL in step 3 of the authentication process to tell the server that you don’t have a callback address. The typical ‘oob’ workflow is that (in workflow step 4), the service provider’s website will display an activation code that the user can copy and paste into the app they want to authorize to their account. This makes life easy for app developers because you can just launch the OAuth process in the default browser on whatever device you’re running on. The StackOverflow post I referenced above demonstrates that workflow.
However, Evernote doesn’t implement ‘oob’, which means I have to add a form to my plug-in that displays a web browser control. I can then use the Navigating callback to check for when Evernote is redirecting me to the callback I supplied in Step 4, and then extract my authorization token.
There are other ways to handle this, but the web browser control was the most straightforward for my needs.
Because of this quirk, I decided to make the best of a bad lot and use the same web browser control to log in to the user’s Evernote account so they can read the notes they’re creating in Evernote inside AutoCAD.
But then it got painful for a while – the sample code I found uses WPF and works perfectly, but I wanted to use WinForms. I couldn’t get my implementation to work, and spent a long time trying to debug the various HTTP calls taking place until I realized that the problem is that (the WinForms) System.Windows.Forms.WebBrowser behaves differently than (the WPF) System.Windows.Controls.WebBrowser. The difference was that (for some reason unknown to me) the Navigating event wasn’t firing on the WinForms control when Evernote was sending my token to my callback address. Everything worked fine once I’d switched over to WPF.
Here is the full (VS2012) project.
Here is the command to display WPF UserControl containing my WebBrowser in a palette (code stolen from Kean):
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Windows;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.EditorInput;
using System.Drawing;
  namespace AcadEvernoteTest
{
    public class MyCommandClass
    {
      static PaletteSet _ps = null;
      [CommandMethod("ENPALETTE")]
      public void ShowWPFPalette()
      {
        if (_ps == null)
        {
          // Create the palette set
          _ps = new PaletteSet("Evernote Connect");
          _ps.Size = new Size(600, 600);
          _ps.DockEnabled =
            (DockSides)((int)DockSides.None);
          // Create our first user control instance and
          // host it on a palette using AddVisual()
          UserControl1 uc = new UserControl1();
          _ps.AddVisual("AddVisual", uc);
        }
        // Display our palette set
        _ps.KeepFocus = true;
        _ps.Visible = true;
      }
    }
}
Here is the code that runs in the WPF form. Note that I cleaned up some of the Evernote code in Part 1, but not so much in this sample. The interesting part of the code (the OAuth part) is the Authorize() and webBrowser_Navigating() functions:
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Navigation;
using Codeplex.OAuth;
using System.Reactive.Linq;
using Microsoft.Win32;
using Thrift;
using Thrift.Protocol;
using Thrift.Transport;
using Evernote.EDAM.Type;
using Evernote.EDAM.UserStore;
using Evernote.EDAM.NoteStore;
using Evernote.EDAM.Error;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.EditorInput;
using ac = Autodesk.AutoCAD.ApplicationServices;
    namespace AcadEvernoteTest
{
  /// <summary>
  /// Interaction logic for UserControl1.xaml
  /// </summary>
  public partial class UserControl1 : UserControl
  {
    private const string m_ConsumerKey = "Your key here";
    private const string m_ConsumerSecret = "Your key here";
    private const string m_BaseUrl = "https://sandbox.evernote.com";
    private RequestToken m_RequestToken;
    private String m_AuthToken;
    private String m_NoteStoreUrl;
    private long m_AuthExpiration;
    private List<String> m_BlockNames;
    private String m_DrawingName;
    private NoteStore.Client m_NoteStore;
      private void IterateBlocks()
    {
      Document doc =
        ac.Application.DocumentManager.MdiActiveDocument;
      //We're in a palette - must lock the document
      using (DocumentLock docLock = doc.LockDocument())
      {
        Database db = doc.Database;
        using (Transaction tr = db.TransactionManager.StartTransaction())
        {
          m_BlockNames = new List<String>();
          m_DrawingName = db.Filename;
          BlockTable bt =
            tr.GetObject(db.BlockTableId, OpenMode.ForRead) as BlockTable;
          foreach (ObjectId btrId in bt)
          {
            BlockTableRecord btr =
              tr.GetObject(btrId, OpenMode.ForRead) as BlockTableRecord;
            m_BlockNames.Add(btr.Name);
          }
        }
      }
    }
        private DateTime EvernoteTimeStampToDateTime(long evernoteTimeStamp)
    {
      //See http://dev.evernote.com/documentation/reference/Types.html#Typedef_Timestamp
      // for description of Evernote timestamp
      System.DateTime theDateTime =
        new DateTime(1970, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc);
      return theDateTime.AddSeconds(evernoteTimeStamp / 1000);
    }
        //Sets our notestore variable (used to access notes etc).
    //Called once from our button1 click handler
    private void SetNoteStoreClient()
    {
      TTransport noteStoreTransport = new THttpClient(new Uri(m_NoteStoreUrl));
      TProtocol noteStoreProtocol = new TBinaryProtocol(noteStoreTransport);
      m_NoteStore = new NoteStore.Client(noteStoreProtocol);
    }
      //If note exists we append  text to its contents
    //If note doesn't exist we create it first
    private Note CreateOrUpdateNote(String txtToAdd)
    {
      NoteFilter filter = new NoteFilter();
      filter.Words = m_DrawingName;
      //We assume there's only one note for each drawing
      // and also that no note contains the drawing name in its contents
      // (just in its title).
      NoteList noteList = m_NoteStore.findNotes(m_AuthToken, filter, 0, 1);
      List<Note> foundNotes = noteList.Notes;
        Note noteToEdit;
      StringBuilder sb = new StringBuilder();
      if (foundNotes.Count == 1)
      {
        noteToEdit = foundNotes[0];
        sb.Append(m_NoteStore.getNoteContent(m_AuthToken, noteToEdit.Guid));
        sb.Replace("</en-note>", "<p>" + txtToAdd + "</p></en-note>");
        noteToEdit.Content = sb.ToString();
        noteToEdit = m_NoteStore.updateNote(m_AuthToken, noteToEdit);
      }
      else
      {
        noteToEdit = new Note();
        noteToEdit.Title = m_DrawingName;
        sb.Append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>" +
          "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">" +
          "<en-note><p>" + txtToAdd + "</p></en-note>");
        noteToEdit.Content = sb.ToString();
        noteToEdit = m_NoteStore.createNote(m_AuthToken, noteToEdit);
      }
      return noteToEdit;
    }
        //Return true if the API we're using is up to date
    //Otherwise return false.
    private bool CheckAPIVersion()
    {
      Uri userStoreUrl = new Uri(m_BaseUrl + "/edam/user");
      TTransport userStoreTransport = new THttpClient(userStoreUrl);
      TProtocol userStoreProtocol = new TBinaryProtocol(userStoreTransport);
      UserStore.Client userStore = new UserStore.Client(userStoreProtocol);
      return userStore.checkVersion("Evernote EDAMTest (C#)",
           Evernote.EDAM.UserStore.Constants.EDAM_VERSION_MAJOR,
           Evernote.EDAM.UserStore.Constants.EDAM_VERSION_MINOR);
    }
        private void AddNote()
    {
      String textToAdd;
      Document doc = ac.Application.DocumentManager.MdiActiveDocument;
      Database db = doc.Database;
      m_DrawingName = db.Filename;
      using (DocumentLock docLock = doc.LockDocument())
      {
        PromptStringOptions opts =
          new PromptStringOptions("\nEnter text for note:");
        opts.AllowSpaces = true;
        PromptResult res = doc.Editor.GetString(opts);
        if (res.Status != PromptStatus.OK)
        {
          return;
        }
        textToAdd = res.StringResult;
      }
      CreateOrUpdateNote(textToAdd);
    }
        private void Parse()
    {
      IterateBlocks();
      StringBuilder sb = new StringBuilder();
      sb.Append("<p>Blocks in Drawing:</p><p><ul>");
      foreach (String name in m_BlockNames)
      {
        sb.Append("<li>" + name + "</li>");
      }
      sb.Append("</ul></p>");
      CreateOrUpdateNote(sb.ToString());
    }
      //Store token info in registry for future use
    //Should really encrypt this.
    private void UpdateRegistry()
    {
      using (RegistryKey key =
        Registry.CurrentUser.CreateSubKey("Software\\SGP\\AcadEverNoteTest\\Token"))
      {
        if (null != key)
        {
          key.SetValue("Token", m_AuthToken);
          key.SetValue("NoteStoreUrl", m_NoteStoreUrl);
          key.SetValue("Expiration", m_AuthExpiration);
        }
       }
    }
      //Read any existing token info from registry
    private void ReadRegistry()
    {
      using (RegistryKey key =
        Registry.CurrentUser.OpenSubKey("Software\\SGP\\AcadEverNoteTest\\Token"))
      {
        if (null != key)
        {
          m_AuthToken = (String)key.GetValue("Token");
          m_NoteStoreUrl = (String)key.GetValue("NoteStoreUrl");
          m_AuthExpiration = long.Parse((String)key.GetValue("Expiration"));
        }
      }
    }
      public UserControl1()
    {
      InitializeComponent();
    }
      private void Button1_Click(object sender, RoutedEventArgs e)
    {
      ReadRegistry();
      if ((m_AuthToken == null)
        || (m_NoteStoreUrl == null)
        || (m_AuthExpiration == 0))
      {
        //Authorize on first run for this Windows login (no registry entries)
        Authorize();
      }
      else
      {
        DateTime expDate = EvernoteTimeStampToDateTime(m_AuthExpiration);
        DateTime now = DateTime.UtcNow;
        if (now > expDate)
        {
          //Our timestamp has expired - re-authorize
          Authorize();
        }
        else
        {
          //We're already authorized and our token is current
          //Now check API version is up-to-date
          if (!CheckAPIVersion())
          {
            MessageBox.Show("Oops! This plug-in is using an out of date version of the Evernote API.",
              "API Error");
            return;
          }
          SetNoteStoreClient();
          webBrowser.Navigate(m_BaseUrl);
          Button1.IsEnabled = false;
          Button2.IsEnabled = true;
          Button3.IsEnabled = true;
        }
      }
    }
        private void Authorize()
    {
      var authorizer = new OAuthAuthorizer(m_ConsumerKey, m_ConsumerSecret);
      authorizer.GetRequestToken(m_BaseUrl + "/oauth",
        new Codeplex.OAuth.Parameter("oauth_callback", "http://localhost/myapp"))
      .Select(res => res.Token)
        //.ObserveOnDispatcher()
      .Subscribe(token =>
      {
        m_RequestToken = token;
        var url = authorizer.BuildAuthorizeUrl(m_BaseUrl + "/OAuth.action",
          token);
        Dispatcher.BeginInvoke(new Action(() => webBrowser.Navigate(new Uri(url))));
      });
    }
        private void webBrowser_Navigating(object sender, NavigatingCancelEventArgs e)
    {
      if (e.Uri.ToString().StartsWith("http://localhost/myapp"))
      {
        var splitString =
          e.Uri.ToString().Split('&').Select(s => s.Split('=')).ToDictionary(s => s.First(), s => s.Last());
        string verifier = splitString["oauth_verifier"];
        var authorizer = new OAuthAuthorizer(m_ConsumerKey, m_ConsumerSecret);
        authorizer.GetAccessToken(m_BaseUrl + "/oauth",
          m_RequestToken, verifier)
        //.ObserveOnDispatcher()
        .Subscribe(res => {
            try {
              m_AuthToken = Uri.UnescapeDataString(res.Token.Key);
              m_NoteStoreUrl =
                Uri.UnescapeDataString(res.ExtraData["edam_noteStoreUrl"].First());
              m_AuthExpiration = long.Parse(res.ExtraData["edam_expires"].First());
              UpdateRegistry();
              if (!CheckAPIVersion())
              {
                MessageBox.Show("Oops! This plug-in is using an out of date version of the Evernote API.", "API Error");
                return;
              }
              //Initialize NoteStore access
              SetNoteStoreClient();
              //This is an asynchronous callback, so can't directly call methods/properties
              // on the following controls.
              //Send webbrowswer control to Evernote Web console
              Dispatcher.BeginInvoke(new Action(() => webBrowser.Navigate(m_BaseUrl)));
              //Deactivate connect button and deactivate the other two
              Dispatcher.BeginInvoke(new Action(() => Button1.IsEnabled = false));
              Dispatcher.BeginInvoke(new Action(() => Button2.IsEnabled = true));
              Dispatcher.BeginInvoke(new Action(() => Button3.IsEnabled = true));
            }
            catch (KeyNotFoundException) {
              //Add error handler
            }
            finally
            {
            }
        });
      }
   }
        private void Button2_Click(object sender, RoutedEventArgs e)
    {
      Parse();
    }
        private void Button3_Click(object sender, RoutedEventArgs e)
    {
      AddNote();
    }
  }
}
(BTW You can add the ReactiveOAuth assemblies to your project using Nuget).
And finally, here is a screenshot of Evernote (hosted in my palette) requesting my permission for the plug-in to access my account:
I’m not sure where to take this series next. This could be the last part (of 2), or I may come back and try a different OAuth library either with Evernote or another web service. Either way, that will probably be after Christmas (or Week of Rest, as we call it in Autodesk).

