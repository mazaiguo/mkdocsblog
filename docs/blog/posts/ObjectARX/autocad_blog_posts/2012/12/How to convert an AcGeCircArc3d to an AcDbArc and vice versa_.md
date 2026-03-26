---
title: "How to convert an AcGeCircArc3d to an AcDbArc and vice versa?"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
description: "The following ARX code does this:"
author: Autodesk
---
# How to convert an AcGeCircArc3d to an AcDbArc and vice versa?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-convert-an-acgecircarc3d-to-an-acdbarc-and-vice-versa.html

## 文章内容

By Gopinath Taget
The following ARX code does this:
void convertArc2Arc( AcGeCircArc3d*pGeArc, AcDbArc*&pDbArc )
{
AcGePoint3d center = pGeArc->center();
AcGeVector3d normal = pGeArc->normal();
AcGeVector3d refVec = pGeArc->refVec();
AcGePlane plane = AcGePlane(center, normal);
 double ang = refVec.angleOnPlane(plane);
pDbArc = new AcDbArc(center, normal,
  pGeArc->radius(),pGeArc->startAng() + ang,
  pGeArc->endAng() + ang );
}
  void convertArc2Arc( AcDbArc*pDbArc, AcGeCircArc3d*&pGeArc)
{
pGeArc = new AcGeCircArc3d(
pDbArc->center(),
pDbArc->normal(),
pDbArc->normal().perpVector(),
pDbArc->radius(),
pDbArc->startAngle(),
pDbArc->endAngle());
}

