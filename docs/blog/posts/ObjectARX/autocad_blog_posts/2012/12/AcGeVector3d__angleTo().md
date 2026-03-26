---
title: "AcGeVector3d::angleTo()"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - XREF
description: "The method AcGeVector3d::angleTo("
author: Autodesk
---
# AcGeVector3d::angleTo()

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/acgevector3dangleto.html

## 文章内容

By Xiaodong Liang
Issue
The method AcGeVector3d::angleTo(
                                                  const AcGeVector3d &vec,
                                                  const AcGeVector3d&  refVec)  is described as follows in the ARXREF.HLP:
"Returns the angle between this vector and the vector 'vec' in the range [0, 2 * PI]; If ( refVec.dotProduct(crossProduct(vec)) >= 0.0 ) the return value coincides with the return value of the function angleTo( vec ). Otherwise the return value is 2*PI minus the return value of the function angleTo( vec )."
What exactly is meant when passing as refVec?
Solution
According to the online documentation, there are two overloaded functions for angleTo().
One is:

double AcGeVector3d::angleTo( const AcGeVector3d& vec) const;
Returns the angle between this vector and the vector vec in the range [0, Pi].
Another is:

double AcGeVector3d::angleTo(
                    const AcGeVector3d& vec,
                    const AcGeVector3d& refVec) const;
Returns the angle between this vector and the vector vec in the range [0, 2 x  Pi]. If (refVec.dotProduct(crossProduct(vec)) >= 0.0), then the return value  coincides with the return value of the function angleTo(vec). Otherwise, the  return value is 2 x Pi minus the return value of the function angleTo(vec). Therefore, the return angle's range is different. That's exactly why the refVec  is needed. Dot Product, as you know, is a method to find out how parallel two
lines are. The result of the calculation is a scalar. This is most useful if you  use unit vectors (get a number between -1 and 1), such as our usage here  (vectors).
|x1| |x2|

|y1| . |y2| = (x1 * x2) + (y1 * y2) + (z1 * z2)

|z1| |z2|
Cross Product is the process of multiplying two vectors together to get a  normal to the plane they describe with the Vector (0,0,0).

|x1| |x2| |y1*z2 - z1*y2|

|y1| x |y2| = |z1*x2 - x1*z2|

|z1| |z2| |x1*y2 - y1*x2|
Therefore, in the code,
refVec.dotProduct(crossProduct(vec))
it first checks the angle between the normal (for the plane which 'this' vector  and 'vec' vector is on) and the refVec. As it states, if
(refVec.dotProduct(crossProduct(vec)) >= 0.0), then the return value coincides with the return value of the function angleTo(vec). Otherwise the return value is 2 x Pi minus the return value of the function angleTo(vec). You can actually use the normal vector for the plane that 'this' vector is on,  as the refVec, to check the 'vec'. Of course, you can choose other vectors that  are not the same as the normal vector depends on your application needs.

