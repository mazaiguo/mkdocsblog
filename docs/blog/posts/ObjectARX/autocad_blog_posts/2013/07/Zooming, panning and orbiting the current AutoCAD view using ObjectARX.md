---
title: "Zooming, panning and orbiting the current AutoCAD view using ObjectARX"
date: 2013-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
description: "Our colleauge Kean has produced a blog on zooming, panning, orbiting the current view in .NET. I am writing the code in ObjectARX. The basic workfl..."
author: Autodesk
---
# Zooming, panning and orbiting the current AutoCAD view using ObjectARX

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/zooming-panning-and-orbiting-the-current-autocad-view-using-objectarx.html

## 文章内容

By Xiaodong Liang
Our colleauge Kean has produced a blog on zooming, panning, orbiting the current view in .NET. I am writing the code in ObjectARX. The basic workflow for zooming, panning, orbiting is similar:
1. get he current view record
2. adjust its parameters. e.g.
   zooming: adjust height and width with a factor
   panning: adjust the view center
   orbiting: adjust the view direction along an axis.
3. update the current view with the updated view record.
static void panView()
{
    AcDbDatabase *pDb =
    acdbHostApplicationServices()->workingDatabase();  
         acedVports2VportTableRecords();
       //get the active viewport object
      AcDbViewportTable *pVpT = NULL;
      AcDbViewportTableRecord *pActVp = NULL; 
      //get the *Active view port
      pDb->getViewportTable(pVpT,AcDb::kForRead);
      pVpT->getAt(_T("*Active"),pActVp,AcDb::kForWrite);
      pVpT->close();
        //get the view center point
        //assume we need to pan the view along X & Y in 10
      double panStep = 10;
      AcGePoint2d mCentPt = pActVp->centerPoint();
      mCentPt.x += panStep;
      mCentPt.y += panStep;
        //set the view center
      pActVp->setCenterPoint(mCentPt);
      //close the Active viewport
      pActVp->close();  
      //update the viewport
      acedVportTableRecords2Vports(); 
}
  static void zoomView()
{
    AcDbDatabase *pDb =
    acdbHostApplicationServices()->workingDatabase();  
         acedVports2VportTableRecords();
       //get the active viewport object
      AcDbViewportTable *pVpT = NULL;
      AcDbViewportTableRecord *pActVp = NULL; 
      //get the *Active view port
      pDb->getViewportTable(pVpT,AcDb::kForRead);
      pVpT->getAt(_T("*Active"),pActVp,AcDb::kForWrite);
      pVpT->close();  
        //assume we need to zoom the view out in scaling 10
      double zoomFactor = 10;
        pActVp->setHeight(pActVp->height() * zoomFactor);
      pActVp->setWidth(pActVp->width() * zoomFactor); 
        //close the Active viewport
      pActVp->close();  
      //update the viewport
      acedVportTableRecords2Vports(); 
}
  static void orbitView()
{
    AcDbDatabase *pDb =
    acdbHostApplicationServices()->workingDatabase();  
         acedVports2VportTableRecords();
       //get the active viewport object
      AcDbViewportTable *pVpT = NULL;
      AcDbViewportTableRecord *pActVp = NULL; 
      //get the *Active view port
      pDb->getViewportTable(pVpT,AcDb::kForRead);
      pVpT->getAt(_T("*Active"),pActVp,AcDb::kForWrite);
      pVpT->close();  
            //assume we need to orbit the view direction
      // along (1,0,0) in angle 30 degree.
        AcGeVector3d oOldDir =  pActVp->viewDirection();
      AcGeMatrix3d oM;
      oM.setToRotation(30 * 3.1415926 / 180,AcGeVector3d(1,0,0),AcGePoint3d::kOrigin);
      oOldDir.transformBy(oM);
      pActVp->setViewDirection(oOldDir);      
        //close the Active viewport
      pActVp->close();  
      //update the viewport
      acedVportTableRecords2Vports(); 
}

## 评论

**内容**: newman said...
The Autodesk function "acedVportTableRecords2Vports()" is slowly. It is performed for more than 10 seconds. It's is not good for C++. Do you have another function for zooming View ?
Reply
10/04/2016 at 09:11 AM

---
**内容**: newman said...
I find this. It's very quickly.
AcDbViewTableRecord mVTR;
AcGePoint2d max_2d(10,10);
AcGePoint2d min_2d(0,0);
mVTR.setCenterPoint( min_2d + (max_2d - min_2d) / 2.0 );
mVTR.setHeight(10);
acedSetCurrentView(&mVTR, NULL);
Reply
10/04/2016 at 09:52 AM

---
