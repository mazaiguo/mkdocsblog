---
title: "Draw text *exactly* in the center of a Circle using ObjectARX"
date: 2012-09-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Unicode
description: "If you have a custom entity and you are trying to draw some text (from within your worldDraw or viewportDraw) exactly in the center of a circle (no..."
author: Autodesk
---
# Draw text *exactly* in the center of a Circle using ObjectARX

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/draw-text-exactly-in-the-center-of-a-circle-using-objectarx.html

## 文章内容

by Fenton Webb
If you have a custom entity and you are trying to draw some text (from within your worldDraw or viewportDraw) exactly in the center of a circle (not slightly off), maybe for a label or something similar, you may be having problems because of the font width depending on the character you are using.
Here’s some code that should solve your problem…
{
AcGiTextStyle style;
// get the text style
Acad::ErrorStatus es = fromAcDbTextStyle(style, "Standard");
style.loadStyleRec();
// if ok
if (es == Acad::eOk)
{
   // setup the text
   const char *text = "1";
   int length = -1;
   // find out the extents
   AcGePoint2d extMax,extMin;
   if (Acad::eOk==style.extentsBox(text, false, length, false,extMin,extMax))
   {
     // work out the insertion point
     AcGePoint3d insertionPnt = center() - AcGeVector3d((extMin.x+ extMax.x)/2.0, (extMin.y + extMax.y)/2.0, 0);
  vport_draw->geometry().text(insertionPnt, AcGeVector3d::kZAxis, AcGeVector3d::kXAxis, text, length, true, style);
   }
  }
}

## 评论

**内容**: petcon said...
how about acedTextBox ?
Reply
09/14/2012 at 09:51 PM

---
**内容**: Fenton Webb said...
Hey Petcon
we can't use acedTextBox in a custom entity because DBX DLLs are not dependent on acad.exe/accore.dll (they need to also work in DWGTrueview, Revit, Inventor, etc
Reply
09/17/2012 at 10:14 AM

---
