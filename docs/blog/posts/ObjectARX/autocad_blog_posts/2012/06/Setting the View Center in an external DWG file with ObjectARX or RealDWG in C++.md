---
title: "Setting the View Center in an external DWG file with ObjectARX or RealDWG in C++"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - DWG
  - ObjectARX
description: "In raw AutoCAD setting the View center is really easy, just set the VIEWCTR sysvar using acedSetVar(“VIEWCTR”). If you want to set the View center ..."
author: Autodesk
---
# Setting the View Center in an external DWG file with ObjectARX or RealDWG in C++

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/setting-the-view-center-in-an-external-dwg-file-with-objectarx-or-realdwg-in-c.html

## 文章内容

by Fenton Webb
In raw AutoCAD setting the View center is really easy, just set the VIEWCTR sysvar using acedSetVar(“VIEWCTR”). If you want to set the View center in a DWG file that is not loaded into the AutoCAD editor, it takes a little more work.
Here’s how you do it…
#include "dbents.h"
#include "dbobjptr2.h"  // include the smart pointer template
  static void Wcs2Dcs(AcDbViewportTableRecord *pVp, AcGeMatrix3d &resultMat);
// set the viewctr outside of the AutoCAD Editor
// by Fenton Webb, DevTech, Autodesk 01/06/2012
void setViewCenter()
{
  // open some dwg file
  AcDbDatabase *dwg = new AcDbDatabase(false, true);
  if (dwg->readDwgFile(_T("c:\\temp\\fenton.dwg")) == Acad::eOk)
  {
    // read in the whole file, don't cache
    dwg->closeInput();
      // start by getting the viewport table id
    AcDbObjectId id = dwg->viewportTableId();
    {
      AcDbSmartObjectPointer<AcDbViewportTable> pVt (id, AcDb::kForRead);
      // if ok
      if (pVt.openStatus() == Acad::eOk)
      {
        AcDbObjectId vpId;   
        // get the active viewport
        pVt->getAt(_T("*Active"), vpId);   
        // and open for write
        AcDbViewportTableRecordPointer pOldVTR(vpId, AcDb::kForWrite);   
        // if ok
        if (pOldVTR.openStatus() == Acad::eOk)
        {
          AcGeMatrix3d wcs2dcs;   
          AcGePoint3d newCenter(100,100,0);       
          Wcs2Dcs(pOldVTR.object(), wcs2dcs);   
          newCenter = wcs2dcs*newCenter;   
          // gives position of new pt in DCS wrt view center
          AcGePoint2d oldCenter = pOldVTR->centerPoint();   
            pOldVTR->setCenterPoint(
                        AcGePoint2d(newCenter[X]+oldCenter[X],
                                    newCenter[Y]+oldCenter[Y]));                                   
          // just set the view direction to show that also...
          pOldVTR->setViewDirection(AcGeVector3d(-1,-1,1));   
        }
      }
    }
      // save the changes
    Acad::ErrorStatus es = dwg->saveAs(_T("c:\\temp\\fenton2.dwg"));
  }
}
  /////////////////////////////////////////////////////////////////
void Wcs2Dcs(AcDbViewportTableRecord *pVp, AcGeMatrix3d &resultMat)
{   
  // first get all the data   
  AcGeVector3d viewDirection = pVp->viewDirection();   
  AcGePoint2d centre2d = pVp->centerPoint();   
  AcGePoint3d viewCenter = AcGePoint3d( centre2d.x, centre2d.y, 0);       
  AcGePoint3d viewTarget = pVp->target ();    
  double twistAngle = -pVp->viewTwist();    
  double height = pVp->height();   
  double width = pVp->width();   
  double lensLength = pVp->lensLength();
    // prepare the transformation   
  AcGeVector3d xAxis, yAxis, zAxis;   
  zAxis = viewDirection.normal();   
  xAxis = AcGeVector3d::kZAxis.crossProduct( viewDirection );       
  if( !xAxis.isZeroLength() )
  {       
    xAxis.normalize();       
    yAxis = zAxis.crossProduct( xAxis );   
  }
  else if( zAxis.z < 0 )
  {       
    xAxis = -AcGeVector3d::kXAxis;       
    yAxis = AcGeVector3d::kYAxis;       
    zAxis = -AcGeVector3d::kZAxis;   
  }
  else
  {       
    xAxis = AcGeVector3d::kXAxis;       
    yAxis = AcGeVector3d::kYAxis;       
    zAxis = AcGeVector3d::kZAxis;   
  }       
    AcGeMatrix3d dcs2wcs;   
  // display coordinate system (DCS) to world coordinate system (WCS)      
  // then adjust to the viewCenter   
  dcs2wcs = AcGeMatrix3d::translation( viewCenter - AcGePoint3d::kOrigin);       
  // Then transform for the view direction   
  AcGeMatrix3d matCoords;   
  matCoords.setCoordSystem( AcGePoint3d::kOrigin, xAxis, yAxis, zAxis);       
  dcs2wcs = matCoords * dcs2wcs;       
  // Then adjust for the viewTarget   
  dcs2wcs = AcGeMatrix3d::translation( viewTarget - AcGePoint3d::kOrigin) * dcs2wcs;       
  // Then the twist angle   
  dcs2wcs = AcGeMatrix3d::rotation(twistAngle, zAxis, viewTarget ) * dcs2wcs;       
  AcGeMatrix3d perspMat;  
  if( pVp->perspectiveEnabled())
  {       
    // we do special perspective handling      
    double viewSize = height;          
    double aspectRatio = width / height;              
    double adjustFactor = 1.0 / 42.0;       
    double adjustedLensLength = viewSize * lensLength * sqrt ( 1.0 + aspectRatio * aspectRatio ) * adjustFactor;               
    double eyeDistance = viewDirection.length();       
    double lensDistance = eyeDistance - adjustedLensLength;                       
    double ed = eyeDistance;      
    double ll = adjustedLensLength;      
    double l = lensDistance;               
    perspMat.entry[2][2] = (ll - l ) / ll;      
    perspMat.entry[2][3] = l * ( ed - ll ) / ll;      
    perspMat.entry[3][2] = -1.0 / ll;      
    perspMat.entry[3][3] = ed / ll;  
  }  
    resultMat = perspMat * dcs2wcs.inverse();
}

## 评论

**内容**: nizar akel said...
hi all
i need to open external dwg file and i need to do zoom extents then close it. all this should be done silintly while working on another dwg drawing
thanks alot
nizar
Reply
09/19/2014 at 12:55 AM

---
