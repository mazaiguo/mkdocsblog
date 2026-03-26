---
title: "About TDUSRTIMER and AcDbDate"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "The TDUSRTIMER system variable does not store the elapsed milliseconds, but instead stores the time elapsed form the last reset in a Julian date fo..."
author: Autodesk
---
# About TDUSRTIMER and AcDbDate

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/about-tdusrtimer-and-acdbdate.html

## 文章内容

By Augusto Goncalves
The TDUSRTIMER system variable does not store the elapsed milliseconds, but instead stores the time elapsed form the last reset in a Julian date format. The easiest way to get the time elapsed in seconds is to use the AcDbDate class.
void ASDKgetTime()
{
  struct resbuf rUsrTime;
  acedGetVar(_T("TDUSRTIMER"), &rUsrTime);
    AcDbDate testDate ;
  testDate.setJulianFraction(rUsrTime.resval.rreal) ;
    acutPrintf (
    _T("\nMinute: %d\nSec: %d\nMilisec: %d"),
    testDate.minute (),
    testDate.second (),
    testDate.millisecond ()) ;
}

