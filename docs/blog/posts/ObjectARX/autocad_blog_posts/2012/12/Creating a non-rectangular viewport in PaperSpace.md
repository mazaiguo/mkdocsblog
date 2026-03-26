---
title: "Creating a non-rectangular viewport in PaperSpace"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "AcDbViewport::setNonRecClipEntityId() can be used  to associate a viewport with an entity and enabling non-rectangular clipping is done through AcD..."
author: Autodesk
---
# Creating a non-rectangular viewport in PaperSpace

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/creating-a-non-rectangular-viewport-in-paperspace.html

## 文章内容

By Gopinath Taget
AcDbViewport::setNonRecClipEntityId() can be used  to associate a viewport with an entity and enabling non-rectangular clipping is done through AcDbViewport::setNonRectClipOn()
For a clipping entity to be valid, it must be contained in the same paperspace as the viewport entity and should be one of the entities as explained with ObjectARX help file. Please see the documentation for AcDbViewport::setNonRecClipEntityId() method for more details.
The sample code snippet below creates a non-rectangular viewport of type circle and assign a specified view to the same:
void fCreateNonRectangularViewPort()
{
 //____create the circle
ads_point centerPoint;
 if(RTNORM != acedGetPoint(NULL,
  L"\nEnter the Viewport center point:",centerPoint))
  return;
ads_real radius;
 if(RTNORM != acedGetDist(centerPoint,
  L"\nEnter the radius of the Viewport:",&radius))
  return;
ACHAR viewName[133];
    if (RTNORM != ads_getstring(0,
  L"\nEnter name of view to use: ", viewName))
        return;
  AcDbCircle* pCircle = new AcDbCircle;
 //____assigning the center point
pCircle->setCenter(AcGePoint3d(centerPoint[X],centerPoint[Y],0));
pCircle->setRadius(radius);
AcDbBlockTable *pTable;
AcDbBlockTableRecord *pRecord;
 if (Acad::eOk != acdbHostApplicationServices()->
  workingDatabase()->getBlockTable(pTable, AcDb::kForRead)) {
  acutPrintf(L"\nCannot get block table.");
  delete pCircle;
  return;
}
 if (Acad::eOk != pTable->getAt(ACDB_PAPER_SPACE,
  pRecord, AcDb::kForWrite)) {
  acutPrintf(L"\nCannot access paper space.");
  pTable->close();
  delete pCircle;
  return;
}
pTable->close();
AcDbObjectId circleId;
 if (Acad::eOk != pRecord->appendAcDbEntity(circleId, pCircle)) {
  acutPrintf(L"\nCannot append circle to paper space.");
  pRecord->close();
  delete pCircle;
  return;
}
pRecord->close();
pCircle->close();
   //____create the viewport entity
AcDbViewport *pViewport = new AcDbViewport;
 //___assign the center point of circle
 //(since the value is known directly assigning)
pViewport->setCenterPoint(AcGePoint3d(centerPoint[X],
  centerPoint[Y],0));    
 //___Append new viewport to the paper space
 if (Acad::eOk != acdbHostApplicationServices()->
  workingDatabase()->getBlockTable(pTable, AcDb::kForRead)) {
  acutPrintf(L"\nCannot get block table.");
  delete pViewport;
  return;
}
 if (Acad::eOk != pTable->getAt(ACDB_PAPER_SPACE,
  pRecord, AcDb::kForWrite)) {
  acutPrintf(L"\nCannot access paper space.");
  pTable->close();
  delete pViewport;
  return;
}
pTable->close();
AcDbObjectId viewportId;
 if (Acad::eOk != pRecord->appendAcDbEntity(viewportId,
  pViewport)) {
  acutPrintf(L"\nCannot append viewport to paper space.");
  pRecord->close();
  delete pViewport;
  return;
}
pRecord->close();
pViewport->setNonRectClipEntityId(circleId);
pViewport->setNonRectClipOn();
   //___set the view
AcDbViewTable *pViewTable;
AcDbViewTableRecord *pView;
 if (Acad::eOk != acdbHostApplicationServices()->
  workingDatabase()->getViewTable(pViewTable,
  AcDb::kForRead)) {
  acutPrintf(L"\nCannot get view table.");
  pViewport->close();
  return;
}
   if (Acad::eOk != pViewTable->getAt(viewName,
  pView, AcDb::kForRead)) {
  acutPrintf(L"\nCannot access view '%s'.", viewName);
  pViewport->close();
  pViewTable->close();
  return;
}
pViewTable->close();
   if (acedSetCurrentView(pView, pViewport)!=Acad::eOk)
  acutPrintf(L"\nFailed to set view");
  pViewport->setOn();
pView->close();
pViewport->close();
   //update the screen such the viewport is updated
acedCommand(RTSTR,L"_REGEN",RTNONE,0);
  }

## 评论

**内容**: nizar said...
hi
how can you use
pViewTable->getAt(viewName,
if you didnt use viewName before?
this can cant be reach the acedSetCurrentView(...
nizar
Reply
02/09/2013 at 08:28 AM

---
