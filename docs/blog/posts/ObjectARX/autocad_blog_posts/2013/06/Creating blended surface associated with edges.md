---
title: "Creating blended surface associated with edges"
date: 2013-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Surface
description: "Here is a sample code to create a blended surface that is associated with the edges from two other surfaces. The associativity ensures that the ble..."
author: Autodesk
---
# Creating blended surface associated with edges

发布日期: 2013-06-01

原始链接: https://adndevblog.typepad.com/autocad/2013/06/creating-blended-surface-associated-with-edges.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to create a blended surface that is associated with the edges from two other surfaces. The associativity ensures that the blended surface is suitably modified by AutoCAD when any of those surfaces are modified.
In this sample code, two extruded surfaces are created. The edge information from those surfaces are used to create the loft profile. The loft profiles are used to create a blended surface.
#include "dbextrudedsurf.h"
#include "dbBlendOptions.h"
#include "AcDbAssocVariable.h"
#include "AcDbAssocDependency.h"
#include "AcDbAssocPersSubentIdPE.h"
#include "acarray.h"
AcDbDatabase *pDb
            = acdbHostApplicationServices()->workingDatabase();
Acad::ErrorStatus es;
  AcDbObjectId surfaceId1 = AcDbObjectId::kNull;
AcDbObjectId surfaceId2 = AcDbObjectId::kNull;
AcDbSweepOptions sweepOptions;
  // Create the first cylindrical surface
AcGePoint3d center1 = AcGePoint3d::kOrigin;
double radius1 = 10.0;
double height1 = 5.0;
AcDbCircle *pCircle1
      = new AcDbCircle(center1, AcGeVector3d::kZAxis, radius1);
AcDb3dProfile circularProfile1(pCircle1);
AcDbExtrudedSurface *pExtrudedSurface1 = NULL;
es = AcDbSurface::createExtrudedSurface
                    (
                        &circularProfile1,
                        AcGeVector3d(0.0, 0.0, height1),
                        sweepOptions,
                        pExtrudedSurface1
                    );
  // Create the second cylindrical surface
AcGePoint3d center2(0.0, 0.0, 10.0);
double radius2 = 5.0;
double height2 = 5.0;
AcDbCircle *pCircle2
    = new AcDbCircle(center2,  AcGeVector3d::kZAxis, radius2);
AcDb3dProfile circularProfile2(pCircle2);
AcDbExtrudedSurface *pExtrudedSurface2 = NULL;
es = AcDbSurface::createExtrudedSurface
                (
                    &circularProfile2,
                    AcGeVector3d(0.0, 0.0, height2),
                    sweepOptions,
                    pExtrudedSurface2
                );
  AcDbBlockTable *pBlockTable;
AcDbBlockTableRecord *pMS = NULL;
pDb->getBlockTable(pBlockTable, AcDb::kForRead);
pBlockTable->getAt(ACDB_MODEL_SPACE, pMS, AcDb::kForWrite);
  // Add both the cylindrical surfaces to the database
pMS->appendAcDbEntity(surfaceId1, pExtrudedSurface1);
  pMS->appendAcDbEntity(surfaceId2, pExtrudedSurface2);
  pMS->close();
pBlockTable->close();
  // Get the Protocol extension associated with the
// first cylindrical surface.
// This will be used to fetch the edge information.
AcDbAssocPersSubentIdPE* const pAssocPersSubentIdPE1
    = AcDbAssocPersSubentIdPE::cast(
    pExtrudedSurface1->queryX(AcDbAssocPersSubentIdPE::desc()));
  if( pAssocPersSubentIdPE1 == NULL)
    return;
  // Get all the edge subentities from the first cylindrical surface
AcArray<AcDbSubentId> edgeSubentIds1;
pAssocPersSubentIdPE1->getAllSubentities
                    (
                        pExtrudedSurface1,
                        AcDb::kEdgeSubentType,
                        edgeSubentIds1
                    );
  // Get the edge subent for the edge that will be used for
// the blended surfaces.
AcDbFullSubentPath path1(surfaceId1, edgeSubentIds1[0]);
  // Create a loft profile using the edge
AcDbEdgeRef edgeRef1(path1);
AcArray<AcDbEdgeRef> edgeArray1;
edgeArray1.append(edgeRef1);
AcDbPathRef pathRef1(edgeArray1);
AcDbLoftProfile startProfile(pathRef1);
  // Get the Protocol extension associated with the
// second cylindrical surface
AcDbAssocPersSubentIdPE* const pAssocPersSubentIdPE2
    = AcDbAssocPersSubentIdPE::cast(
        pExtrudedSurface2->queryX(AcDbAssocPersSubentIdPE::desc()));
  if( pAssocPersSubentIdPE2 == NULL)
    return;
  // Get all the edge subentities from the second cylindrical surface
AcArray<AcDbSubentId> edgeSubentIds2;
pAssocPersSubentIdPE2->getAllSubentities
                (
                    pExtrudedSurface2,
                    AcDb::kEdgeSubentType,
                    edgeSubentIds2
                );
  // Get the edge subent for the edge that will be used for
// the blended surfaces.
AcDbFullSubentPath path2(surfaceId2, edgeSubentIds2[1]);
  // Create a loft profile using the edge
AcDbEdgeRef edgeRef2(path2);
AcArray<AcDbEdgeRef> edgeArray2;
edgeArray2.append(edgeRef2);
AcDbPathRef pathRef2(edgeArray2);
AcDbLoftProfile endProfile(pathRef2);
  pExtrudedSurface1->close();
pExtrudedSurface2->close();
  // Create the blended surface using the loft profiles
// Ensure that we create an associative blended surface.
AcDbBlendOptions blendOptions;
AcDbObjectId blendSurfaceId = AcDbObjectId::kNull;
AcDbSurface *pBlendSurface = NULL;
  es = AcDbSurface::createBlendSurface
                (
                    &startProfile,
                    &endProfile,
                    &blendOptions,
                    true,
                    blendSurfaceId
                );
if(es == Acad::eOk)
{
    acutPrintf(ACRX_T("Created blended surface !"));
}
The cylindrical surfaces and the blended surface appear as shown in this image :

## 评论

**内容**: Konstantin said...
Hi,
is there a version in C# .NET ?
Reply
07/01/2013 at 05:14 AM

---
**内容**: Balaji said...
Hi Konstantin,
It should be possible to follow the same steps even with the .Net API. Sorry, I do not have the equivalent of it in C# ready with me, but please do let me know if you are finding it difficult to migrate it and I will try rewriting it in .Net.
Reply
07/03/2013 at 03:24 AM

---
