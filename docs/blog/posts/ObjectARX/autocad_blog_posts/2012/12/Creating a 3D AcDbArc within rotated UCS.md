---
title: "Creating a 3D AcDbArc within rotated UCS"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Dimension
  - UCS
description: "Consider this: You would like to create an AcDbArc in ARX by having the user specify a center point and two endpoints, but the angles are all wrong..."
author: Autodesk
---
# Creating a 3D AcDbArc within rotated UCS

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/creating-a-3d-acdbarc-within-rotated-ucs.html

## 文章内容

By Gopinath Taget
Consider this: You would like to create an AcDbArc in ARX by having the user specify a center point and two endpoints, but the angles are all wrong when you have a custom rotated UCS. So what is going on?
The problem is that the coordinates of points returned from acedGetPoint are in UCS, while arguments to AcDbArc expect WCS coordinates and vectors. The solution is to use acdbUcs2Wcs() to convert the points from UCS to WCS, then obtain the correct reference angles and apply the startAngle and endAngle to the new AcDbArc entity. The best way to obtain the normal for your new arc is to get the cross product of v1 and v2(the vectors joining the center point and the two end points of the arc), which returns a vector which is perpendicular to the plane on which these two vectors lie. Note that this example uses the distance from 'center' to 'pt1' as the radius of the arc.
void CreateArc()
{
AcGePoint3d center, pt1, pt2;
 if(RTNORM != acedGetPoint( NULL,
  L"Center point: ", asDblArray(center) )
  || RTNORM != acedGetPoint(
  asDblArray(center), L"Begin Arc: ",
  asDblArray( pt1 ) )
  || RTNORM != acedGetPoint(
  asDblArray(center), L"End Arc: ",
  asDblArray( pt2) ))
{
  ads_printf( L"\nFunction canceled\n" );
  return;
}
 // Convert the points to WCS
AcGePoint3d centerWcs,pt1Wcs,pt2Wcs;
acdbUcs2Wcs(asDblArray(center),
  asDblArray(centerWcs),false);
acdbUcs2Wcs(asDblArray(pt1),
  asDblArray(pt1Wcs),false);
acdbUcs2Wcs(asDblArray(pt2),
  asDblArray(pt2Wcs),false);
AcGeVector3d v1Wcs(pt1Wcs-centerWcs),
  v2Wcs(pt2Wcs-centerWcs);// create the WCS vectors
 // Get the normal for the new arc.
AcGeVector3d arcNorm=v1Wcs.crossProduct(v2Wcs);
 // Create the new Arc
 // Note radius is distance from centerWcs to pt1Wcs.
AcDbArc * pArc=new
  AcDbArc(centerWcs,arcNorm,
  centerWcs.distanceTo(pt1Wcs),0,6.28);
 // Get the reference Vector...
AcGeVector3d arcRef=arcNorm.perpVector();
arcNorm.negate();// We want our arc between the two
                  // points, not everywhere but in-between.
 double startAngle= v1Wcs.angleTo(arcRef,arcNorm);
 double endAngle = v2Wcs.angleTo(arcRef,arcNorm);
 // Set the Angles
pArc->setStartAngle(startAngle);
pArc->setEndAngle(endAngle);
postToModelSpace(pArc);// Append To MODEL SPACE
}
To keep this example simple, the function postToModelSpace(), which just appends the new entity to the model space of the current drawing has been omitted.

