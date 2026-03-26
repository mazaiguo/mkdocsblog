---
title: "Zoom to a Window in Editor using CommandASync"
date: 2014-05-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
description: "In this post, I will illustrate a sample based on AutoCAD 2015 API Editor.CommandAsync."
author: Autodesk
---
# Zoom to a Window in Editor using CommandASync

发布日期: 2014-05-01

原始链接: https://adndevblog.typepad.com/autocad/2014/05/zoom-to-a-window-in-editor-using-commandasync.html

## 文章内容

By Madhukar Moogala
In this post, I will illustrate a sample based on AutoCAD 2015 API Editor.CommandAsync.
Problem: Can I zoom to particular window in an Editor as long as I press esc or cancel to quit?
Answer: Yes, with help of CommandAsync, you can achieve this task.
#region "send Zoom command by callback function"
private static bool ZoomExit = false;
//declare the callback delegation
delegate void Del();
private static Del _actionCompletedDelegate;
// Exit function，check if Zoom command is esc\cancelled
static void
MdiActiveDocument_CommandCancelled(object sender,CommandEventArgs e)
{
    ZoomExit = true;
}
[CommandMethod("TestZoom")]
public static void TestZoom()
{
   var ed = Application.DocumentManager.MdiActiveDocument.Editor;
   var doc = Application.DocumentManager.MdiActiveDocument;
   //esc event
   doc.CommandCancelled += MdiActiveDocument_CommandCancelled;
   // start Zoom command
   Editor.CommandResult cmdResult1 =
   ed.CommandAsync(new object[]{
   "_.ZOOM", Editor.PauseToken, Editor.PauseToken});
   // delegate callback function, wait for interaction ends
   _actionCompletedDelegate = new Del(CreateZoomAsyncCallback);
   cmdResult1.OnCompleted(new Action(_actionCompletedDelegate));
   ZoomExit = false;
}
// callback function
public static void CreateZoomAsyncCallback()
{
    var ed = Application.DocumentManager.MdiActiveDocument.Editor;
    //if Zoom command is running
    if (!ZoomExit)
    {
        // AutoCAD hands over to the callback function
        Editor.CommandResult cmdResult1 =
        ed.CommandAsync(new object[]{
        "_.ZOOM", Editor.PauseToken, Editor.PauseToken});
        // delegate callback function, wait for interaction ends
        _actionCompletedDelegate = new Del(CreateZoomAsyncCallback);
       cmdResult1.OnCompleted(new Action(_actionCompletedDelegate));
    }
    else
    {
        ed.WriteMessage("Zoom Exit");
        return;
    }
}
#endregion

## 评论

**内容**: Alexander Rivilis said...
Hi Madhukar!
All code is broken because of trimming spaces. Please repost it.
Reply
05/15/2014 at 12:09 PM

---
**内容**: Madhukar Moogala said in reply to Alexander Rivilis...
Hi Alex,
Sorry for the trouble, can you check now ?
Reply
05/15/2014 at 10:53 PM

---
**内容**: Alexander Rivilis said in reply to Madhukar Moogala...
Now it is OK. Thanks!
Reply
05/16/2014 at 03:01 AM

---
**内容**: Vaidas Velutis said...
i am getting eNotAplicable with this code, mayby someone knows why :)
Reply
09/10/2014 at 12:34 AM

---
