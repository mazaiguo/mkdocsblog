---
title: "How to Intersect a line with a solid?"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - API
  - Solid
description: "This is possible using the B-Rep API. The code snippet below illustrates how you can find the intersections of a linear entity ( LINE, XLINE or RAY..."
author: Autodesk
---
# How to Intersect a line with a solid?

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/how-to-intersect-a-line-with-a-solid.html

## 文章内容

By Gopinath Taget
This is possible using the B-Rep API. The code snippet below illustrates how you can find the intersections of a linear entity ( LINE, XLINE or RAY ) with an entity represented using ACIS (that is a SOLID, REGION, or BODY).
// This is command 'INTSOLID'
void Asdkintsolid()
{
  AcDbObjectId lineId;
AcDbObjectId solidId;
AcDbEntity * pEnt;
AcDbEntity * pLinearEnt;
AcGePoint3dArray hitPoints;
 int nHitsWanted;
  ads_name en ;
ads_point pt ;
   // User picks a line
  if ( acedEntSel (_T("\nSelect a line: "), en, pt) != RTNORM )
  return;
 // Get pointer to line
 if ( acdbGetObjectId (lineId, en) != Acad::eOk )
{
  return;
}
acdbOpenAcDbEntity(pLinearEnt, lineId, AcDb::kForRead );
 if(pLinearEnt == NULL )
{
  acutPrintf(_T("\nCannot open line"));
  return;
}
   // User picks a solid
  if ( acedEntSel (_T("\nSelect a solid: "), en, pt) != RTNORM )
  return;
   // Get pointer to line
 if ( acdbGetObjectId (solidId, en) != Acad::eOk )
{
  return;
}
acdbOpenAcDbEntity(pEnt, solidId, AcDb::kForRead );
 if(pEnt == NULL )
{
  acutPrintf(_T("\nCannot open solid"));
  pLinearEnt->close();
  return;
}
   // Get required number of intersections to be returned.
 // If user enters zero, then we will return all intersections.
  if (RTNORM != acedGetInt(_T("\nEnter number of Hits required : "),
   &nHitsWanted))
{
  acutPrintf(_T("\nYou must enter an integer"));
   pEnt->close();
   pLinearEnt->close();
  return;
}
   // Find number of intersections
 if ( Acad::eOk != getHits( pLinearEnt, pEnt,
  nHitsWanted, hitPoints))
{
   pEnt->close();
   pLinearEnt->close();
  return;
}
   // Entities not needed any more
pEnt->close();
pLinearEnt->close();
   // Print out intersections
 int len = hitPoints.length();
 if ( len == 0 )
{
  acutPrintf(_T("\nNo intersections found."));
}
 else
{
  acutPrintf(_T("\n%d intersections found."), len);
    for (int i = 0; i < len; i++)
  {
   AcGePoint3d pt = hitPoints[i];
      acutPrintf(_T("\nIntersection %d: (%f, %f, %f)"),
    i+1, pt[X], pt[Y], pt[Z]);
  }
}
 return;
}
    Acad::ErrorStatus getHits( AcDbEntity * pLinearEnt,
       AcDbEntity * pEnt,
       int nHitsWanted,
       AcGePoint3dArray &hitPoints)
// Parameters:
//  AcDbEntity * pLinearEnt - pointer to a line
//  AcDbEntity * pEnt - pointer to a solid
//  int nHitsWanted - number of intersections
//  to return (0 means return all)
//  AcGePoint3dArray hitPoints - array to
//  return intersection points
// Returns:
//  Acad::eOk - if all is well
//  Acad::eInvalidInput - if there is a problem
{
 // Check that solid pointer is a really a solid
 if( !(pEnt->isKindOf(AcDb3dSolid::desc()) ||
   pEnt->isKindOf(AcDbRegion::desc()) ||
   pEnt->isKindOf(AcDbBody::desc()) ) )
{
  acutPrintf(_T("\nSecond argument must be a solid, not a %s"),
   pEnt->isA()->name());
  return Acad::eInvalidInput;
}
   // Check that the line pointer is a line.
 // If it is, create a corresponding AcGe object.
AcGeLinearEnt3d * pGeLine;
 if(pLinearEnt->isKindOf( AcDbLine::desc() )) {
  AcDbLine * pLine = (AcDbLine*)pLinearEnt;
  pGeLine = new AcGeLineSeg3d(pLine->startPoint(),
   pLine->endPoint() );
} else if (pLinearEnt->isKindOf( AcDbRay::desc() )) {
  AcDbRay * pRay = (AcDbRay*)pLinearEnt;
  pGeLine = new AcGeRay3d(pRay->basePoint(), pRay->unitDir() );
} else if (pLinearEnt->isKindOf( AcDbXline::desc() )) {
  AcDbXline * pXline = (AcDbXline *)pLinearEnt;
  pGeLine = new AcGeLine3d(pXline->basePoint(),
   pXline->unitDir() );
} else {
  acutPrintf(_T("\nFirst argument must be a line, not a %s"),
   pLinearEnt->isA()->name());
  return Acad::eInvalidInput;
}
   // Find the number of intersections using B-Rep API
AcBrBrep*pBrep = new AcBrBrep;
AcDbObjectId solidId = pEnt->objectId();
pBrep->setSubentPath( AcDbFullSubentPath( solidId,
  AcDbSubentId()));
  AcBrHit*pHits = NULL;
Adesk::UInt32 nHitsFound;
pBrep->getLineContainment(*pGeLine, nHitsWanted,
  nHitsFound, pHits );
   // Append valid intersection points to hitPoints
 for( Adesk::UInt32 i=0;i<nHitsFound; i++ ) {
  AcBrEntity*pHitEntity = NULL;
  pHits[i].getEntityHit( pHitEntity );
    if( pHitEntity == NULL )
   continue;
    AcGePoint3d hitPt;
  pHits[i].getPoint(hitPt);
    if( !pHitEntity->isKindOf(AcBrBrep::desc()) ) {
   hitPoints.append( hitPt );
  }
  else
  {  
   acutPrintf(
    _T("\nIgnoring the point at (%f, %f, %f) with a %s"),
    hitPt.x, hitPt.y, hitPt.z, pHitEntity->isA()->name());
  }
  delete pHitEntity;
}
   // Convert points from WCS to UCS
 int nPts = hitPoints.length();
 for( int i=0; i<nPts;i++ ) {
  ads_point pt;
  asPnt3d(pt) = hitPoints[i];
  acdbWcs2Ucs(pt,pt,0);
  hitPoints[i] = asPnt3d(pt);
}
   // Tidy up
 delete [] pHits;
 delete pBrep;
 delete pGeLine;
   // end of function - everything must have worked
 return Acad::eOk;
}

## 评论

**内容**: Gennady said...
how to do the same in c#?
Thanks,
Gennady
Reply
10/17/2016 at 02:46 PM

---
**内容**: Mario said...
Can you explain how to run this code in autocad?
Thanks,
Mario
Reply
03/02/2017 at 10:31 PM

---
