---
title: "Zooming to drawing extents for a viewport without sending commands"
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "How to do zoom drawing extents for a viewport without sending commands?"
author: Autodesk
---
# Zooming to drawing extents for a viewport without sending commands

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/zooming-to-drawing-extents-for-a-viewport-without-sending-commands.html

## 文章内容

By Balaji Ramamoorthy
Issue
How to do zoom drawing extents for a viewport without sending commands?
Solution
For every viewport, you need three things to zoom correctly.
1. Its View center ( using setViewCenter( ) ) - and not its center point. View center is the 2D point that you center your view on, while center point (using setCenterPoint( ) ) is the viewport's center point in PaperSpace Layout. Center point is simply used to position viewports in a layout. The view center would depend on the drawing's extent.
2. View Direction.
3. View's height, and not the Viewport's height. Viewport's width and height would apply to paper space. The width and height once again will depend on draiwing's extent.
The following code creates 3 layouts that is zoomed to drawing's extents programatically. They are placed arbitratily in paper space layout, but you may set your own center point and view's height. The view's width is set in the code to be proportional the extent's windows width:height ratio. If you don't do this, the layout won't be wide enough to accomodate the whole drawing although it may be tall enough!
static void AdskTestCommand()
{
    AcDbDatabase *pDbUse
            = acdbHostApplicationServices()->workingDatabase();
    AcDbDictionary *pNOD;
    Acad::ErrorStatus eStat;
    eStat = pDbUse->getNamedObjectsDictionary(pNOD, AcDb::kForRead);
      if (eStat != Acad::eOk)
        return;
      AcDbObjectId idDict;
    eStat = pNOD->getAt(L"ACAD_LAYOUT", idDict);
    pNOD->close();
    if (eStat != Acad::eOk)
        return;
      AcDbDictionary *pDict;
    eStat = acdbOpenObject(pDict, idDict, AcDb::kForRead);
    if (eStat != Acad::eOk)
        return;
      AcDbObjectId idLyt;
    eStat = pDict->getAt(L"Layout1", idLyt);
    pDict->close();
      AcApLayoutManager *pLayM
        =(AcApLayoutManager*)acdbHostApplicationServices()->layoutManager();
    pLayM->setCurrentLayout(L"Layout1");
      AcDbLayout* pLyt;
    if (acdbOpenObject(pLyt, idLyt, AcDb::kForRead) != Acad::eOk)
       return;
    AcDbObjectId idBtr = pLyt->getBlockTableRecordId();
    pLyt->close();
      AddViewPort(idBtr, AcGePoint3d(2,5,0), AcGeVector3d( 0,0,1));
    //for sw-iso
    AddViewPort(idBtr, AcGePoint3d(5,5,0), AcGeVector3d( -1,-1,1));
    //for ne-iso
    AddViewPort(idBtr, AcGePoint3d(8,5,0), AcGeVector3d( 1,1,1)); 
}
  // Gets a rectangular window in viewport's x-y plane
// that represents drawing's extents
static void getUcsExts(AcGePoint2d &maxExt,
    AcGePoint2d &minExt,
    AcGeMatrix3d UcsMat )
{
    AcDbDatabase* pDb
            = acdbHostApplicationServices()->workingDatabase();
    AcGePoint3d max = pDb->extmax(), min = pDb->extmin();
      // Make extents box
    AcDbExtents ext(min, max);
      // Transform extents to UCS
    ext.transformBy(UcsMat);
      max = ext.maxPoint();
    min = ext.minPoint();
      maxExt[X] = max[X];
    maxExt[Y] = max[Y];
      minExt[X] = min[X];
    minExt[Y] = min[Y];
}
  static void SetViewportExtents(AcDbViewport *pVp,
      AcGePoint2d &max,
      AcGePoint2d &min, 
      double height)
{
    // Set View center
    AcGePoint2d ViewCenter;
    ViewCenter[X] = (max[X]+min[X])/2.0;
    ViewCenter[Y] = (max[Y]+min[Y])/2.0;
    pVp->setViewCenter(ViewCenter);
      //set View's height + 0.5
    pVp->setViewHeight((max[Y]-min[Y])+0.5);
      // Get width proportional to height
    double WidthHeightRatio = (max[X]-min[X])/(max[Y]-min[Y]);
    pVp->setHeight(height);
      //The viewport's width maintains the extent windows proportions
    pVp->setWidth(height * WidthHeightRatio);
}
  // Get WCS to UCS transformation matrix
static void getTrnsMatrix (AcGeMatrix3d &ucsMatrix,
     AcGeVector3d ViewDirection, AcGePoint3d origin)
{
    AcGePlane XYPlane(origin, ViewDirection);
    ucsMatrix.setToWorldToPlane(XYPlane);
}
  void AddViewPort(AcDbObjectId idToBtr,
     AcGePoint3d centerPoint,
     AcGeVector3d vecVPoint)
{
    AcDbDatabase* pDb
          = acdbHostApplicationServices()->workingDatabase();
    AcDbViewport* pVp = new AcDbViewport;
      // Append new viewport to paper space
    AcDbBlockTableRecord *pBTR;
    if (acdbOpenObject(pBTR, idToBtr, AcDb::kForWrite) != Acad::eOk)
    {
        acutPrintf(L"\nCannot access paper space.");
        delete pVp;
        return;
    }
     if (pBTR->appendAcDbEntity( pVp) != Acad::eOk)
   {
      acutPrintf(L"\nCannot append viewport to paper space.");
      pBTR->close();
      delete pVp;
      return;
   }
     pBTR->close();
     pVp->setCenterPoint(centerPoint);
     //Set View direction
   pVp->setViewDirection(vecVPoint);
     //Assume target point is WCS (0,0,0)
   AcGeMatrix3d ucsMatrix;
   getTrnsMatrix (ucsMatrix, vecVPoint,AcGePoint3d(0,0,0));
     // Get a rectangular window in viewport's x-y plane
   // that represents drawing's extents
   AcGePoint2d maxExt, minExt;
   getUcsExts(maxExt, minExt, ucsMatrix);
     // Here 2 is the view's height. You may change it to any height
   SetViewportExtents(pVp, maxExt, minExt, 2);
   pVp->setOn();
   pVp->close();
}
Posted at 11:12 PM in AutoCAD, Balaji Ramamoorthy, ObjectARX | Permalink

## 评论

**内容**: Nenad said...
Dear Sir,
I have one question. I am trying to show only some entities in AcDbViewport. In my model I have several entities and I need to create new AcDbLayout that will display only some entities, not all. I have command that creates new AcDbLayout. Then I tried to manipulate with AcDbLayout::database(), to remove Ids of those entities that shouldn't be displayed, but it seems that I can't do it this way? Then I tried to use this code, just to change AcDbViewport dimensions so it will show only entities that I want. I calculated their rectangular window in Model space and tried to set AcDbViewport to show only that. I set viewport's ViewCenter and ViewHeight to center and height of that rectangle but it didn't work. It seems like AutoCad automatically changed them so all entities could be displayed?
Could you tell me is there any way to show only entities that I want to display?
Reply
10/31/2014 at 03:38 AM

---
**内容**: Balaji said...
Hi Nenad,
You can try assigning different layers for the entities that you want shown / hidden and then use freeze layer specific to a viewport. Please try the code in this blog post :
http://adndevblog.typepad.com/autocad/2012/05/freeze-and-thaw-layers-in-a-paperspace-viewport.html
Regards,
Balaji
Reply
10/31/2014 at 05:06 AM

---
