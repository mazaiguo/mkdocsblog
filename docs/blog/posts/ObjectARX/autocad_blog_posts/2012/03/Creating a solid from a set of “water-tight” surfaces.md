---
title: "Creating a solid from a set of “water-tight” surfaces"
date: 2012-03-01
categories:
  - AutoCAD
tags:
  - Database
  - Solid
  - Surface
description: "A collection of surfaces that together form a closed volume and which do not have gaps, overlaps, such surfaces can be used to create a solid. Here..."
author: Autodesk
---
# Creating a solid from a set of “water-tight” surfaces

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/creating-a-solid-from-a-set-of-water-tight-surfaces.html

## 文章内容

By Balaji Ramamoorthy
A collection of surfaces that together form a closed volume and which do not have gaps, overlaps, such surfaces can be used to create a solid. Here is a sample code to do this using the "createSculptedSolid" method of the "AcDb3dSolid" class.
// surfaceOids :
// A collection of the objectId of the surfaces that
// form the bounds of the solid
  Acad::ErrorStatus es;
  AcDb3dSolid *pSolid = new AcDb3dSolid();
pSolid->setDatabaseDefaults();
  AcArray<AcDbEntity*> surfacesArray;
AcGeIntArray limits;
AcDbEntity *pSurfaceEnt;
  for(int surfCnt = 0;
        surfCnt < surfaceOids.size(); surfCnt++)
{
    es = acdbOpenAcDbEntity(
                pSurfaceEnt, surfaceOids[surfCnt],
                AcDb::kForRead);
      if ( es == Acad::eOk &&
         pSurfaceEnt->isKindOf(AcDbSurface::desc()))
    {
        surfacesArray.append(pSurfaceEnt);
    }
}
  es = pSolid->createSculptedSolid(surfacesArray, limits);
if(es == Acad::eOk)
{
    AcDbObjectId solidOid = AcDbObjectId::kNull;
    Add2Db(pSolid, solidOid);
      // To show the newly created solid away
    // from the surfaces, we transform it..
    AcDbEntity *pSolidEnt;
    es = acdbOpenAcDbEntity(
            pSolidEnt, solidOid, AcDb::kForWrite);
    if  (es == Acad::eOk &&
            pSolidEnt->isKindOf(AcDb3dSolid::desc()))
    {
        AcGeVector3d vec(15.0, 15.0, 0.0);
        AcGeMatrix3d transform =
                    transform.setToTranslation(vec);
        es = pSolidEnt->transformBy(transform);
        pSolidEnt->close();
        acutPrintf(ACRX_T(
                    "Solid3d created from surfaces !"));
    }
    else
    {
        acutPrintf(ACRX_T("Solid3d creation failed !"));
    }
}
else
{
    acutPrintf(ACRX_T("Solid3d creation failed !"));
    delete pSolid;
}
  // Close the surfaces
int surfCnt = 0;
for(; surfCnt < surfacesArray.length(); surfCnt++)
{
    pSurfaceEnt = surfacesArray[surfCnt];
    pSurfaceEnt->close();
}

