---
title: "Mirroring plane from a mirroring matrix"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Wondering how you can get a mirroring plane from a matrix passed into transformBy( ) during a MIRROR command?"
author: Autodesk
---
# Mirroring plane from a mirroring matrix

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/mirroring-plane-from-a-mirroring-matrix.html

## 文章内容

By Gopinath Taget
Wondering how you can get a mirroring plane from a matrix passed into transformBy( ) during a MIRROR command?
Here I present one way to calculate a mirroring plane from a matrix passed into transformBy( ) during a MIRROR command. This is done using vector algebra.
if [M] is a transformation matrix passed in during a mirroring operation, then the mirror of an arbitrary point P will be [M]P.
We know that a mirroring plane is midway between the point P and its mirror [M]P,
so any point on the mirroring plane = ( 1/2) .(P+ [ M ]P ). This by the way is the same as a vector P projected on this plane.
This can also be written as:
Point on mirroring plane = ( 1/2) .([I]P+ [ M ]P)
Or
Point on mirroring plane = ( 1/2) .([I]+ [ M ]) x P
Here [ I ] is the identity matrix.
So the transformation matrix applied to find the projection on this plane is ( 1/2) .( [ I ] + [ M ] ). You may then take two arbitrary vectors to find projections on this plane - so you have 2 coplanar vectors. You may then find the cross product of these two to find a vector normal to them. You then take an origin, say (0,0,0) and transform with the above transformation matrix to find a point on this plane.
So now you have a point on the mirroring plane and a vector normal to it. With these you can construct a mirroring plane. The code below shows how to do this.
xform is the transformation matrix passed into transformBy during a mirroring operation (you can do this with an editor reactor checking to see when "MIRROR" happens)
AcGePoint3d origin(0,0,0);
AcGeVector3d normal, Axis1, Axis2, Axis3,
XAxis(1,0,0), YAxis(0,1,0), ZAxis(0,0,1);
AcGeMatrix3d Identity, Temp; 
AcGePlane MirrorPlane;
AcGeMatrix3d Mirror;
Identity.setToIdentity();
  for(int i=0; i<4; i++) {
 for(int j=0; j<4; j++) {
  Temp(i,j) = 0.5*(Identity(i,j) + xform(i,j));
}
}
  Axis1 = (XAxis.transformBy(Temp)).normalize();
Axis2 = (YAxis.transformBy(Temp)).normalize();
Axis3 = (ZAxis.transformBy(Temp)).normalize();
origin = origin.transformBy(Temp);
  // Choose two vectors out of the three Axis1,
// Axis2 and Axis3 to find the cross product.
// Make sure that the two selected vectors are of
// unit length and are not parallel
if (Axis1.length() == 1 && Axis2.length() == 1 && 
fabs(Axis1.dotProduct(Axis2)) != 1) {
normal = (Axis1.crossProduct(Axis2)).normalize();
} else if (Axis2.length() == 1 && Axis3.length() == 1 && 
fabs(Axis2.dotProduct(Axis3)) != 1) {
normal = (Axis2.crossProduct(Axis3)).normalize();
} else if (Axis3.length() == 1 && Axis1.length() == 1 && 
fabs(Axis3.dotProduct(Axis1)) != 1) {
normal = (Axis3.crossProduct(Axis1)).normalize();
}
  MirrorPlane.set(origin, normal); // This is the mirroring plane

