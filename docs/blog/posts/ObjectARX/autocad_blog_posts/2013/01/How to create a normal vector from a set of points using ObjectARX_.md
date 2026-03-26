---
title: "How to create a normal vector from a set of points using ObjectARX?"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "How can you build the plane that contains an array of points in order to get the normal direction? The following geometric utility does this:"
author: Autodesk
---
# How to create a normal vector from a set of points using ObjectARX?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-create-a-normal-vector-from-a-set-of-points-using-objectarx.html

## 文章内容

By Gopinath Taget
How can you build the plane that contains an array of points in order to get the normal direction? The following geometric utility does this:
Adesk::Boolean obtainNormal( AcGePoint3dArray &wcsPts,
AcGeVector3d &normal )
{
AcGeVector3d xAxis = AcGeVector3d::kIdentity;
normal = AcGeVector3d::kIdentity;
   int nPts = wcsPts.length();
 for( int i=0; i<nPts ; i++ ) {
  AcGeVector3d vec = wcsPts[(i+1)%nPts] - wcsPts[i];
  if( vec.isZeroLength() )
   continue;
  else if( !normal.isZeroLength() ) {
   if( vec.isPerpendicularTo( normal ))
    continue;
   else
    return Adesk::kFalse;
  }
    else if( xAxis.isZeroLength() )
   xAxis = vec;
  else if( !xAxis.isParallelTo(vec ) ) {
   normal = xAxis.crossProduct( vec ).normal();
  }
}
   if( normal.isZeroLength() ) {
  if( xAxis.isZeroLength() )
   normal = AcGeVector3d::kZAxis;
  else
   normal = xAxis.perpVector();
}
 return Adesk::kTrue;
}

