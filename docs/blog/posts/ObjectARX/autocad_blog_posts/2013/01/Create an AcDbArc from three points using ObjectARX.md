---
title: "Create an AcDbArc from three points using ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Unicode
description: "Before we get started with this one, aside from the original issue and solution text, notice the function for converting AcGeCurve objects into AcD..."
author: Autodesk
---
# Create an AcDbArc from three points using ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/create-an-acdbarc-from-three-points-using-objectarx.html

## 文章内容

By Fenton Webb
Before we get started with this one, aside from the original issue and solution text, notice the function for converting AcGeCurve objects into AcDbCurve equivalents createFromAcGeCurve() – very useful…
Issue
Similar to command line creation of an arc, how to create an AcDbArc in
ARX by specifying a startpoint, midpoint and endpoint ?
Solution
You can emulate this AutoCAD-editor feature by using the AcGe helper classes:
void test2()
{  
  // get the points
  AcGePoint3d p1, p2, p3;  
  if(RTNORM != acedGetPoint(NULL, L"First point: ", asDblArray(p1))  
|| RTNORM != acedGetPoint(NULL, L"Second point: ", asDblArray(p2))  
  || RTNORM != acedGetPoint(NULL, L"Third point: ", asDblArray(p3)))  
  {
    acutPrintf(L"\nFunction canceled\n" );     
    return;   
  }   
    // create an AcGeCirc
  AcGeCircArc3d geArc(p1, p2, p3);
  AcDbArc *pArc = NULL;
  // now convert the AcGeCirc to an AcDbArc
  AcDbCurve::createFromAcGeCurve(geArc, (AcDbCurve*&) pArc);
  // now cast to a smart pointer so we don't have to worry about
  // closing or freeing
  AcDbObjectPointer<AcDbArc> arc;
  arc.acquire(pArc);
  // get the current database
  AcDbDatabase *db = curDoc()->database();
  AcDbBlockTableRecordPointer curSpace(db->currentSpaceId(), AcDb::kForWrite);
  if(curSpace.openStatus() == Acad::eOk)
    curSpace->appendAcDbEntity(arc.object());
}

