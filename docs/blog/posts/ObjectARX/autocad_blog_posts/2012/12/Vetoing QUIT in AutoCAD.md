---
title: "Vetoing QUIT in AutoCAD"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
description: "How can I veto quit in AutoCAD?"
author: Autodesk
---
# Vetoing QUIT in AutoCAD

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/vetoing-quit-in-autocad.html

## 文章内容

By Philippe Leefsma
Q:
How can I veto quit in AutoCAD?
A:
There are two situations to consider:
1) Subclass the AutoCAD main frame and watch for WM_CLOSE message. This message is generated when user tries to quit AutoCAD using any of the possible methods. In the sample, we veto the quitting of AutoCAD, but this can be modified to make changes in the documents, save them and then allow AutoCAD to quit. This way you can avoid the save dialog while quitting AutoCAD.
2) Using the event AcApDocManagerReactor::documentLockModeChanged() to trap the EXIT command that the user can issue at command prompt.
The attached arx sample implements both approaches.
ArxVetoQuit.zip

## 评论

**内容**: langshanglibie said...
Hi, Philippe Leefsma!
When I used the first method, and when I inputed "quit" at command prompt the second time,
//windows proc function
LRESULT CALLBACK fWndProc(HWND hwnd, UINT uMsg,WPARAM wParam,LPARAM lParam)
{
// Handle the WM_CLOSE message and return true to veto the message
// this stops AutoCAD from closing
if(uMsg == WM_CLOSE)
{
acutPrintf(L"\nQuit Canceled...");
return true;
}
// Send all the messages you receive to AutoCAD so they can be handled as normal
return ::CallWindowProc(wndProc,hwnd,uMsg,wParam,lParam);
}
I can't received the WM_CLOSE message, I saved the current document in commandWillStart() in my MyEditorReactor derived from AcEditorReactor. Why this happend?
Reply
09/10/2013 at 08:02 PM

---
**内容**: Philippe said in reply to langshanglibie...
Hi,
Sorry, so far I do not reproduce the behavior. I am testing under 2014. What version and platform are you using? Are you using the exact same code that is provided in the attachment? What does "commandWillStart" have to do with the workflow?
Reply
09/12/2013 at 07:30 AM

---
**内容**: langshanglibie said in reply to Philippe...
Thanks, Philippe!
I have resolved my problem using all my skills, experiences, and tricks.
Best wishes for you!
Reply
09/12/2013 at 06:01 PM

---
