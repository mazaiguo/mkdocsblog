---
title: "How to give back UI focus during lengthy calculations (ObjectARX)"
date: 2012-09-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Database
  - ObjectARX
description: "I have a large arx application which performs lengthy calculations. When the calculation is running, our clients would normally minimize the AutoCA..."
author: Autodesk
---
# How to give back UI focus during lengthy calculations (ObjectARX)

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/how-to-give-back-ui-focus-during-lengthy-calculations-objectarx.html

## 文章内容

By Philippe Leefsma
Q:
I have a large arx application which performs lengthy calculations. When the calculation is running, our clients would normally minimize the AutoCAD window down to the task bar (it can run for days). Occasionally, in order to monitor progress, the AutoCAD window is maximized but the screen within the window is not refreshed. How can I workaround this?
A:
There are a couple of ways to do what you want.
The first way is multi-threading. I will say that multi-threading isn't recommended because it can have undesirable effects, especially when dealing with the AutoCAD drawing database, and is unsupported.
The second way is to implement your own Command Message Handler - recommended. When your program is executing it takes away the Message handling control from AutoCAD. Because of this when you minimize and maximize the AutoCAD window nothing gets repainted or updated because AutoCAD doesn't get the relevant messages that are sent from the operating system. So, what we need to do is to grab these messages in our 'calculation' loop and then spend some of our calculation time posting them back to AutoCAD and waiting for AutoCAD to process them.
// get the AutoCAD CWinApp class
CWinApp *app = acedGetAcadWinApp();
  // get the Main window
CWnd *wnd = app->GetMainWnd ();
  // loop round while we have stuff to do
while (!acedUsrBrk ())
{
    ++count;
       // now we have to add our own DispatchMessage handler because our loop
    // will stop autocad's one from processing
    //
    // dispatch incoming sent messages, check the thread message queue for
    // a posted message, and retrieve the message (if any exist).
    MSG msg;  
    while (::PeekMessage (&msg, wnd->m_hWnd, 0, 0, PM_NOREMOVE))
    {
        // check to see if we can pump the messages round
        if (!app->PumpMessage())
        {
             ::PostQuitMessage(0);
             break;
        }
    }
      LONG lIdle = 0;
      // let MFC do its idle processing
    while (app->OnIdle (lIdle++));
       //.... calculation code...
  }

## 评论

**内容**: Tony Tanzillo said...
acedUsrBrkWithMessagePump() seems to work well for me
Reply
09/24/2012 at 01:14 PM

---
