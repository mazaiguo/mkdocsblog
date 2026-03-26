---
title: "How to use AcDbRegion::getAreaProp()"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "The first three parameters for the function are described as"
author: Autodesk
---
# How to use AcDbRegion::getAreaProp()

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-use-acdbregiongetareaprop.html

## 文章内容

By Xiaodong Liang
The first three parameters for the function are described as
- origin Returns origin of the region
- xAxis Returns xAxis of the region
- yAxis Returns yAxis of the region
But considering the const declaration for these parameters
virtual Acad::ErrorStatus getAreaProp(
                           const AcGePoint3d& origin,
                           const AcGeVector3d& xAxis,
                           const AcGeVector3d& yAxis, ... );
It's clear that these three parameters are not output parameters but input parameters. Using parameters that were not initialized properly results in the function returning Acad::eInvalidInput.
Here is a correct application of AcDbRegion::getAreaProp():
// note for code brevity, some error checking are omitted
//
void getRegionAreaProp()
{
    ads_name eNam;
    ads_point pt;
    AcDbObjectId eId;
      if (acedEntSel(L"\nSelect an region: ", eNam, pt) != RTNORM)
    {
        acutPrintf(L"\nNothing selected.");
        return;
    }
    acdbGetObjectId(eId, eNam);
      AcDbEntity* pEnt = NULL;
    if(acdbOpenAcDbEntity(pEnt, eId, AcDb::kForRead) != Acad::eOk)
    {
        acutPrintf(L"\nError open entity.");
        return;
    }
    AcDbRegion* pReg = AcDbRegion::cast(pEnt);
    if(!pReg)
    {
        pEnt->close();
        return;
    }   
    double perimeter, area, momInertia[2],
           prodInertia, prinMoments[2],   
           radiiGyration[2];
    AcGePoint2d centroid, extentsLow, extentsHigh;
    AcGeVector2d prinAxes[2];
      AcGePoint3d origin;
    AcGeVector3d xAxis;
    AcGeVector3d yAxis;
      // initialize the three arguments
    AcGePlane plane;
    pReg->getPlane(plane);
    plane.getCoordSystem(origin, xAxis, yAxis);
      Acad::ErrorStatus es = pReg->getAreaProp(
        // these (3) are the input parameters
        origin, xAxis, yAxis,
        perimeter,
        area,
        centroid,
        momInertia,
        prodInertia,
        prinMoments,
        prinAxes,
        radiiGyration,
        extentsLow,
        extentsHigh);
      assert(es == Acad::eOk);
    // you can determine what to do exactly with the results
    // here I just print a message
    acutPrintf(L"\nSucceded in getting an region's area prop.");
    pReg->close();
}

