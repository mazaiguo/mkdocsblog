---
title: "How to calculate the length of an entity in ObjectArx/.NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C++
  - ObjectARX
description: "You can use the getStartParam() and getEndParam() to obtain the start and end parameters of the Curve based entity and then use GetDistanceAtParame..."
author: Autodesk
---
# How to calculate the length of an entity in ObjectArx/.NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-calculate-the-length-of-an-entity-in-objectarxnet.html

## 文章内容

By Gopinath Taget
You can use the getStartParam() and getEndParam() to obtain the start and end parameters of the Curve based entity and then use GetDistanceAtParameter() method to get the length of the Spline. Please find the code below which will calculate the Length of the Spline.
Acad::ErrorStatus es;
ads_name ename;
ads_point pt;
  if (RTNORM != acedEntSel(NULL, ename, pt))
{
    return;
}
AcDbObjectId objid;
acdbGetObjectId(objid, ename);
AcDbCurve* pEnt;
acdbOpenObject(pEnt, objid, AcDb::kForRead);
  double startParam, endParam, startDist, endDist;
es = pEnt->getStartParam(startParam);
es = pEnt->getEndParam(endParam);
es = pEnt->getDistAtParam(startParam, startDist);
es = pEnt->getDistAtParam(endParam, endDist);
acutPrintf(L"\nLength = %f", endDist - startDist);
Also in .Net, you can use the something like this to get the entity length.
a = curve.StartParam
b = curve.EndParam
length = curve.GetDistanceAtParameter(b) -
    curve.GetDistanceAtParameter(a)

## 评论

**内容**: petcon said...
there is a huge mistake in the arx code
everytime use acdbOpenObject PLEASE CHECK the return VALUE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Reply
05/16/2012 at 09:46 PM

---
**内容**: Gopinath Taget said...
Hi Petcon,
I am guessing acdbOpenObject caused you some heart burn. I sympathise. Programming is hard.
The point of the code above was to convey how to determine the length of a curve based entity and in that context the mistake you point to does not seem all that huge.
Bullet proof code makes for some very unreadable prose and this leads to some reluctant compromises in favor of simplicity and readability.
But I can always strive better.
Cheers
Gopinath
Reply
05/16/2012 at 10:22 PM

---
**内容**: petcon said...
fine. for readable.
Reply
05/17/2012 at 03:29 AM

---
**内容**: Omar said...
Gig like
Reply
05/07/2014 at 12:08 AM

---
**内容**: Omar said...
Big Like
Reply
05/07/2014 at 12:09 AM

---
