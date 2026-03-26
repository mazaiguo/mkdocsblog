---
title: "AcDbPolyline::getSplitCurves() only adds new vertices in some cases"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - Polyline
description: "I am having a problem with the AcDbPolyline::getSplitCurves() function. The function is returning a set of entities which is incorrect for the inpu..."
author: Autodesk
---
# AcDbPolyline::getSplitCurves() only adds new vertices in some cases

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/acdbpolylinegetsplitcurves-only-adds-new-vertices-in-some-cases.html

## 文章内容

By Philippe Leefsma
Q:
I am having a problem with the AcDbPolyline::getSplitCurves() function. The function is returning a set of entities which is incorrect for the input provided. I call getSplitCurves() on a polyline with two points on the polyline, expecting to get two polylines returned. Instead of getting two polylines, I only get a copy of the original polyline that has two extra vertices added.
A:
The behavior of getSplitCurves() is affected by the order of the points in the AcGePoint3dArray. If the points are appended to the AcGePoint3dArray in the order that they would be if they were measured from the start point of the polyline then the expected behavior occurs. (two polylines are returned).  The following code snippet uses this approach. It finds the distance on the  curve from the start of the curve to the point, and then add the points to the array in the order of their distance from the start of the curve. 
...
 AcGePoint3d projpt;
 if ((es = pBoundary->getClosestPointTo(sp, projpt)) != Acad::eOk)
  return es;
   AcGePoint3d projpt2;
 if ((es = pBoundary->getClosestPointTo(pt2, projpt2)) != Acad::eOk)
        return es;
   double dist1;
 double dist2;
 es = pBoundary->getDistAtPoint(projpt, dist1);
 es = pBoundary->getDistAtPoint(projpt2, dist2);
 if (dist1 < dist2)
 {
  // first point is closer to the start point
  pts.append(projpt);
  pts.append(projpt2);
 }
 else{
  //second point is closer to the start point
  pts.append(projpt2);
  pts.append(projpt);
 }
    if ((es = pBoundary->getSplitCurves(pts, ents)) != Acad::eOk)
  return es;
...

## 评论

**内容**: bikelink said...
thanks ! i'm going crazy about this!
Reply
01/19/2016 at 09:20 AM

---
