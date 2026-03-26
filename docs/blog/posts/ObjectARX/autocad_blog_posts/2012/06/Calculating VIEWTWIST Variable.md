---
title: "Calculating VIEWTWIST Variable"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "The VIEWTWIST system variable represents the angle between the up vector relative to the view direction in WCS and the actual view's up vector in D..."
author: Autodesk
---
# Calculating VIEWTWIST Variable

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/calculating-viewtwist-variable.html

## 文章内容

By Balaji Ramamoorthy
The VIEWTWIST system variable represents the angle between the up vector relative to the view direction in WCS and the actual view's up vector in DCS. The following code uses the view direction, and constructs an up vector (which is perpendicular to it). It then calculates the actual up vector of the view,and measures the angle between them.
Here is the sample code :
const double PI = 3.14159265359;
  // first obtain the view direction
struct resbuf viewRb;
acedGetVar(ACRX_T("VIEWDIR"), &viewRb );
  AcGeVector3d dirVector
            = asVec3d(viewRb.resval.rpoint);
  // Make sure this value is in WCS
acdbUcs2Wcs(
                asDblArray( dirVector),
                asDblArray( dirVector),
                Adesk::kTrue
            );
  // Calculate the default upVector for this view direction.
AcGeVector3d sideVector
                = dirVector.perpVector();
  AcGeVector3d upVector
            = dirVector.crossProduct(sideVector).normal();
  ads_point UpVec;
asVec3d( UpVec) = upVector;
  // calculate the actual upVector, by
// applying the view transformation.
struct resbuf from, to;
from.restype = RTSHORT;
from.resval.rint = 0;    // WCS
to.restype = RTSHORT;
to.resval.rint = 2;      // DCS
acedTrans(UpVec, &from, &to, TRUE, UpVec);
  // get the twist angle
double safeViewTwist;
safeViewTwist = atan2(UpVec[Y],UpVec[X]) - PI/2 ;
  // Mathematically, we're done.
// The only problem is that VIEWTWIST is normally stored
// between 0 and 2PI, so we'd better add that onto a negative result
if( safeViewTwist < -1e-6 )
    safeViewTwist+= (PI * 2.0 );
acutPrintf(
            ACRX_T("\nsafeViewTwist: %f"),
            safeViewTwist
          );
  // Lets just check that we have the same answer
struct resbuf viewTwist;
acedGetVar(ACRX_T("VIEWTWIST"), &viewTwist );
acutPrintf(
            ACRX_T("\nReal VIEWTWIST: %f"),
            viewTwist.resval.rreal
          );

