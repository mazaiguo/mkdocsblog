---
title: "Balloon notification in statusbar tray item"
date: 2014-12-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Plugin
description: "ObjectARX 2004 SDK had this nice C++ sample on adding tray items to the status bar and displaying balloon notification in one of those tray items. ..."
author: Autodesk
---
# Balloon notification in statusbar tray item

发布日期: 2014-12-01

原始链接: https://adndevblog.typepad.com/autocad/2014/12/balloon-notification-in-statusbar-tray-item.html

## 文章内容

By Balaji Ramamoorthy
ObjectARX 2004 SDK had this nice C++ sample on adding tray items to the status bar and displaying balloon notification in one of those tray items. I have migrated this sample project to work on AutoCAD 2015 and you can download it here :
StatusBar
To build this sample, place it under \samples\editor folder in ObjectARX 2015 SDK path. Here is a sample code snippet to display balloon window from that sample :
 // Create the bubble notification message, and callbacks. 
 int  result;
 AcApDocument *pDoc=acDocManager->curDocument();
   CString strMsg(_T(" Notification" ));
   AcTrayItemBubbleWindowControl bwControl(
  "Attention!" , 
  strMsg, 
  "HyperText Here" , 
  "www.autodesk.com" );
   bwControl.SetIconType(
  AcTrayItemBubbleWindowControl::
  BUBBLE_WINDOW_ICON_INFORMATION);
   bwControl.SetCallback(BubbleWindowCallback, pDoc);
    result=trayItems[0]->ShowBubbleWindow(&bwControl);
  To control the time the balloon will be displayed, please run the "TRAYSETTINGS" command and set the display time.

## 评论

**内容**: khanh said...
thanks..
Reply
12/31/2020 at 12:38 AM

---
