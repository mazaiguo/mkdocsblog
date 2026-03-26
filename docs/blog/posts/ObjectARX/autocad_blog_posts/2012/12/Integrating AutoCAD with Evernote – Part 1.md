---
title: "Integrating AutoCAD with Evernote – Part 1"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - DWG
  - Plugin
description: "Its time for me to start getting to grips with REST APIs, so I decided to begin my adventure by playing around with the Evernote API. I tend to use..."
author: Autodesk
---
# Integrating AutoCAD with Evernote – Part 1

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/integrating-autocad-with-evernote-part-1.html

## 文章内容

By Stephen Preston
Its time for me to start getting to grips with REST APIs, so I decided to begin my adventure by playing around with the Evernote API. I tend to use AutoCAD as my ‘console’ when experimenting with new APIs, so it was an obvious choice to write an AutoCAD plug-in that took some information from a DWG and posted it as a Note in Evernote.
I opted for Evernote as my first venture into REST, because several people had told me that the Evernote developer information on their website was really well written. I could just as easily have used something else, because REST is pretty much the API of choice for web services these days – for example DropBox or Flickr, or even BIM360 Glue (but Jeremy beat me to that one).
The goals I set for myself for this exercise were:
Understand what web based REST APIs actually are.
See how a web service vendor like Evernote exposes those REST APIs to developers.
Understand how to authenticate to a web service using OAuth.
Health warning – I’m documenting a learning process here. Its possible that you’ll find more polished code samples elsewhere (its also possible that I’ll later find that I ‘went the long way around’ with some of my code). However, I hope that I’ll save you some time by documenting some of the learning process and maybe start you thinking about consuming web services in your own apps.
For this first post ina series of (as yet undetermined length) I’ll very quickly introduce the concept of REST APIs and then show a simple AutoCAD plug-in that accesses Evernote using a private developer key. I’ll cover OAuth with Evernote in the next post.
What is REST?
My first question was what exactly is a REST API in the context of accessing a web service, and from the point of view of someone like myself who has never done any web programming? The problem with finding the answer to that question is the same as finding any other information on the web – you get so many hits returned for your search that you don’t know where to start. I found these two articles explained REST straightforwardly enough that I could understand it, so I’m not going to try to rewrite all that in my own words:
http://rest.elkstein.org/
http://www.infoq.com/articles/rest-introduction
Both these articles were written in the ‘early days’ of REST (way back in 2007/2008 :-), when it wasn’t obvious that REST would be widely adopted.
My own elevator pitch for what is REST (as a client) is this:
You make a call to a web service using a simple URL (e.g. http://www.example.com/customers/1234). Any parameters you want to pass in are a part of that URL (e.g. I’m asking for information on customer number 1234). The web service responds with the answer to your request. And that’s it.
Its up to the creator of the web service to define the URLs you’ll call, but general convention is to make them (relatively) human readable. If you’re a web programming beginner, then that’s really all you need to know to get up and running.
In .NET, you’ll be using the HttpWebRequest and HttpWebResponse classes if you want to to make raw REST calls, but many vendors (Evernote is one) provide an SDK that gives you wrappers for their RESTful services – so you don’t necessarily even have to know you’re dealing with HTTP.
Even if you can’t find a .NET wrapper for your favorite web service, you can still use something like RESTSharp to simplify your web services requests.
The Evernote SDK
Before I start on the details, here are two reasons why (with hindsight) I should have started my REST learning with something other than Evernote:
Evernote changed their authentication system very recently, and not all their samples have been updated to reflect this (by which I mean their C# sample is out of date at the time of writing). It also means that many of the forum posts you’ll read refer to the old way of doing things. Hopefully, this will be fixed soon.
Evernote uses OAuth authentication, but they have a little quirk that made it slightly more cumbersome to implement the authentication procedure than other services. More on that in a future post.
To get started with the Evernote SDK, simply go to dev.evernote.com and click on the big green button that says “Get started with the API”. As you’d expect from what it says on the button, that will take you through the steps you need to get started with the API :-). I’m not going to describe the SDK or object model here, as the Evernote developer documentation does that very well already.
There are two ways to work with the Evernote Cloud API. This is a fairly typical model you’ll encounter:
If you’re writing an app you want to sell or give to others, then you’ll need to apply for an API key that you’ll use to authenticate your app for each user using the OAuth protocol.
If you’re developing an app that you’ll just use with your own Evernote account then you can request a ‘developer token’ that gives API access to just your account without the need to use OAuth. This is much simpler than using OAuth when you’re getting started – just make sure you don’t tell anyone your key or they will have full access to your account.
I’ll be using the developer token in this post, but I’ll switch to an API key when I add OAuth.
Once you’ve downloaded the Evernote C# SDK, created an account on the Evernote sandbox server, and obtained your developer token, you’re ready to start coding.
Before jumping into my AutoCAD sample, you might prefer to run the sample included in the Evernote SDK. Just paste your developer token into the placeholder in the code, set a breakpoint, and hit F5.
My AutoCAD example is derived from the SDK sample. I’ve just moved the code across to an AutoCAD plug-in project and prettied it up a little bit. The plug-in defines two commands:
ENNOTE – Prompts for text at the command line that is then added to an Evernote Note.
ENBLOCKS – Lists the blocks contained in the current drawing in an Evernote Note.
Download the full sample here. (Its a VS2012 project).
If you want to do this from scratch, setup the project using the AutoCAD .NET Wizards to create a new AutoCAD C# plug-in project (or create a Class Library project and add the AutoCAD managed assemblies by hand), and then add the Evernote the Thrift assemblies from the Evernote SDK. That’s all you need – just two extra references.
Here is the code. Make sure you replace the “Your developer token here” placeholder text with your developer token before you run it. Full error handling is left as an exercise for the reader, and note that I’m not cleaning up the input text when creating my XML strings, so its possible to enter text that will break the XML:
using System;
using System.Collections.Generic;
using System.Text;
using Thrift;
using Thrift.Protocol;
using Thrift.Transport;
using Evernote.EDAM.Type;
using Evernote.EDAM.UserStore;
using Evernote.EDAM.NoteStore;
using Evernote.EDAM.Error;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.EditorInput;
    namespace AcadEvernoteTest
{
  public class MyCommandClass
  {
    private static List<String> m_BlockNames;
    private static String m_DrawingName;
    private static NoteStore.Client m_NoteStore;
    private static UserStore.Client m_UserStore;
    //Change this if you're using production server
    private  const string m_BaseUrl = "https://sandbox.evernote.com";
    //TODO: Add your developer token here
    private const String m_AuthToken = "Your developer token";
        //Reuqest a string on the command line
    // and add it as a Note in Evernote
    [CommandMethod("EnNote")]
    public static void EnNote()
    {
      if (InitEvernote())
      {
        AddNote();
      }
    }
        //Parse all blocktablerecords in drawing
    // and add list of names to Note in Evernote
    [CommandMethod("EnBlocks")]
    public static void EnBlocks()
    {
      if (InitEvernote())
      {
        Parse();
      }
    }
        //Ask user to enter text for a Note and create/update note
    private static void AddNote()
    {
      String textToAdd;
      Document doc = Application.DocumentManager.MdiActiveDocument;
      Database db = doc.Database;
      //Use DWG filename as Note title
      m_DrawingName = db.Filename;
      //Get string from user
      PromptStringOptions opts =
          new PromptStringOptions("\nEnter text for note:");
      opts.AllowSpaces = true;
      PromptResult res = doc.Editor.GetString(opts);
      if (res.Status != PromptStatus.OK)
      {
        return;
      }
      textToAdd = res.StringResult;
      //Create or update Note
      CreateOrUpdateNote(textToAdd);
    }
        //Creates a list of blocktablerecord names
    // and adds them to a Note
    private static void Parse()
    {
      //Iterate BTRs gathering their names
      IterateBlocks();
      //Build string to add to Note
      StringBuilder sb = new StringBuilder();
      sb.Append("<p>Blocks in Drawing:</p><p><ul>");
      foreach (String name in m_BlockNames)
      {
        sb.Append("<li>" + name + "</li>");
      }
      sb.Append("</ul></p>");
      //Add string to new or existing note
      CreateOrUpdateNote(sb.ToString());
    }
        //Extract nanes of all blocktabl records from current drawing
    private static void IterateBlocks()
    {
      Database db = Application.DocumentManager.MdiActiveDocument.Database;
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
        //If note exists we append  text to its contents
    //If note doesn't exist we create it first
    private static Note CreateOrUpdateNote(String txtToAdd)
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
          "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
          + "<en-note><p>" + txtToAdd + "</p></en-note>");
        noteToEdit.Content = sb.ToString();
        noteToEdit = m_NoteStore.createNote(m_AuthToken, noteToEdit);
      }
      return noteToEdit;
    }
        //Return true if the API we're using is up to date
    //Otherwise return false.
    //(Also sets userstore and notestore member variables)
    private static bool InitEvernote()
    {
      //Set userstore
      SetUserStoreClient();
      //Check API is current
      bool bCurrent =  m_UserStore.checkVersion("Evernote EDAMTest (C#)",
            Evernote.EDAM.UserStore.Constants.EDAM_VERSION_MAJOR,
            Evernote.EDAM.UserStore.Constants.EDAM_VERSION_MINOR);
      //If API is current, set notestore
      if (bCurrent)
      {
        SetNoteStoreClient();
      }
      return bCurrent;
    }
        //Sets notestore member variable (used to access notes etc).
    private static void SetNoteStoreClient()
    {
      // Get the URL used to interact with the contents of the user's account
      // When your application authenticates using OAuth, the NoteStore URL
      // will be returned along with the auth token in the final OAuth request.
      // In that case, you don't need to make this call.
      String noteStoreUrl = m_UserStore.getNoteStoreUrl(m_AuthToken);
      TTransport noteStoreTransport = new THttpClient(new Uri(noteStoreUrl));
      TProtocol noteStoreProtocol = new TBinaryProtocol(noteStoreTransport);
      m_NoteStore = new NoteStore.Client(noteStoreProtocol);
    }
      //Sets Userstore member variable.
    //Access to notestore is via userstore when using a developer token.
    private static void SetUserStoreClient()
    {
      Uri userStoreUrl = new Uri(m_BaseUrl + "/edam/user");
      TTransport userStoreTransport = new THttpClient(userStoreUrl);
      TProtocol userStoreProtocol = new TBinaryProtocol(userStoreTransport);
      m_UserStore = new UserStore.Client(userStoreProtocol);
    }
  }
}
Login to your Evernote sandbox account, and you should see something like this:
And that’s the end of Part 1. Here’s what I learned:
Using REST APIs from .NET (and calling them from a desktop application) is really simple.
Most web service providers post wrappers for their REST APIs so you can more easily use them on your platform of choice.
They’re more likely to provide iOS, Android/Java or Python wrappers – but if they don’t provide .NET wrappers themselves then someone else has usually written one.
Next time I’ll show how to use OAuth authentication to connect to any Evernote user’s account from an AutoCAD plug-in.

## 评论

**内容**: Dorothy Schmidt said...
I ve been hunting for a site that provides such information for several days therefore I appreciate this post. It also wishes to emphasize that if you are looking for erbium laser benefits you should definitely visit it.
Reply
03/24/2024 at 02:28 PM

---
