---
title: "Equivalent to ObjectARX acdbDistF() in AutoCAD.NET"
date: 2013-02-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
description: "I just had one of those frustrating moments where I couldn’t find a function I wanted in .NET I knew what it was in ObjectARX, but not in .NET… Aft..."
author: Autodesk
---
# Equivalent to ObjectARX acdbDistF() in AutoCAD.NET

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/equivalent-to-objectarx-acdbdistf-in-autocadnet.html

## 文章内容

by Fenton Webb
I just had one of those frustrating moments where I couldn’t find a function I wanted in .NET I knew what it was in ObjectARX, but not in .NET… After what seemed hours (5 mins) I ended up searching the AutoCAD source and found it. Anyway, I thought I’d post it here for you guys (and Google) as a reference.
If you want to convert a decimal value to a string UNITS, then in ObjectARX the function is:
int acdbDisToF(const ACHAR * str, int unit, ads_real * v);
the equivalent function in AutoCAD.NET is
Autodesk.AutoCAD.Runtime.Converter.DistanceToString()

