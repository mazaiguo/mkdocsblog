---
title: "Calculating tight bounding box around a solid"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Solid
description: "Consider this: When you calculate the box of a solid, or any other AcDbEntity, this box is aligned with the x,y,z axes. This box might be much larg..."
author: Autodesk
---
# Calculating tight bounding box around a solid

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/calculating-tight-bounding-box-around-a-solid.html

## 文章内容

By Gopinath Taget
Consider this: When you calculate the box of a solid, or any other AcDbEntity, this box is aligned with the x,y,z axes. This box might be much larger than the smallest box which could contain the solid. To take an extreme example, consider the cylinder with radius 1, height 100, aligned with the vector 1,1,1. The box returned by
AutoCAD for this entity has the volume 2.092463E+005. The optimal box (not aligned with the x,y,z axes) has the volume 400. How can you obtain this box?
An exact answer for this problem is not simple, but a good approximation is possible. One can calculate the principal axes from the solid, and align the box with these axes. This gives the perfect answer in this case, and will generally produce a much better answer than doing nothing at all. The attached code shows an approach where the user can select a solid, and then create a box that is the calculated tight box around the solid.
void asdkasdktightboundbox()
{
ads_name eName;
ads_point pt;
   if( RTNORM != acedEntSel(
  _T("\nPlease select a solid "), eName, pt ))
  return;
AcDbObjectId id;
acdbGetObjectId( id, eName );
AcDb3dSolid*pSolid = NULL;
  acdbOpenObject(pSolid, id, AcDb::kForRead );
 if( pSolid == NULL ) {
  acutPrintf(L"\nObject not a solid");
  return;
}
 double volume;
AcGePoint3d centroid;
 double momInertia[3];
 double prodInertia[3];
 double prinMoments[3];
AcGeVector3d prinAxes[3];
 double radiiGyration[3];
  AcDbExtents extents;
  Acad::ErrorStatus es;
es = pSolid->getMassProp(
  volume,
  centroid,
  momInertia,
  prodInertia,
  prinMoments,
  prinAxes,
  radiiGyration,
  extents);
AcGePoint3d max = extents.maxPoint();
AcGePoint3d min = extents.minPoint();
   int xAxis, zAxis;
 double bigVol = (max.x - min.x ) * ( max. y - min.y ) * (max.z - min.z);
acutPrintf(_T("\ncalculated original box "));
acutPrintf(_T("\nvolume %e"), bigVol );
acutPrintf(_T("\nOriginal box is %e the size of the object"), bigVol/volume );
   // some work to make x the largest prin axis, and z the smallest.
 if(prinMoments[0] > prinMoments[1] )
{
  xAxis = 0;
  zAxis = 1;
}
 else
{
  xAxis = 1;
  zAxis = 0;
}
   if(prinMoments[zAxis] > prinMoments[2] )
  zAxis =  2;
 else if(prinMoments[xAxis] < prinMoments[2] )
  xAxis = 2;
  AcGeMatrix3d mat;
AcGeVector3d yAxisVec =
  prinAxes[zAxis].crossProduct( prinAxes[xAxis]);
mat.setCoordSystem( centroid, prinAxes[xAxis],
  yAxisVec, prinAxes[zAxis]);
acutPrintf(_T("\nxAxis %e %e %e"), prinAxes[xAxis].x,
  prinAxes[xAxis].y,prinAxes[xAxis].z);
acutPrintf(_T("\nyAxis %e %e %e"),
  yAxisVec.x, yAxisVec.y, yAxisVec.z);
acutPrintf(_T("\nzAxis %e %e %e"),
  prinAxes[zAxis].x, prinAxes[zAxis].y,prinAxes[zAxis].z);
AcDbEntity*pNewEnt = NULL;
  es = pSolid->getTransformedCopy( mat.inverse(), pNewEnt );
 if( pNewEnt == NULL )
{
  acutPrintf(_T("\nCannot transform solid"));
  acutPrintf(_T("\nError: %s"), acadErrorStatusText(es));
  pSolid->close();
  return;
}
  AcDbExtents newExtents;
pNewEnt->getGeomExtents( newExtents );
 delete pNewEnt;
 //delete pNewEnt;
max = newExtents.maxPoint();
min = newExtents.minPoint();
 double deltaX = (max.x - min.x );
 double deltaY = ( max. y - min.y );
 double deltaZ = (max.z - min.z );
 double smallVol = deltaX * deltaY * deltaZ;
  acutPrintf(_T("\ncalculated smaller box "));
acutPrintf(_T("\nvolume %e"), smallVol );
acutPrintf(
  _T("\nAligned box is %e the size of the object"),
  smallVol/volume );
acutPrintf(
  _T("\nOriginal box is %e the size of the aligned box"),
  bigVol/smallVol);
  AcDb3dSolid*pNewSolid = new AcDb3dSolid;
pNewSolid->createBox(deltaX, deltaY, deltaZ );
AcGePoint3d newBoxCenter = min + 0.5 * (max - min);
pNewSolid->transformBy( mat * AcGeMatrix3d::translation(
  newBoxCenter - AcGePoint3d::kOrigin ) );
AcDbBlockTableRecord*pRecord;
acdbOpenObject(pRecord, pSolid->ownerId(), AcDb::kForWrite );
pSolid->close();
   if( pRecord == NULL )
{
  acutPrintf(_T("\nCannot open BTR"));
  delete pNewSolid;
  return;
}
  pRecord->appendAcDbEntity(pNewSolid);
pNewSolid->close();   
pRecord->close();
  }

