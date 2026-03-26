---
title: "Calculating the Center of an Arc in a Polyline using ObjectARX"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Polyline
description: "The easiest way to do this is to construct an AcGeCircArc2d or AcGeCircArc3d"
author: Autodesk
---
# Calculating the Center of an Arc in a Polyline using ObjectARX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/calculating-the-center-of-an-arc-in-a-polyline-using-objectarx.html

## 文章内容

by Fenton Webb
The easiest way to do this is to construct an AcGeCircArc2d or AcGeCircArc3d
object and then use its center() method to get the point you want.
The following function finds any arc segments in a lightweight polyline and
identifies the center by dropping a point entity (AcDbPoint) in the calculated
location.
#include <dbobjptr.h>
void show_centers()
{     
  // UI for selecting an entity  
  ads_name en;  
  ads_point pt;  
  int rc = acedEntSel(L"Select LW polyline: ", en, pt);  
  if (rc != RTNORM)
  {  
    acutPrintf(L"Nothing selected.\n", rc);  
    return;   
  }      
    // convert ads_name to object id 
  AcDbObjectId eId;    
  Acad::ErrorStatus es = acdbGetObjectId(eId, en);  
  // open object 
  AcDbObjectPointer<AcDbPolyline> pPolyline(eId, AcDb::kForRead);
  if(pPolyline.openStatus() != Acad::eOk)  
  {  
    acutPrintf(L"You did not select a LW polyline.\n");    
    return;   
  }   
    // get the number of segments  
  int segments = pPolyline->numVerts() - 1;  
  for(int i = 0; i < segments; i++)
  {   
    if(pPolyline->segType(i) != AcDbPolyline::kArc)
      continue;   
      // get arc segment on polyline   
    AcGeCircArc2d geArc;   
    pPolyline->getArcSegAt(i, geArc);   
    // get center   
    AcGePoint2d center = geArc.center();   
    // create a point entity   
    AcDbObjectPointer<AcDbPoint> pPoint;
    AcDbPoint *pointPtr = new AcDbPoint(AcGePoint3d(center[0],
  center[1], 0.0));
    pPoint.acquire(pointPtr);     
      // add the point entity to the block table record   
    // containing the selected polyline   
    AcDbBlockTableRecordPointer curSpace(pPolyline->blockId(),
      AcDb::kForWrite);
    if (curSpace.openStatus() == Acad::eOk)
      curSpace->appendAcDbEntity(pPoint);   
      acutPrintf(L"\n - center: [%f, %f]", center[0], center[1]);
  }  
}

