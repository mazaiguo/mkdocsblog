---
title: "Find an entity under the cursor position using Win32 and ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Selection
description: "How do I find the entity under the cursor position using raw Win32?"
author: Autodesk
---
# Find an entity under the cursor position using Win32 and ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/find-an-entity-under-the-cursor-position-using-win32-and-objectarx.html

## 文章内容

By Fenton Webb
Issue
How do I find the entity under the cursor position using raw Win32?
Solution
The best way to find the entity under the cursor/crosshair is to use the AcEdInputPointMonitor class. However, if you must find the entity under the cursor using raw Win32, here’s how…
First, to catch a mouse event before any "normal" AutoCAD's action (such as, pressing mouse down/up) takes place, you can register your own event-handling function, using acedRegisterFilterWinMsg(). ObjectARX 2008 SDK comes with a good sample about this (objectarx\samples\editor\mfcsamps\pretranslate). Please refer it for the detail about capturing AutoCAD Window's messaging.
Secondly, in the actual event-handling function of your own, you can use acedSSGet() with the option "_:E" (select everything within the cursor's object selection pickbox option). By specifying only the first point, you can make a selection window as the same as the cursor position.
The following code defines a function that you can register with acedRegisterFilterWinMsg(). To test this code, simply replace the function named FilterMouse() in the sample project (\objectarx\samples\editor\mfcsamps\pretranslate) with the following one.
BOOL filterMouse(MSG *pMsg)
{
 if( pMsg->message == WM_MOUSEMOVE   || 
  pMsg->message == WM_LBUTTONDOWN || pMsg->message == WM_LBUTTONUP ) {
  acedDwgPoint cpt={ 0, 0, 0 };
  CPoint cPnt(pMsg->lParam);
  acedCoordFromPixelToWorld(cPnt, cpt) ;
  ads_point pt={ cpt[X], cpt[Y], 0 } ;
  ads_name ss;
  acedSSGet(L"_:E", pt, NULL, NULL, ss) ;
  long len =0 ;
  acedSSLength(ss, &len) ;
  acutPrintf(L"\nThe ss length is %d", len) ;
  acedSSFree(ss) ;
  if ( pMsg->message == WM_LBUTTONDOWN || pMsg->message == WM_LBUTTONUP )
   unmouse ();
 }
 return (FALSE) ; //----- continue
}

