---
title: "Preventing AutoCAD from entering a zero doc state"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Unicode
description: "When AutoCAD is in a zero document state, you have very limited access to AutoCAD's functionality. One straightforward method of solving this probl..."
author: Autodesk
---
# Preventing AutoCAD from entering a zero doc state

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/preventing-autocad-from-entering-a-zero-doc-state.html

## 文章内容

By Virupaksha Aithal
When AutoCAD is in a zero document state, you have very limited access to AutoCAD's functionality. One straightforward method of solving this problem is to prevent AutoCAD from entering the zero document state.
For this, handle the "DocumentCollection.DocumentToBeDestroyed" event, in this event handler; make a call to "ExecuteInApplicationContext" passing a callback. Add a new document, when AutoCAD calls the callback function.
static bool bBeginQuit = false;
  [CommandMethod("ZeroDocState")]
public static void ZeroDocState()
{
    Application.BeginQuit +=new EventHandler(Application_BeginQuit);
    DocumentCollection docMg = Application.DocumentManager;
    docMg.DocumentToBeDestroyed +=
        new DocumentCollectionEventHandler(docMg_DocumentToBeDestroyed);
}
    static void Application_BeginQuit(object sender, EventArgs e)
{
    bBeginQuit = true;
}
  static void docMg_DocumentToBeDestroyed(object sender,
                                    DocumentCollectionEventArgs e)
{
    DocumentCollection docman = (DocumentCollection)sender;
      //1 - means, after closing the document AutoCAD will
    //be in zero document state, so call ExecuteInApplicationContext
    if (docman.Count == 1)
    {
        Application.DocumentManager.ExecuteInApplicationContext(
                                      ApplicationContextAdd, null);
    }
}
  static void ApplicationContextAdd(object data)
{
    try
    {
        if(!bBeginQuit)
            Application.DocumentManager.Add("");
    }
    catch
    {
      }
}

## 评论

**内容**: Tony Tanzillo said...
It looks like you haven't bothered to test your solution.
AutoCAD will enter zero document state when the user issues the QUIT command.
What then?
Reply
09/22/2012 at 01:25 AM

---
**内容**: Tony Tanzillo said...
On second thought... what possible legitimate reason can there be to prevent AutoCAD from entering zero-document state?
"When AutoCAD is in a zero document state, you have very limited access to AutoCAD's functionality"..
That is kind of like saying "when you park your car and turn off the ignition, you have very limited access to your car's functionality".
Duh
Reply
09/22/2012 at 01:31 AM

---
**内容**: Madhukar Moogala said in reply to Tony Tanzillo...
Tony - The analogy you used answers your own question, so I'm not sure the reason for your 'duh'. And this is a question that is frequently asked by ADN partners, so many people clearly do want this behavior.
Its very kind of you to pop onto this blog occasionally to give us the benefit of your knowledge - our whole community benefits if we all share with each other - but please keep your comments constructive when you do visit. If you can't post a comment without being condescending, then please don't post comments.
Reply
09/22/2012 at 03:35 PM

---
**内容**: Tony Tanzillo said in reply to Madhukar Moogala...
ADN partners that don't understand why preventing AutoCAD from entering a zero-document state is not not a legitimate requirement which they shouldn't do, should be made to understand why, rather than thoughtlessly accommodated, without regards for whether the need is legitimate and/or interferes with the normal intended use of the product.
If a user closes all open documents, they did it for a reason. If the ADN partner doesn't know how to display their own UI in zero-document state (which is usually the reason why they want to prevent the user from getting there) then they should be shown how to do that, rather than shown how to implement a kludge that interferes with the normal use of the product, and the use of other extensions that may display a different UI when AutoCAD enters zero-document state.

Reply
09/24/2012 at 01:25 PM

---
**内容**: Madhukar Moogala said in reply to Tony Tanzillo...
Thank you for expanding on your previous comment, Tony. I agree that its always important to understand the underlying reason why someone is asking for a specific functionality. But we'll have to agree to disagree on the 'legitimacy' of this one. We have a large community of programmers who customize AutoCAD for many reasons, and in very different environments. They know what they and their customers want and need - not us. To say its 'not a legitimate requirement' is using too broad a brush. A reductio ad absurdum of this is that any AutoCAD customization changes the behavior some AutoCAD user has come to expect, ergo all customization is illegitimate.
Reply
09/24/2012 at 03:06 PM

---
**内容**: Tony Tanzillo said in reply to Madhukar Moogala...
The solution posted crashes AutoCAD when the QUIT command is used, which I believe does qualify as interference.
Reply
09/25/2012 at 07:49 AM

---
**内容**: Madhukar Moogala said in reply to Tony Tanzillo...
Thank you Tony. My previous responses were to your second comment - I hadn't referred to your first comment until now. It appears that you now accept that this is a legitimate use case, and your only beef is that Viru didn't explicitly demonstrate in this post how an exiting app should clean up an event handler it has registered. That's not surprising, as this blog is mostly focused on code snippets rather than full-blown apps - we don't cover every caveat in every post. But it is a good suggestion for a future post - probably after we've finished with AU and our Developer Days conferences - and I'm sure Viru will address the specific point for this post now you've raised it (and once he returns from vacation).
Reply
09/25/2012 at 09:57 AM

---
**内容**: Virupaksha Aithal said in reply to Tony Tanzillo...
Thanks for the comments. I included a check for quit scenario. The modified code is now on the blog.
-Viru
Reply
09/27/2012 at 03:04 AM

---
