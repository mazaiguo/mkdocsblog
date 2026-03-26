---
title: "Setting the Wait Cursor type using ObjectARX and Win32"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "Sometimes, you want to tell the user that your application is busy and what better way to do that then with an Hour Glass wait cursor… Obviously, y..."
author: Autodesk
---
# Setting the Wait Cursor type using ObjectARX and Win32

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/setting-the-wait-cursor-type-using-objectarx-and-win32.html

## 文章内容

by Fenton Webb
Sometimes, you want to tell the user that your application is busy and what better way to do that then with an Hour Glass wait cursor… Obviously, you can create your own custom cursor and display it using the same technique…
Here’s how:
//////////////////////////////////////////////////////////////////////////
static HHOOK MyHook;
static HCURSOR hWaitCursor;
//////////////////////////////////////////////////////////////////////////
static LRESULT CALLBACK MyMsgProc (int nCode, WPARAM wParam, LPARAM lParam);
//////////////////////////////////////////////////////////////////////////
// This is command 'WAITCURSOR, by Fenton Webb [14/10/2004], DevTech, Autodesk
void asdkWaitCursor()
{
  // load the Wait cursor
  hWaitCursor = LoadCursor(NULL, IDC_WAIT);  
  // and set it
  HCURSOR hCursor = SetCursor(hWaitCursor); 
    // now set a hook so we can constantly keep our cursor set
  MyHook = SetWindowsHookEx(WH_CALLWNDPROCRET, (HOOKPROC)MyMsgProc, (HINSTANCE)
 NULL, GetCurrentThreadId ()); 
  // now do the wait intensive task...
  ACHAR cResult [256];
  acedGetString (0, _T("\nPretending to wait : "), cResult); 
    // and finally clean up
  UnhookWindowsHookEx (MyHook) ;
    SetCursor (hCursor) ;
}
//////////////////////////////////////////////////////////////////////////
LRESULT CALLBACK MyMsgProc (int nCode, WPARAM wParam, LPARAM lParam)
{
  // forward the other hook calls
  if ( nCode < 0 ) 
    return (CallNextHookEx(MyHook, nCode, wParam, lParam)); 
    LRESULT ret = CallNextHookEx(MyHook, nCode, wParam, lParam);
    // keep updating our cursor type
  SetCursor (hWaitCursor); 
    return (ret) ;
}

## 评论

**内容**: Patrick EMIN said...
I don't understand how the cursor looks; is it a Windows type cursor or a custom image?
Reply
06/09/2012 at 02:09 AM

---
**内容**: Account Deleted said in reply to Patrick EMIN...
It is a windows type cursor: http://msdn.microsoft.com/en-us/library/windows/desktop/ms648391%28v=vs.85%29.aspx
Reply
06/09/2012 at 01:59 PM

---
**内容**: Martin said...
Is there a .net version of this?
Cheers,
Martin.
Reply
06/11/2012 at 03:29 PM

---
**内容**: Account Deleted said in reply to Martin...
As usually with help of P/Invoke http://support.microsoft.com/kb/318804/en-us it is possible: http://support.microsoft.com/kb/318804/en-us
Reply
06/12/2012 at 02:15 PM

---
