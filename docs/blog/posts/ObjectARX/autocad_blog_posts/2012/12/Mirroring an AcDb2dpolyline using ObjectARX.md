---
title: "Mirroring an AcDb2dpolyline using ObjectARX"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Polyline
description: "When I apply a transformation to an AcDb2dPolyline that has a mirror component, the arcs of the reflected polyline go the wrong way. How can I avoi..."
author: Autodesk
---
# Mirroring an AcDb2dpolyline using ObjectARX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/mirroring-an-acdb2dpolyline-using-objectarx.html

## 文章内容

by Fenton Webb
Issue
When I apply a transformation to an AcDb2dPolyline that has a mirror component, the arcs of the reflected polyline go the wrong way. How can I avoid this?
Solution
If the transformation has a reflection or mirror component, the bulges need to be negated. This is done when the object is invoked with the mirror command, but not when calling the ARX function. The following sample does this.
void utilsmirror()
{
  // select the 2d polyline
  ads_name eName;
  ads_point pt;
  int res = ads_entsel(_T("\nPlease pick a polyline"), eName, pt);
  if (res != RTNORM)
    return;
    // convert the ename to an ObjectARX objectid
  AcDbObjectId id;
  acdbGetObjectId( id, eName );
    // now open the polyline2d for write
  AcDbObjectPointer<AcDb2dPolyline> pPoly(id, AcDb::kForWrite);
  // if ok
  if (pPoly.openStatus() == Acad::eOk)
  {
    AcGeMatrix3d mat;
    // setup a mirroring transform matrix
    mat.setToMirroring( AcGePlane( AcGePoint3d::kOrigin, AcGeVector3d::kXAxis ));
    // now mirror the polyline
    pPoly->transformBy(mat);
    // finally, iterate the vertexes and invert the bulges
    AcDbObjectIterator *pIter =  pPoly->vertexIterator();
    for(; !pIter->done(); pIter->step() )
    {
      AcDbObjectId id = pIter->objectId();
      AcDbObjectPointer<AcDb2dVertex> pVertex(id, AcDb::kForWrite);
      if(pVertex.openStatus() == Acad::eOk)
        pVertex->setBulge( -pVertex->bulge() );
    }
    delete pIter;
  }
  else     acutPrintf(_T("\nNot an AcDb2dPolyline..."));
}

