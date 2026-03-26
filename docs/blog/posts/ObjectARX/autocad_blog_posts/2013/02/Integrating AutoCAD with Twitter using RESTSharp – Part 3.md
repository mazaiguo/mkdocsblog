---
title: "Integrating AutoCAD with Twitter using RESTSharp – Part 3"
date: 2013-02-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
description: "In part 1 I learned the basics of RESTSharp using the Twitter search API. This was an easy starting point because that API doesn’t need authenticat..."
author: Autodesk
---
# Integrating AutoCAD with Twitter using RESTSharp – Part 3

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/integrating-autocad-with-twitter-using-restsharp-part-3.html

## 文章内容

By Stephen Preston
In part 1 I learned the basics of RESTSharp using the Twitter search API. This was an easy starting point because that API doesn’t need authentication.
In part 2 I implemented ‘out of band’ OAuth authentication – opening the user’s default browser for them to authorize my app and then paste a PIN back into AutoCAD for me to use to request my access key from Twitter. (In my opinion, this is better than using an embedded web browser control, because the user is reassured that your app isn’t phishing them).
In this final installment, I’ll use the Status API to update my status on Twitter(otherwise known as tweeting) from the AutoCAD command line. This isn’t really doing anything new with RESTSharp – I’m just creating another RestRequest – the only change is that I’ll be making a POST request instead of a GET request. This is because I want to update something (my status) on the Twitter server.
Here is the commented code for the manual tweeting command (TWEETTHIS), including a slightly refactored and renamed ‘OAuthTest’ method from the sample code from the previous installment:
using System;
using System.Net;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.EditorInput;
using RestSharp;
using RestSharp.Authenticators.OAuth;
using RestSharp.Contrib;
using RestSharp.Authenticators;
using System.Diagnostics;
  namespace AcadTwitterTest1
{
  public class TwitterTestClass
  {
      private const string m_ConsumerKey = "YOUR KEY HERE";
    private const string m_ConsumerSecret = "YOUR KEY HERE";
    private static RestClient m_Client; 
      //The OAuthTest class in my previous blog post
    // but with a slight refactoring
    [CommandMethod("AUTHORIZE")]
    public static void DoOAuth()
    {
      Editor ed =
        Application.DocumentManager.MdiActiveDocument.Editor;
      var baseUrl = "http://api.twitter.com";
      m_Client = new RestClient(baseUrl);
      //Request token using our consumer and secret keys
      m_Client.Authenticator =
        OAuth1Authenticator.ForRequestToken(m_ConsumerKey, m_ConsumerSecret);
      var request = new RestRequest("oauth/request_token", Method.POST);
      var response = m_Client.Execute(request);
      if (response.StatusCode != HttpStatusCode.OK)
      {
        m_Client = null;
        ed.WriteMessage("\nOops! Something went wrong - couldn't link to your Twitter account\n");
        return;
      }
        var qs = HttpUtility.ParseQueryString(response.Content);
      var oauth_token = qs["oauth_token"];
      var oauth_token_secret = qs["oauth_token_secret"];
        //authorize using returned token
      request = new RestRequest("oauth/authorize");
      request.AddParameter("oauth_token", oauth_token);
      var url = m_Client.BuildUri(request).ToString();
      //Launch default browser with authorization URL
      Process.Start(url);
      //User logs into Twitter and clicks 'authorize' button
      //Browser displays PIN
        //Ask user to enter the PIN displayed in the browser
      PromptStringOptions opts =
        new PromptStringOptions("\nEnter Twitter authorization PIN:");
      opts.AllowSpaces = true;
      PromptResult res = ed.GetString(opts);
      if (res.Status != PromptStatus.OK)
      {
        ed.WriteMessage("\nCommand cancelled.\n");
        m_Client = null;
        return;
      }
      string strPIN = res.StringResult.Trim();
      if (strPIN == "")
      {
        ed.WriteMessage("\nCommand cancelled.\n");
        m_Client = null;
        return;
      }
        //Use PIN to request access token for users account
      request = new RestRequest("oauth/access_token", Method.POST);
      m_Client.Authenticator = OAuth1Authenticator.ForAccessToken(
      m_ConsumerKey, m_ConsumerSecret, oauth_token, oauth_token_secret, strPIN
      );
      response = m_Client.Execute(request);
      if (response.StatusCode != HttpStatusCode.OK)
      {
        m_Client = null;
        ed.WriteMessage("\nOops! Something went wrong - couldn't link to your Twitter account\n");
        return;
      }
        qs = HttpUtility.ParseQueryString(response.Content);
      oauth_token = qs["oauth_token"];
      oauth_token_secret = qs["oauth_token_secret"];
        //Test it worked by calling verify_credentials API
      //Note - the code listed on
      // https://github.com/restsharp/RestSharp/blob/master/RestSharp.IntegrationTests/oAuth1Tests.cs
      // contains a bug (maybe the API changed). The next line in
      // the original is
      // request = new RestRequest("account/verify_credentials.xml");
      // i.e. Its missing the 1.1.
      request = new RestRequest("1.1/account/verify_credentials.json");
      m_Client.Authenticator = OAuth1Authenticator.ForProtectedResource(
      m_ConsumerKey, m_ConsumerSecret, oauth_token, oauth_token_secret
      );
      //Put a breakpoint on following line and check that
      // response.StatusCode == HttpStatusCode.OK.
      // And check the returned JSON string.
      response = m_Client.Execute(request);
      if (response.StatusCode != HttpStatusCode.OK)
      {
        m_Client = null;
        ed.WriteMessage("\nOops! Something went wrong - couldn't link to your Twitter account\n");
      }
    }
      //Prompts user for text to tweet.
    [CommandMethod("TWEETTHIS")]
    public static void tweet()
    {
      Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      //If m_Client is null, then we've not authenticated yet
      if (m_Client == null)
      {
        DoOAuth();
      }
      //If m_Client is still null then there was a problem authenticating
      if (m_Client == null)
      {
        return;
      }
      //Ask user to enter tweet text
      PromptStringOptions opts =
        new PromptStringOptions("\nTweet away (<= 140 chars):");
      opts.AllowSpaces = true;
        //Loop until string is the correct length
      string strTweet;
      do
      {
        PromptResult res = ed.GetString(opts);
        if (res.Status != PromptStatus.OK)
        {
          ed.WriteMessage("\nCommand cancelled.\n");
          return;
        }
        strTweet = res.StringResult.Trim();
        if (strTweet == "")
        {
          ed.WriteMessage("\nCommand cancelled.\n");
          return;
        }
      } while (strTweet.Length > 140);
        //Update status on Twitter
      var request =
        new RestRequest("1.1/statuses/update.json", Method.POST);
      request.AddParameter("status", strTweet);
      var response = m_Client.Execute(request);
      if (response.StatusCode != HttpStatusCode.OK)
      {
        m_Client = null;
        ed.WriteMessage("\nOops! Something went wrong - couldn't send your tweet\n");
      }
    }
  }
}
There’s nothing special in the command itself, so no screenshot. It just tweets whatever you type when prompted by the command (and asks for authorization if you’ve not already run the AUTHORIZE command).
Note that I’m not storing the authorization token anywhere, so the app has to be re-authorized every time it runs.
After writing this command, I started thinking of other things I could do with the Twitter Status API. The whole point of Twitter is to send frequent status updates to your followers – to spam them with completely inane comments (the more inane your comments, the more your followers will love you :-). That was when I thought of using AutoCAD events to trigger tweets. I considered tweeting every time I added an entity to a drawing, but I thought that might be going too far (and the Twitter API is throttled), so I decided that tweeting every time a new drawing is created or opened would probably be frequent enough to annoy someone’s followers, but infrequent enough to avoid being throttled.
To implement that, I added the following methods to my TwitterTestClass:
    //Starts tweeting about every document you open or create
    [CommandMethod("STARTAUTOTWEETING")]
    public static void StartAutoTweeting()
    {
      Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      //Don't subscribe to event more than once.
      if (m_AutoTweeting)
      {
        return;
      }
      //If m_Client is null, then we've not authenticated yet
      if (m_Client == null)
      {
        DoOAuth();
      }
      //If m_Client is still null then there was a problem authenticating
      if (m_Client == null)
      {
        return;
      }
      //Subscribe to DocumentCreated event
      Application.DocumentManager.DocumentCreated +=
        DocumentManager_DocumentCreated;
      //Set AutoTweeting flag to true so only respond to event once.
      m_AutoTweeting = true;
      ed.WriteMessage("\nYou are now Auto-Tweeting\n");
    }
      //Gives your followers respite by cancelling the AutoTweeting
    [CommandMethod("STOPAUTOTWEETING")]
    public static void StopAutoTweeting()
    {
      Editor ed =
        Application.DocumentManager.MdiActiveDocument.Editor;
      //Unsubscribe to event if we were subscribed to it
      if (m_AutoTweeting)
      {
        Application.DocumentManager.DocumentCreated -=
          DocumentManager_DocumentCreated;
        //REset AutoTweeting flag so we can resubsribe later.
        m_AutoTweeting = false;
        ed.WriteMessage("\nYou have stopped Auto-Tweeting\n");
      }
      }
      //Our event handler
    static void DocumentManager_DocumentCreated(
                      object sender,
                      DocumentCollectionEventArgs e)
    {
      //This function should only be called if
      // we've already authorized Twitter account access
      // so this check should be unecessary.
      if (m_Client == null)
      {
        return;
      }
      //Grab document name
      string strDocName = e.Document.Name;
      //Strip out path to leave just filename
      if (strDocName.Contains("\\"))
      {
        strDocName =
          strDocName.Substring(strDocName.LastIndexOf("\\")+1);
      }
      //Construct tweet
      string strTweet = "I just started work on a new AutoCAD DWG: "
                         + strDocName;
      //Trim tweet to 140 chars (if filename is very long)
      if (strTweet.Length > 140)
      {
        strTweet = strTweet.Substring(0, 137) + "...";
      }
        //Post the tweet
      var request =
        new RestRequest("1.1/statuses/update.json", Method.POST);
      request.AddParameter("status", strTweet);
      var response = m_Client.Execute(request);
      //Tell the user if something went wrong.
      //Note: If we try to tweet the same text twice, then response.StatusCode
      // will be Forbidden
      if (response.StatusCode != HttpStatusCode.OK)
      {
        Editor ed =
          Application.DocumentManager.MdiActiveDocument.Editor;
        ed.WriteMessage("\nOops! Something went wrong - couldn't autotweet\n");
      }
    }
And also a class helper variable:
    private static bool m_AutoTweeting = false;
Now we’ve got a handle on the RESTSharp API, the code is pretty straightforward (albeit not very tidy). The command names are self-documenting – STARTAUTOTWEETING and STOPAUTOTWEETING. And here is the result in my Twitterfeed after creating a few new drawings:
And that brings to an end my experiment with the Twitter API. (It turned out to be so simple to use with RESTSharp that I’m bored with it now :-). To summarize what I learned:
I used the Twitter API because I wanted to try ‘out of band’ authentication. That, for me, is better than an embedded web browser control (unless you actually want to display a web page in your app).
I used RESTSharp just because I found mention of it when googling and it looked quite simple/helpful. That indeed turned out to be the case. I’m not saying RESTSharp is the best there is, but its certainly an improvement on using the core .NET Framework classes if you’re making multiple calls to the same REST API server.
JSON derserializers are cool. (If you need to know the result from a REST request. I used them for the Search API, but I only cared about the response StatusCode when tweeting).
(The author of this post accepts no responsibility for you being ‘unfollowed’ by all your friends if you use this code :-D).

## 评论

**内容**: verdier86@hotmail.com said...
Is it possible to get a copy of the source code?
Reply
12/27/2013 at 03:27 AM

---
**内容**: Madhukar Moogala said in reply to verdier86@hotmail.com...
Hi Verdier,
I've upgraded my laptop since making this post, and it looks like I deleted this project during the migration process. But you can still copy and paste the code into your own project.
Sorry about that,
Stephen
Reply
01/01/2014 at 01:17 PM

---
