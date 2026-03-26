---
title: "Obtain the Visual Style/Shademode of a Viewport using ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "Here’s a code snippet I use to get the Visual Style of a Viewport, mostly in my viewportDraw() callback… You have to obtain the Viewport object ID ..."
author: Autodesk
---
# Obtain the Visual Style/Shademode of a Viewport using ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/obtain-the-visual-styleshademode-of-a-viewport-using-objectarx.html

## 文章内容

By Fenton Webb
  Here’s a code snippet I use to get the Visual Style of a Viewport, mostly in my viewportDraw() callback… You have to obtain the Viewport object ID first, then use this code…
  // paper space checks
AcDbObjectPointer<AcDbViewport> viewportType(vpObjId, AcDb::kForRead);
if (viewportType.openStatus() == Acad::eOk)
{
   TCHAR *visualStyleName = NULL;
 AcDbDictUtil::getVisualStyleName(visualStyleName, viewportType->visualStyle());
 acutPrintf(_T("\nVisual Style = %s"), visualStyleName);
   // free up the string
   acutDelString(visualStyleName);
}
else
{
 // model space
 AcDbObjectPointer<AcDbViewportTableRecord> viewport(vpObjId, AcDb::kForRead);
 if (viewport.openStatus() == Acad::eOk)
{
    TCHAR *visualStyleName = NULL;
    AcDbDictUtil::getVisualStyleName(visualStyleName, viewport->visualStyle());
    acutPrintf(_T("\nVisual Style = %s"), visualStyleName);
       // free up the string
       acutDelString(visualStyleName);
}
 else
    acutPrintf(_T("\nVisual Style = 2dWireframe"));
}

