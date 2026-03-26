---
title: "Custom entity support for the fillet command"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
description: "Assume a custom entity (MyLine) derives from AcDbCurve and draws lines in subWorlddraw. An ARX command creates two MyLine.  When you run FILLET  co..."
author: Autodesk
---
# Custom entity support for the fillet command

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/custom-entity-support-for-the-fillet-command.html

## 文章内容

By Xiaodong Liang
Assume a custom entity (MyLine) derives from AcDbCurve and draws lines in subWorlddraw. An ARX command creates two MyLine.  When you run FILLET  command, it will pop out
Fillet requires 2 lines, arcs, or circles.
The problem is that when the FILLET command is invoked, the entire implementation is bypassed and not used.
The workaround is to derive native AutoCAD entities
that are based on AcDbCurve. For example, you can derive from AcDbLine so your custom line will automatically support the FILLET command.
  There is one more issue. After FILLET command, the two custom lines are filleted. However the lines are not trimmed. This used to work in 2002.
The workaround is custom line classes can implement their own extend() method to override the one in AcDbInternalLine and get AutoCAD’s behavior 
MyLine.h:
 virtual Acad::ErrorStatus extend(double newParam);
MyLine.cpp:
Acad::ErrorStatus CMyLine::extend(double param)
{
    assertWriteEnabled();
    AcGePoint3d startPnt(startPoint()),
                endPnt(endPoint());
      double norm = startPnt.distanceTo(endPnt);
    AcGeLine3d geLine (startPnt, endPnt);
    AcGePointOnCurve3d ponc(geLine);
    if (param > 0.0)
        setEndPoint(ponc.point(param / norm));
    else
        setStartPoint(ponc.point(param / norm));
    return Acad::eOk;
  }
By this method, the result is as expected:

