---
title: "What are AcDbCurve/Curve Parameters? ObjectARX/.NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C++
  - ObjectARX
  - Polyline
description: "Please can you explain what Parameters are?"
author: Autodesk
---
# What are AcDbCurve/Curve Parameters? ObjectARX/.NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/what-are-acdbcurvecurve-parameters-objectarxnet.html

## 文章内容

By Philippe Leefsma
Please can you explain what Parameters are?
In simple terms, the parameter of a curve defines a 0-n floating point value indicating point positions on a curve.
Lets use a polyline as an example of what to expect from a parameter value.
If we have a polyline which has 5 points, and each of the 4 lines are different in length. If we call AcDbCurve::getStartParam() we will be returned a value of 0, if we call AcDbCurve::getEndParam() we will get a value of 4, if we extract the 2nd polyline point and call AcDbCurve::getParamAt() we will be returned a parameter value of 1. So you can see that in the case of a polyline, the parameter values directly represent each of the start and end points of the Polyline.
Parameters are very powerful, for instance, I can extract the halfway point between p1 and p2 by calling AcDbCurve::getPointAtParam(0.5) or the third of a distance between p3 and p4 by calling AcDbCurve::getPointAtParam(2.33333).
Another point to mention is that parameter values, although define a 0-n floating point value indicating point positions on a curve, are designed to best fit the needs of the curve being implemented. For example, the polyline example above uses parameter values as start and end point positions, this is a very efficient way to use parameters for a polyline and indeed makes logical sense, but for a circle the parameter values correspond to a radian increment around the circle. So, for a polyline the parameter value is non-uniform whereas the circle uses a uniform parameter value.

## 评论

**内容**: Owen Wengerd said...
It is not correct to assume that the parameter of a "halfway point" is the average of the two endpoint parameters. The mapping between parameters and points is entirely up to the implementor, and it could just as well be a logarithmic or other non-linear mapping. The correct way to get a "halfway point" is to use getDistAtParam to get the distances (say d1 and d2) at both parameters, then getPointAtDist to get the parameter at (d1 + d2 / 2.0).
Reply
05/17/2012 at 04:45 PM

---
**内容**: petcon said...
this is FAQ from most beginners.
it is a great explaination.
i think getPointAtParam(0.5) just means get the mid p between first p and second p
Reply
05/17/2012 at 10:04 PM

---
**内容**: Account Deleted said in reply to petcon...
What about circle (AcDbCircle), spline (AcDbSpline), ellipse (AcDbEllipse)?
What about ray (AcDbRay) and xline (AcDbXline)?
In the general case getPointAtParam(0.5) is not middle point between first point and second point.
Reply
05/18/2012 at 02:46 AM

---
