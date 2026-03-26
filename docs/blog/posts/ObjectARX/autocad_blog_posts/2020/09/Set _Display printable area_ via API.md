---
title: "Set "Display printable area" via API"
date: 2020-09-01
categories:
  - AutoCAD
tags:
  - API
  - Plot
description: "When you make a new Layout a new Page Setup called Layout1"
author: Autodesk
---
# Set "Display printable area" via API

发布日期: 2020-09-01

原始链接: https://adndevblog.typepad.com/autocad/2020/09/set-display-printable-area-via-api.html

## 文章内容

By Madhukar Moogala
When you make a new Layout a new Page Setup called *Layout1*
You see the printable area in Layout. This is a dashed rectangle.
In order to remove that rectangles you set the option via UI:
Go to TOOLS > OPTIONS > DISPLAY > LAYOUT  ELEMENTS > Uncheck "Display printable area"
or to do the same in API

void turnOffPrintableArea() 
{

  AcApLayoutManager* pApLayoutMgr =
  (AcApLayoutManager*)acdbHostApplicationServices()->layoutManager();
 if (pApLayoutMgr != NULL) {
        pApLayoutMgr->setShowPaperMargins(false);
        pApLayoutMgr->updateCurrentPaper();
 }
}
Unfortunately, the interface AcApLayoutManager for application-specific routines that manipulate, access AcDbLayout objects and controls layout related GUI attributes is not exposed to NET.

