---
title: "Converting Julian dates"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "The easiest way to convert a Julian date into day, month, year, hour and minutes format is to use of the AcDbDate class. Also, visit this post for ..."
author: Autodesk
---
# Converting Julian dates

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/converting-julian-dates.html

## 文章内容

By Augusto Goncalves
The easiest way to convert a Julian date into day, month, year, hour and minutes format is to use of the AcDbDate class. Also, visit this post for more information.
struct resbuf rDate;
double time, fpart, ipart;
acedGetVar(_T("DATE"), &rDate);
time = rDate.resval.rreal;
fpart = modf (time, &ipart);
  AcDbDate testDate;
testDate.setJulianFraction(fpart);
acutPrintf(_T("\nMinute: %d\nSec: %d\nMilisec: %d"),
  testDate.minute (),
  testDate.second (),
  testDate.millisecond ());

