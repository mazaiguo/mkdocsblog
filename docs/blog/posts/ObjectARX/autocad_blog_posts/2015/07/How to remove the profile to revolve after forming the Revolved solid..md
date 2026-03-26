---
title: "How to remove the profile to revolve after forming the Revolved solid."
date: 2015-07-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
  - Solid
description: "Sometime back I have received a query from an ADN partner about"
author: Autodesk
---
# How to remove the profile to revolve after forming the Revolved solid.

发布日期: 2015-07-01

原始链接: https://adndevblog.typepad.com/autocad/2015/07/how-to-remove-the-profile-to-revolve-after-forming-the-revolved-solid.html

## 文章内容

By Madhukar Moogala
Sometime back I have received a query from an ADN partner about
“After using AcDb3dSolid::createRevolvedSolid(), the revolved curve is visible in solid.”
The profile used to create Revolve appears in the solid, as shown in the snapshot.
  This can be removed using cleanBody api of AcDb3dSolid, it removes all edges and faces not necessary to support the topology of the solid.
C++ Code:
void createSolid()
{
    double PI_VALUE = 4.0 * atan(1.0);
    AcGePoint2dArray pointArray;
    pointArray.append(AcGePoint2d(10.0, 0.0));
    pointArray.append(AcGePoint2d(15.0, 0.0));
    pointArray.append(AcGePoint2d(16.0, 2.0));
    pointArray.append(AcGePoint2d(16.0, 10.0));
    pointArray.append(AcGePoint2d(10.0, 10.0));
    pointArray.append(AcGePoint2d(10.0, 0.0));
      AcDbPolyline* pPline = new AcDbPolyline();
    for (int i = 0; i < pointArray.length(); i++)
    {
        pPline->addVertexAt(i, pointArray[i]);
    }
      AcDbRevolveOptions revolveOptions;
    AcDb3dSolid* pSolid = new AcDb3dSolid();
    if (eOkVerify(pSolid->createRevolvedSolid(pPline,
                    AcGePoint3d::kOrigin,
                    AcGeVector3d::kYAxis,
                    2.0 * PI_VALUE,
                    0.0, revolveOptions)))
    {
    /*Removes all edges and faces not necessary to
    support the topology of the solid.*/
    if(eOkVerify(pSolid->cleanBody()))
    {
        AcDbObjectId objId;
        AcDbDatabase* pcurDb =
acdbHostApplicationServices()->workingDatabase();
        postToDatabase(pcurDb,
                        pSolid,
                        objId);
    }
      }
    delete pSolid;
    pSolid =NULL;
    return;
}

