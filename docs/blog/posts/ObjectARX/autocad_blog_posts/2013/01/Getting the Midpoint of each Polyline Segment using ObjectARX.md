---
title: "Getting the Midpoint of each Polyline Segment using ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Plot
  - Polyline
description: "An AcDbPolyline is derived from AcDbCurve, a curve uses Parameter values to define its geometry. For a Polyline, the Parameter start value is 0 and..."
author: Autodesk
---
# Getting the Midpoint of each Polyline Segment using ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/getting-the-midpoint-of-each-polyline-segment-using-objectarx.html

## 文章内容

By Fenton Webb
An AcDbPolyline is derived from AcDbCurve, a curve uses Parameter values to define its geometry. For a Polyline, the Parameter start value is 0 and the end parameter is the total number of vertices –1. Those parameter values can be utilized to quickly and easily work out mid points, like this:
Acad::ErrorStatus getMidPointOnEachSegOfCrv(AcDbCurve *pCurve)
{
  if(!pCurve->isKindOf(AcDbCurve::desc()))
  {
    acutPrintf(L"\nSelected entity is not a CURVE derived object");
    return Acad::eInvalidInput;
  }
    Acad::ErrorStatus es;
  double startParam, endParam;
  // get the start param, usually it starts at 0 or 1
  es = pCurve->getStartParam( startParam );
  acutPrintf(L"\nstartParam is %fl", startParam);
    // get the end param, for a polyline it's the total number of
  // vertex's -1
  es =  pCurve->getEndParam( endParam );
  acutPrintf(L"\nendParam is %fl", endParam);
  // now loop the parameters, adding 1.0 each iteration
  for(double i=startParam; i<=endParam; ++i)
  {
    AcGePoint3d pt;
    es = pCurve->getPointAtParam(i+.5, pt);
    if (es == Acad::eOk)
      acutPrintf(L"\n%f,%f,%f", pt[0], pt[1], pt[2]);
  }
    return Acad::eOk;
}

## 评论

**内容**: Owen Wengerd said...
Oh no, et tu Fenton!? Your code violates the central tenet of parameterized curves: that parameters are *opaque* and you should *make no assumptions* about them. Please, in the name of all that is good and holy, fix this abomination that you have posted by using the "dist" functions as designed and intended.
Reply
01/07/2013 at 04:36 PM

---
**内容**: Fenton Webb said...
Hey Owen!
feel free to correct it as you see fit! I like to bend the rules, myself.
Reply
01/07/2013 at 04:38 PM

---
**内容**: Owen Wengerd said in reply to Fenton Webb...
Hmm, you are a stubborn one. I guess I need to break out the big guns and blog my old QuirkyPolyline sample.
Reply
01/07/2013 at 04:57 PM

---
**内容**: Owen Wengerd said in reply to Fenton Webb...
QuirkyPolyline exposes the error of your ways: http://otb.manusoft.com/2013/01/quirkypolyline-exposing-foolish-programmers.htm
Reply
02/05/2013 at 10:23 PM

---
**内容**: Alexander Rivlis said...
Hi, Fenton!
Please, double check your's code:
for(double i=startParam; i<=endParam; ++i)
{
AcGePoint3d pt;
es = pCurve->getPointAtParam(startParam+.5, pt);
if (es == Acad::eOk)
acutPrintf(L"\n%f,%f,%f", pt[0], pt[1], pt[2]);
}
Maybe:
es = pCurve->getPointAtParam(i+.5, pt);
Reply
01/08/2013 at 03:40 AM

---
**内容**: Fenton Webb said...
Hey Owen!
that's really good content, thanks for that.
Reply
02/06/2013 at 10:50 AM

---
