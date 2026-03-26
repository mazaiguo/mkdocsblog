---
title: "Drawing/erasing temporary graphics with acedGrDraw"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "You can use acedGrDraw to Drawing/erasing temporary graphics. below code shows drawing a color vector and eraing the same. Code also shows the draw..."
author: Autodesk
---
# Drawing/erasing temporary graphics with acedGrDraw

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/drawingerasing-temporary-graphics-with-acedgrdraw.html

## 文章内容

By Virupaksha Aithal
You can use acedGrDraw to Drawing/erasing temporary graphics. below code shows drawing a color vector and eraing the same. Code also shows the drawing of XOR vector (by passing color as -1)
void acedGrDrawTest(void)
{
int result = 0;
//draw color line
acedGrDraw (asDblArray (AcGePoint3d (0,0,0)),
            asDblArray (AcGePoint3d (100,100,0)), 5, 0);
  // get user input
acedGetInt (_T("\nPress to erase blue line"), &result);
// now erase it
acedGrDraw (asDblArray (AcGePoint3d (0,0,0)), asDblArray
                        (AcGePoint3d (100,100,0)), 0, 0);
  // get user input again
acedGetInt (_T("\nPress to draw in XOR ink"), &result);
// create a line in -1 XOR ink 
acedGrDraw (asDblArray (AcGePoint3d (0,0,0)), asDblArray
                        (AcGePoint3d (100,100,0)), -1, 0);
  // get user input again
acedGetInt (_T("\nPress to erase XOR ink"), &result);
// erase XOR ink
acedGrDraw (asDblArray (AcGePoint3d (0,0,0)),
            asDblArray (AcGePoint3d (100,100,0)), -1, 0);
}

