---
title: "How to control an Entity viewportDraw so that it always displays a Plan view using ObjectARX?"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C++
  - ObjectARX
  - Unicode
description: "Using ObjectARX to create and define a Custom Entity type you can implement Viewport specific draw functionality, amongst other things. The same ca..."
author: Autodesk
---
# How to control an Entity viewportDraw so that it always displays a Plan view using ObjectARX?

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/how-to-control-an-entity-viewportdraw-so-that-it-always-displays-a-plan-view-using-objectarx.html

## 文章内容

by Fenton Webb
Using ObjectARX to create and define a Custom Entity type you can implement Viewport specific draw functionality, amongst other things. The same can also be achieved with .NET Overrules which is really cool. A common question we get from developers is, how can I make my custom entity Text follow the same direction as the View, in other words, plan to the View.
Here’s how…
void drawTextPlanView(AcGiViewportDraw* pVd,
                        AcGePoint3d insPnt, TCHAR *textStr)
{
  // get the current viewport
  AcGiViewport* pView = &pVd->viewport();
  AcGePoint3d cam, tar;
  // work out the viewing properties
  pView->getCameraLocation(cam);
  pView->getCameraTarget(tar);
  // now calc the normal vector
  AcGeVector3d normal = cam - tar;
  normal.normalize();
    // finally draw the text in the viewport
  AcGiTextStyle giStyle;
  fromAcDbTextStyle(giStyle, curDoc()->database()->textstyle());
  AcGeVector3d dir = insPnt.asVector().crossProduct(normal);
  dir.y = 0;
  pVd->geometry().text(insPnt, normal, dir,
    textStr, _tcslen(textStr), Adesk::kFalse, giStyle);
}

