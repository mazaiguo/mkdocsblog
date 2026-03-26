---
title: "How to programmatically mimic the vpoint command?"
date: 2012-08-01
categories:
  - AutoCAD C++
tags:
  - C++
description: "I use the following code to change the view:"
author: Autodesk
---
# How to programmatically mimic the vpoint command?

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/how-to-programmatically-mimic-the-vpoint-command.html

## 文章内容

By Xiaodong Liang
Issue
I use the following code to change the view:
  ads_point pt = {1,1,1};
  acedCommand(RTSTR, "vpoint", RTSTR, "non",
              RT3DPOINT, pt, RTNONE);

Why doesn't the following ARX code change the view?
AcDbViewportTable *pTable;
  acdbHostApplicationServices()->workingDatabase()->getViewportTable(
        pTable,
        AcDb::kForRead));   
AcDbViewportTableRecord *pRecord;
pTable->getAt("*ACTIVE", pRecord, AcDb::kForWrite);
AcGeVector3d direction(1, 1, 1);
pRecord->setViewDirection(direction);
pRecord->close();
pTable->close();
Solution
When using ARXDBG to check the result of your code, the viewdir is changed for the active viewport table record. Note that viewdir system variable is not changed and the actual view does not change, either.
What you can do is to set up a AcDbViewTableRecord object, then use acedSetCurrentView() to set the current view according to the object's settings.
The following code mimics what the VPOINT command does:
  static void simulateVpointCmd()
{
    AcDbViewportTableRecordPointer pRecord(
        acedActiveViewportId(),AcDb::kForWrite );
      Acad::ErrorStatus es = pRecord.openStatus();
    assert(es == Acad::eOk);
    pRecord->setViewDirection(AcGeVector3d(1,1,1));
      AcDbViewTableRecord vtr;
    vtr.setBackClipDistance(pRecord->backClipDistance());
    vtr.setBackClipEnabled(pRecord->backClipEnabled());
    vtr.setElevation(pRecord->elevation());
    vtr.setFrontClipAtEye(pRecord->frontClipAtEye());
      vtr.setFrontClipDistance(pRecord->frontClipDistance());
    vtr.setLensLength(pRecord->lensLength());
    vtr.setPerspectiveEnabled(pRecord->perspectiveEnabled());
    vtr.setRenderMode(pRecord->renderMode());
      vtr.setTarget(pRecord->target());
      vtr.setUcs(pRecord->ucsName());
    vtr.setViewDirection(pRecord->viewDirection());
    // viewtwist in vpoint is always 0
    // if you set it correctly, you can't get a result
    // that is similar to vpoint's
    vtr.setViewTwist(pRecord->viewTwist());
      vtr.setCenterPoint(pRecord->centerPoint());
    vtr.setHeight(pRecord->height());
    vtr.setWidth(pRecord->width());
      acedSetCurrentView(&vtr, NULL);
    // this is tweaking it to make it look like the result of vpoint cmd
    acedCommand(RTSTR, L"zoom", RTSTR, L"extents", RTNONE);
}

