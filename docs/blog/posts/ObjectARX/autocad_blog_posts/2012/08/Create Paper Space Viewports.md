---
title: "Create Paper Space Viewports"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Dimension
description: "To create a new viewport in paper space, like MVIEW command, perform the following steps:"
author: Autodesk
---
# Create Paper Space Viewports

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/create-paper-space-viewports.html

## 文章内容

By Augusto Goncalves
To create a new viewport in paper space, like MVIEW command, perform the following steps:
1. Create a new object of type AcDbViewport.
2. Set the view coordinates (with setWidth(), setHeight() and setCenterPoint()).
3. Append the new viewport to the paper space.
4. Get the view the user specified (AcDbViewTableRecord).
5. Set this view on the new viewport with acdbSetCurrentView().
6. Activate the viewport with AcDbViewport::setOn().
NOTE: The AcDbViewport::setOn() function only works if your command has been registered without the ACRX_CMD_TRANSPARENT flag. If this flag is set,
AcDbViewport::setOn() returns with eCommandWasInProgress and you cannot activate the viewport until you set tilemode to 1 and back to 0.
The following code demonstrates how to do this:
// Only works in paperspace
AcDbObjectId mCurViewportId = acedGetCurViewportObjectId();
  if (mCurViewportId == AcDbObjectId::kNull)
{
  acutPrintf(_T("\nCommand only works in paperspace."));
  return;
}
  AcDbViewport *pCurViewport;
if (Acad::eOk != acdbOpenObject(pCurViewport,mCurViewportId,
  AcDb::kForRead))
{
  acutPrintf(_T("\nCannot get active viewport."));
  return;
}
  if (pCurViewport->number() != 1)
{
  acutPrintf(_T("\nCommand only works in paperspace."));
  pCurViewport->close();
  return;
}
pCurViewport->close();
  // Ask for the position
ads_point pt1,pt2;
  if (RTNORM != acedGetPoint(NULL,
  _T("\nSelect first corner: "), pt1))
  return;
  if (RTNORM != acedGetCorner(pt1,
  _T("\nSelect second corner: "), pt2))
  return;
  // Ask for the view to use
ACHAR mViewName[133];
  if (RTNORM != acedGetString(0,
  _T("\nEnter name of view to use: "), mViewName))
  return;
// Create new viewport
AcDbViewport *pViewport = new AcDbViewport;
pViewport->setWidth(fabs(pt2[X] - pt1[X]));
pViewport->setHeight(fabs(pt2[Y] - pt1[Y]));
pViewport->setCenterPoint(AcGePoint3d(
  pt1[X] + (pt2[X] - pt1[X]) / 2,
  pt1[Y] + (pt2[Y] - pt1[Y]) / 2,
  pt1[Z]));
  // Append new viewport to paper space
AcDbBlockTable *pTable;
AcDbBlockTableRecord *pPsBTR;
  if (Acad::eOk != acdbHostApplicationServices()->
  workingDatabase()->getBlockTable(pTable, AcDb::kForRead))
{
  acutPrintf(_T("\nCannot get block table."));
  delete pViewport;
  return;
}
  if (Acad::eOk != pTable->getAt(ACDB_PAPER_SPACE, pPsBTR,
  AcDb::kForWrite))
{
  acutPrintf(_T("\nCannot access paper space."));
  pTable->close();
  delete pViewport;
  return;
}
pTable->close();
  AcDbObjectId mViewPortId;
if (Acad::eOk != pPsBTR->appendAcDbEntity(mViewPortId, pViewport))
{
  acutPrintf(_T("\nCannot append viewport to paper space."));
  pPsBTR->close();
  delete pViewport;
  return;
}
pPsBTR->close();
pViewport->setOn();
  // Set the view
AcDbViewTable *pViewTable;
AcDbViewTableRecord *pViewTR;
  if (Acad::eOk != acdbHostApplicationServices()->
  workingDatabase()->getViewTable(pViewTable, AcDb::kForRead))
{
  acutPrintf(_T("\nCannot get view table."));
  pViewport->close();
  return;
}
  if (Acad::eOk != pViewTable->getAt(mViewName,
  pViewTR, AcDb::kForRead))
{
  acutPrintf(_T("\nCannot access view '%s'."), mViewName);
  pViewport->close();
  pViewTable->close();
  return;
}
pViewTable->close();
  if (acedSetCurrentView(pViewTR, pViewport)!=Acad::eOk)
  acutPrintf(_T("\nFailed to set view"));
  // Close the objects
pViewTR->close();
pViewport->close();

## 评论

**内容**: David said...
Hello Augusto,
Thanks for Post
Can you please show us how to create a Non Rectangular view port and assign Custom-Scale to it.
Kean Walmsley shows how to create. But didn't show how to assing custom scale to it. And I did all I could and it doesn't work.
Thanks
Reply
12/11/2012 at 10:42 AM

---
