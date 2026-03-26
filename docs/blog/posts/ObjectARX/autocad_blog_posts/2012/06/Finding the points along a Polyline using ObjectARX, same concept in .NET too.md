---
title: "Finding the points along a Polyline using ObjectARX, same concept in .NET too"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
  - Polyline
description: "Any Curve derived object inside of AutoCAD uses Parameter values to define significant parts of that Curve. These Parameter values are defined as d..."
author: Autodesk
---
# Finding the points along a Polyline using ObjectARX, same concept in .NET too

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/finding-the-points-along-a-polyline-using-objectarx-same-concept-in-net-too.html

## 文章内容

by Fenton Webb
Any Curve derived object inside of AutoCAD uses Parameter values to define significant parts of that Curve. These Parameter values are defined as double values, ranging from 0.0 to n.
Lines define their Parameter values as 0.0 to Length. So a Line drawn from A to B would have a start parameter value of 0.0 and an end of Length – the midpoint, for instance, can be obtained by using :
double length = 0.0;
line->getEndParam(length);
line->getPointAtParam(length/2.0);
Circles define their Parameter values as 0.0 to 2*PI, as does Arcs and Ellipses. So, by obtaining the start and end params you can very easily get quadrant points using the same technique.
Using the Parameter methods of a Polyline you can get any point on a polyline; the Parameter values work roughly the same as a Line, except the Parameter values only define the vertexes as indexes, no length values - e.g. p1=Param 0.0, p2=Param 1.0, p3=Param 2.0, etc.
There are quite a few functions which work to obtain a point from a Parameter value or visa versa (search the ARX Reference for *Param* to see them all)…
Here’s a few which I use a lot when processing Curve geometry…
AcDbCurve::getParamAtPoint - get the parameter value at a given point, say the start point = vertex 3 and the end point = vertex 4.
// open a polyline and extract the vertex data from it
// start and end points for instance.....
ads_real fromParam = 0.0;
// get the parameter value of vertex 3 start point
pPoly->getParamAtPoint (startPoint, fromParam);      
ads_real toParam = 0.0;
// get the parameter value of vertex 4 start point
pPoly->getParamAtPoint (endPoint, toParam);      
   AcDbCurve::getPointAtParam - get a point using a parameter value. Using the fromParam and toParam above, we can obtain the midpoint between the startPoint (param 3) and the endPoint (param 4) like this
  // get the mid point of the start and end points along the pline
pPoly->getPointAtParam (fromParam + ((toParam-fromParam) / 2.0), midPoint); 
AcDbCurve::getDistAtParam - get a distance from a Parameter value
Now because the parameter values of a Polyline are not length related, but vertex related, then the midpoint parameter value of the entire Polyline, and then its actual midpoint could be obtained like this…
  double startParam=0.0, endParam=0.0, midParam=0.0, dist=0.0;
// always get the startParam, because it tends to be
// defined slightly differently across different curve types
pPoly->getStartParam(startParam);
pPoly->getEndParam(endParam);
// now get the midpoint of the Polyline using params
AcGePoint3d midPoint;
pPoly->getDistAtParam(endParam, dist); 
pPoly->getParamAtDist(dist/2.0, midParam);
pPoly->getPointAtParam(midParam, midPoint);

## 评论

**内容**: Gaston Nunez said...
Hi,
"These Parameter values are defined as double values, ranging from 0.0 to n." that's not true for arcs, ellipse arc etc.
Gaston Nunez
Reply
06/08/2012 at 07:51 PM

---
**内容**: Owen Wengerd said...
I nominate this post for the hall of shame. The internet is awash in misinformation and incorrect or sloppy code samples using curve parameters, but I expect you guys at Autodesk to clean things up, not make them worse. This is now the second post on this blog that presents almost identical incorrect code, as if to reinforce the first post on the subject.
As Gaston says, you can never assume that the start parameter is 0.0, even for AcDbLine and other core entities. Also, it is never safe to assume that a midpoint is halfway between the parameters of the endpoints. The correct way to calculate a midpoint is by first calculating the average of the distances at each endpoint, then finding the point at that distance.
Reply
06/08/2012 at 10:27 PM

---
