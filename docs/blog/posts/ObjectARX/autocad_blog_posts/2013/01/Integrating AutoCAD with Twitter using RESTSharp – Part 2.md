---
title: "Integrating AutoCAD with Twitter using RESTSharp – Part 2"
date: 2013-01-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Plugin
description: "In Part 1, I started learning RESTSharp via the Twitter search API – an API that doesn’t require authentication to use. My goal for this ‘Part 2’ p..."
author: Autodesk
---
# Integrating AutoCAD with Twitter using RESTSharp – Part 2

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/integrating-autocad-with-twitter-using-restsharp-part-2.html

## 文章内容

By Stephen Preston
In Part 1, I started learning RESTSharp via the Twitter search API – an API that doesn’t require authentication to use. My goal for this ‘Part 2’ post is to test basic OAuth using RESTSharp - specifically “Out Of Band’ (OOB) authentication. You’ll recall that OOB is where we launch the user’s default browser for them to authorize our app, and they are then given a PIN that they must type into the app they want to authorize – in this case our AutoCAD plug-in.
The advantage (or disadvantage, depending how you look at it) of blogging as you learn – rather than finishing a project and going back to document it afterwards – is that you never know how hard (or how easy) something will turn out to be. I was lucky that when I searched for a RESTSharp OAuth example, I almost immediately came across this test harness on the RESTSharp GitHub site that demonstrated how to use OAuth with Twitter.
Great – less work for me. But now you probably think I planned this because I’m lazy :-).
Here is the simple conversion of that code to work in AutoCAD – and note too that the GitHub version has a small bug in the final REST API call to account/verify_credentials – I assume the API has changed since that code was written. By the time we make that final call, the authorization process is complete and we have our authorization token – the call is to test that the OAuth process was successful.
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
    [CommandMethod("OATEST")]
    public static void OAuthTest()
    {
      const string consumerKey = "YOUR KEY HERE";
      const string consumerSecret = "YOUR KEY HERE";
        var baseUrl = "http://api.twitter.com";
      var client = new RestClient(baseUrl);
      //Request token using our consumer and secret keys
      client.Authenticator =
        OAuth1Authenticator.ForRequestToken(consumerKey, consumerSecret);
      var request = new RestRequest("oauth/request_token", Method.POST);
      var response = client.Execute(request);
      var qs = HttpUtility.ParseQueryString(response.Content);
      var oauth_token = qs["oauth_token"];
      var oauth_token_secret = qs["oauth_token_secret"];
        //authorize using returned token
      request = new RestRequest("oauth/authorize");
      request.AddParameter("oauth_token", oauth_token);
      var url = client.BuildUri(request).ToString();
      //Launch default browser with authorization URL
      Process.Start(url);
      //User logs into Twitter and clicks 'authorize' button
      //Browser displays PIN
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      //Ask user to enter the PIN displayed in the browser
      PromptStringOptions opts =
        new PromptStringOptions("\nEnter Twitter authorization PIN:");
      opts.AllowSpaces = true;
      PromptResult res = ed.GetString(opts);
      if (res.Status != PromptStatus.OK)
        return;
      string strPIN = res.StringResult.Trim();
      if (strPIN == "")
        return;
        //Use PIN to request access token for users account
      request = new RestRequest("oauth/access_token", Method.POST);
      client.Authenticator = OAuth1Authenticator.ForAccessToken(
      consumerKey, consumerSecret, oauth_token, oauth_token_secret, strPIN
      );
      response = client.Execute(request);
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
      client.Authenticator = OAuth1Authenticator.ForProtectedResource(
      consumerKey, consumerSecret, oauth_token, oauth_token_secret
      );
      //Put a breakpoint on following line and check that
      // response.StatusCode == HttpStatusCode.OK.
      // And check the returned JSON string.
      response = client.Execute(request);
    }
  }
}
I’ve removed my Consumer Key and Consumer Secret Key from the code sample above. To create your own, you have to login to your Twitter account, and then create a new app at https://dev.twitter.com/apps. (See this link for details of the Twitter authentication process).
Set a breakpoint on the last line of code before you run it in the debugger.
Running the OATEST command in AutoCAD launches my default browser for me to login to Twitter and authorize the app (note that I’ve given my app the highest access level by editing the settings for my access keys):
When I’ve entered the username and password for the test account (that I set up specially for this test) and clicked the Authorize app button, Twitter gives me my PIN:
I type this PIN when prompted on the AutoCAD commandline, and hit the breakpoint I set at the end of my function. Stepping over that line and querying the ‘response’ variable in the debugger, I can see that the returned JSON string looks like this:
{
"id":1058645280,
"entities":
{
"description":
  {
  "urls":[]
  }
},
"profile_use_background_image":true,
"default_profile":true,
"statuses_count":0,
"profile_text_color":"333333",
"id_str":"1234567890",
"screen_name":"SGP2013",
"follow_request_sent":false,
"followers_count":2,
"profile_image_url_https":"https:\/\/twimg0-a.akamaihd.net\/sticky\/default_profile_images\/default_profile_0_normal.png",
"utc_offset":null,
"profile_sidebar_border_color":"C0DEED",
"name":"Stephen Preston",
"lang":"en",
"is_translator":false,
"listed_count":0,
"created_at":"Thu Jan 03 19:57:42 +0000 2013",
"protected":false,
"profile_background_tile":false,
"profile_sidebar_fill_color":"DDEEF6",
"url":null,"profile_image_url":"http:\/\/a0.twimg.com\/sticky\/default_profile_images\/default_profile_0_normal.png",
"following":false,
"default_profile_image":true,
"profile_background_color":"C0DEED",
"favourites_count":0,
"friends_count":4,
"contributors_enabled":false,
"location":null,
"time_zone":null,
"notifications":false,
"profile_background_image_url":"http:\/\/a0.twimg.com\/images\/themes\/theme1\/bg.png",
"verified":false,
"profile_link_color":"0084B4",
"description":null,
"profile_background_image_url_https":"https:\/\/twimg0-a.akamaihd.net\/images\/themes\/theme1\/bg.png",
"geo_enabled":false
}
In this post I’ve shown how to use OOB OAuth authentication. This is my preferred approach for an AutoCAD commandline app – and something I found wasn’t possible (yet) using the Evernote API. In my next post I’ll find something more interesting to do with the Twitter API now my OAuth is working.

