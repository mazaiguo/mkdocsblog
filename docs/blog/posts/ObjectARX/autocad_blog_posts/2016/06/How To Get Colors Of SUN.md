---
title: "How To Get Colors Of SUN"
date: 2016-06-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
  - ObjectARX
  - Palette
description: "The colour of SUN is calculated algorithmically based on geographic location and date \time of that day."
author: Autodesk
---
# How To Get Colors Of SUN

发布日期: 2016-06-01

原始链接: https://adndevblog.typepad.com/autocad/2016/06/how-to-get-colors-of-sun.html

## 文章内容

By Madhukar Moogala
The colour of SUN is calculated algorithmically based on geographic location and date \time of that day.
With ObjectARX 2017, we have an API to get color same as that appear on Sun properties palette.
The code is self explanatory.
The API may come of us, if users want to create an artificial light want to set same as sun colour with going much complexity of calculation colour values.
  static void sunColor(void)
  {
  /*make sure is SUN enabled */
  /*Set SUNSTATUS to 1*/
  AcDbObjectId curVportId = AcDbObjectId::kNull;
  curVportId = acedActiveViewportId();
   struct resbuf rb;
  int rt = acedGetVar(_T("CVPORT"), &rb);
  if (rt != RTNORM)
  {
  acutPrintf(_T("\nError acquiring sysvar \"CVPORT\" value."));
  return;
  }
  int vportNum = rb.resval.rint;
   AcDbObjectPointer<AcDbViewportTableRecord>
  curVTR(curVportId, AcDb::kForWrite);
  if (curVTR.openStatus() == Acad::eOk)
  {
   if (curVTR->sunId() != AcDbObjectId::kNull)
  {
   /*Sun enabled, try to get color of AutoCAD sun*/
  AcDbObjectPointer<AcDbSun> pSun(curVTR->sunId(), AcDb::kForRead);
  if (pSun.openStatus() == Acad::eOk)
  {
  const AcGiColorRGB& sunColor = pSun->sunColorPhotometric(1.0);
  double factor = 255.0;
  double r = sunColor.red * factor;
  double g = sunColor.green * factor;
  double b = sunColor.blue * factor;
   acutPrintf(_T("R[%f],G[%f],B[%f]"),r,g,b);
  pSun.close();
  }
  }
  curVTR.close();
  }
   }

