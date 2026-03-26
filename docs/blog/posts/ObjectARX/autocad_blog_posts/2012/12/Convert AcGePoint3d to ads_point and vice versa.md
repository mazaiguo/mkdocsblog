---
title: "Convert AcGePoint3d to ads_point and vice versa"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "There is a function named 'asDblArray()' that casts AcGePoint3d to adspoint wherever it is necessary."
author: Autodesk
---
# Convert AcGePoint3d to ads_point and vice versa

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/convert-acgepoint3d-to-ads_point-and-vice-versa.html

## 文章内容

By Gopinath Taget
There is a function named 'asDblArray()' that casts AcGePoint3d to ads_point wherever it is necessary.
The following sample code demonstrates this:
#include "geassign.h"
AcGePoint3d pt;
acedGetPoint (NULL, L"Get a point: ",asDblArray (pt)) ;
If you want to convert from ads_point to AcGePoint3d, use its complimenting function, 'asPnt3d()'.

