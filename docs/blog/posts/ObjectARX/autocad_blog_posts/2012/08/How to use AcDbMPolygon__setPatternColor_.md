---
title: "How to use AcDbMPolygon::setPatternColor?"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "When I use the following code snippet, the polygon is still white (as default entity color):"
author: Autodesk
---
# How to use AcDbMPolygon::setPatternColor?

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/how-to-use-acdbmpolygonsetpatterncolor.html

## 文章内容

By Philippe Leefsma
Q:
When I use the following code snippet, the polygon is still white (as default entity color):
AcCmColor acadcolor;
  acadcolor.setRed(20);
  acadcolor.setGreen(50);
  acadcolor.setBlue(110);
  AcDbMPolygon *pAcDb = new AcDbMPolygon();
  pAcDb->appendMPolygonLoop(points, bulges, false); //append a loop
  pAcDb->hatch()->setPattern(AcDbHatch::kPreDefined, "SOLID");
  pAcDb->setPatternColor(acadcolor);
  //post to database and close..
  How do I set the color correctly?
A:
The first option is to call acadcolor.setColorMethod(AcCmEntityColor::kByColor) after you set Red, Green, Blue color.
The second option is to use setRGB() as shown:
acadcolor.setRGB(20,50,110);
After you use acadcolor properly, and then execute the LIST command, it displays the following:
Hatch pattern: SOLID
Fill color:  20,50,110

