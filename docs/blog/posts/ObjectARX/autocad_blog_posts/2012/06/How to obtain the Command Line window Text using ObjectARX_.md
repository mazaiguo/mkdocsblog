---
title: "How to obtain the Command Line window Text using ObjectARX?"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - ObjectARX
  - Unicode
description: "The ObjectARX API includes a function acedGetAcadTextCmdLine() that gives you"
author: Autodesk
---
# How to obtain the Command Line window Text using ObjectARX?

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/how-to-obtain-the-command-line-window-text-using-objectarx.html

## 文章内容

by Fenton Webb
The ObjectARX API includes a function acedGetAcadTextCmdLine() that gives you
CWnd MFC access to the Command Line window. The Command Line window has various child CWnd windows (depending on the AutoCAD version you are running on) which we need to loop through to find the text, so just using normal Win32 we can very easily iterate through the child window list and extract the text.
Here’s how…
// get the command line CWnd container
CWnd* pDock = (CWnd*)acedGetAcadTextCmdLine();   
// get the child window
CWnd* pChild = pDock->GetWindow(GW_CHILD);   
// loop while we have children
while (pChild!=NULL)
{       
  CString str;       
  // get the window text
  pChild->GetWindowText(str);       
  // if we don't have any text
  if (str.GetLength() <= 0)
    pChild = pChild->GetNextWindow();   
  else
  {
    // display the text
    MessageBox(NULL, str);
    break;
  }
}

## 评论

**内容**: petcon said...
cool
Reply
06/03/2012 at 10:44 PM

---
**内容**: Artvegas said...
Hi Fenton,
I am trying to p/invoke this from .NET, but I get different handles depending on how I access the text window, as follows:
a) First I P/Invoked acedGetAcadTextCmdLine() as per this post, but no children are found.
b) Second I showed the text window (i.e. ran TEXTSCR) and then P/Invoked the user32 GetForegroundWindow() method. With this I could access the children as per your code.
Do you know why I get different window handle pointers?
Art
Reply
06/07/2012 at 10:05 AM

---
