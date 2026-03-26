---
title: "How to react to the cursor keys properly (without affecting AutoCAD) using ObjectARX?"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - ObjectARX
description: "With ObjectARX you can add a filter function into the AutoCAD's Windows message loop (you can also PInvoke this functionality in .NET too)."
author: Autodesk
---
# How to react to the cursor keys properly (without affecting AutoCAD) using ObjectARX?

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/how-to-react-to-the-cursor-keys-properly-without-affecting-autocad-using-objectarx.html

## 文章内容

by Fenton Webb
With ObjectARX you can add a filter function into the AutoCAD's Windows message loop (you can also PInvoke this functionality in .NET too).
The following example shows how to trap and filter out the cursor keys allowing your application to respond to the keys, rather than let the command line editor do it (return TRUE from the filterCurs()). It uses acedRegisterFilterWinMsg() to register a windows hook, and acedRemoveFilterWinMsg() to unregister the hook...
#include "rxmfcapi.h"
  // After a call of this function AutoCAD will use filterCurs() function
// to process key presses.
//------------------------------------------------------------------------
void curskeys()
{
  if( TRUE == cursDone ) // already has the hook??
    return;
  acutPrintf( _T("Cursor filtering enabled...\n") );
  if( FALSE == acedRegisterFilterWinMsg( filterCurs ) )
    acutPrintf( _T("Can't register Windows cursor-key msg hook\n"));
  else
    cursDone = TRUE;
}
  static BOOL cursDone = FALSE;
// Stop using filterCurs() for processing key presses
//------------------------------------------------------------------
void nocurskeys()
{
  if( TRUE == cursDone )
  {
    acedRemoveFilterWinMsg( filterCurs );
    cursDone = FALSE;
  }
}
// In this function your application can control presses of particular keys
// or let AutoCAD do it.
//------------------------------------------------------------------------------
BOOL filterCurs( MSG *pMsg )
{
  if( WM_KEYDOWN == pMsg->message && pMsg->wParam >= 37 && pMsg->wParam <= 40 )
  {
    switch( pMsg->wParam )
    {
    case 37: // left
      acutPrintf( _T("Left\n") );
      break;
    case 38: // up
      acutPrintf( _T("Up\n") );
      break;
    case 39: // right
      acutPrintf( _T("Right\n") );
      break;
    case 40: // down
      acutPrintf( _T("Down\n") );
      break;
    }
    return TRUE; // filter message
  }
  return FALSE;
}

## 评论

**内容**: Gaetano said...
With AutoCAD 2014 and 2012 the string is without "\n" at the end each line. It is a unique concatenated string. Is it a way to have the same as in the command line window?
Gaetano
Reply
05/27/2013 at 09:14 AM

---
**内容**: alexb said...
Hi,
I have this program which filters F-key presses by subclassing the Acad window. It worked in A2004 and A2008.
In A2012 it works except for the F3 and F6 keys.
Does Acad treat those keys differently?
(I tried the recommended method above too, with the same results.)
Also, when using subclassing, we had the option of calling the original WNDPROC several times with different parameters.
How is it done using acedRegisterFilterWinMsg()?
Thanks,
alex
Reply
03/16/2014 at 11:21 AM

---
