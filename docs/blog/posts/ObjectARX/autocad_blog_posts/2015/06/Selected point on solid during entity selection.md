---
title: "Selected point on solid during entity selection"
date: 2015-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Dimension
  - Selection
  - Solid
  - UCS
description: "The acedEntSel method provides a way for the user to select an entity and it also provides the point that was used during the entity selection. Whe..."
author: Autodesk
---
# Selected point on solid during entity selection

发布日期: 2015-06-01

原始链接: https://adndevblog.typepad.com/autocad/2015/06/selected-point-on-solid-during-entity-selection.html

## 文章内容

By Balaji Ramamoorthy
The acedEntSel method provides a way for the user to select an entity and it also provides the point that was used during the entity selection. When used on a 2D entity, the point returned by acedEntSel is quite useful if you need that information to further work on the entity and perform tasks such as break, trim etc. 
However, when acedEntSel is used to select a solid, the point returned is in the UCS XY Plane regardless of where on the solid you pick. if you use an OSNAP while selecting the solid entity, the point will be on the solid. If the point on the solid that was used while selecting the solid is important for doing further processing in your code, here is a way to get that.
In the following code, a ray is created along the viewing direction with which we will find the intersection points of the solid. The code displays all the intersection points as though the ray pierced the solid. But the first intersection point should provide the selection point, in case you are only interested in that.
Please note that, in AutoCAD 2015 and AutoCAD 2016, the "AcBrBrep::getLineContainment" returns lesser number of hits during an intersection test. This behavior has been logged with our engineering team. AutoCAD 2014 and previous releases provide the right number of hits.
Here is a recording which demonstrates the entity selection and the sample code :
 Acad::ErrorStatus es;
   // pt is in UCS coordinates and in the UCS XY plane  
 // unless a osnap is used while selecting the entity 
 // In that case, the point will be have all  
 // the three coordinate values in UCS. 
 ads_name  ename;
 ads_point pt;
 int  ret = acedEntSel(_T("\\nPick a solid : " ), ename, pt);
 if  (ret != RTNORM)
  return ;
     AcDbObjectId entId = AcDbObjectId::kNull;
 es = acdbGetObjectId(entId, ename);
   AcDbEntity *pEnt = NULL;
 AcDb3dSolid *pSolid = NULL;
 es = acdbOpenAcDbEntity(pEnt, entId, AcDb::kForRead);
 pSolid = AcDb3dSolid::cast(pEnt);
 if (pSolid == NULL)
 {
  acutPrintf(L"\\nSelected entity was not a solid.\\n" );
  return ;
 }
   // Get the WCS coordinates of the selected point 
 AcGePoint3d wcsPt = AcGePoint3d::kOrigin;
 acdbUcs2Wcs(pt, pt, 0);
 wcsPt = asPnt3d(pt);
     resbuf viewRb;
   AcGePoint3d  target = AcGePoint3d::kOrigin; 
 // TARGET is in UCS 
 acedGetVar(_T("TARGET" ), &viewRb); 
 target = asPnt3d(viewRb.resval.rpoint);
 acdbUcs2Wcs(asDblArray(target), asDblArray(target), 0);
   AcGeVector3d dir = AcGeVector3d::kIdentity; 
 // VIEWDIR is in UCS 
 acedGetVar( ACRX_T("VIEWDIR" ), &viewRb ); 
 dir = asVec3d(viewRb.resval.rpoint);
 acdbUcs2Wcs(asDblArray(dir), asDblArray(dir), 1);
 AcGePoint3d  position = target + dir;
 dir = dir.normalize().negate();
   AcGeLine3d testRay(
  wcsPt.project(AcGePlane(position, dir), dir.negate()),
  dir);
   AcBrBrep*pBrep = new  AcBrBrep();
 pBrep->setSubentPath( AcDbFullSubentPath
  ( pEnt->objectId(),  AcDbSubentId()));
   AcBr::ErrorStatus bres;
 AcBrHit *pHits = NULL;
 Adesk::UInt32 nHitsFound = 0;
 // Find all hits 
 bres = pBrep->getLineContainment(
  testRay, 0, nHitsFound, pHits );
 if (bres == AcBr::eOk)
 {
  for ( Adesk::UInt32 i = 0; i < nHitsFound; i++) 
  {
   AcBrEntity *pHitEntity = NULL;
   pHits[i].getEntityHit( pHitEntity );
   if ( pHitEntity == NULL )
    continue ;
        if ( ! pHitEntity->isKindOf(AcBrBrep::desc()))
   {
    AcGePoint3d hitPt;
    pHits[i].getPoint(hitPt);
      AcDbPoint *pDbPt = new  AcDbPoint(hitPt);
    PostToDb(pDbPt);
    es = pDbPt->close();
   } 
   delete  pHitEntity;
  }
  delete  [] pHits;
 }
 delete  pBrep;
   pEnt->close();

