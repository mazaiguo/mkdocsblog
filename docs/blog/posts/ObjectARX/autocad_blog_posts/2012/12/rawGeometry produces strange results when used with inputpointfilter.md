---
title: "rawGeometry produces strange results when used with inputpointfilter"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
description: "If you have ever used the input point monitor to draw temporary graphics, you might wonder why you get strange results while using AcGiCommonDraw::..."
author: Autodesk
---
# rawGeometry produces strange results when used with inputpointfilter

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/rawgeometry-produces-strange-results-when-used-with-inputpointfilter.html

## 文章内容

By Gopinath Taget
If you have ever used the input point monitor to draw temporary graphics, you might wonder why you get strange results while using AcGiCommonDraw::rawGeometry() to draw temporary graphics in the processInputPoint() function of your class derived from AcEdInputPointFilter.
The reason is, the input point API is not intended to be used with AcGiCommonDraw interface. You should use AcGiWorldDraw or AcGiViewportDraw instead. If you want to abstract out AcGiWorldDraw or AcGiViewportDraw methods with similar function/method signatures for code elegance, one approach is to create utility functions that make use of C++ templates. Something like this:
template <class T>
void drawACircle(T* pDrawGeometry)
{  
 // doesn't matter here if 'T' is an  
 // AcGiWorldDraw or AcGiCommonDraw  
 //  
pDrawGeometry->circle(....);
}
You can use AcGiCommonDraw in any other API without problem (in the worldDraw function of a custom entity, for example).

