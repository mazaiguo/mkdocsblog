---
title: "Set model viewport's camera/eye, target, view width, view height"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I want to set the camera, target and field of view in a model viewport precisely to focus on certain objects in perspective view. I tried various w..."
author: Autodesk
---
# Set model viewport's camera/eye, target, view width, view height

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/set-model-viewports-cameraeye-target-view-width-view-height.html

## 文章内容

By Adam Nagy
I want to set the camera, target and field of view in a model viewport precisely to focus on certain objects in perspective view. I tried various ways but it was never exactly what I wanted.
Solution
In the attached drawing (Download Circles) we have three circles red (r = 10), green (r = 20) and blue (r = 30). They are parallel and their center points are along the same line.
Let's say we want to place the camera in the center of the red circle and then focus on the green circle. You could use the AcGsView associated with the current model view and set that. The position sets the camera position and target sets the target. Since the circle's plane is parallel with the display's plane therefore we do not have to convert the circle's extents from WCS to DCS. The field width and height is the view's extent in the plane that is defined by the target point and the view direction. So if you set the target point to the green circle's center point, then the field width and height can be set based on the circle's diameter.
When running the sample first select the red circle's center then the green circle's centre.
static void TransformTest_SetModelView(void)
{
  AcDbDatabase * pDb =
    acdbHostApplicationServices()->workingDatabase();
    if (!pDb->tilemode())
  {
    acutPrintf(
      L"\nThis command is only for Model space (i.e tilemode)\n");
    return;
  }
    AcGePoint3d ptCamera;
  if (RTNORM != acedGetPoint(
    NULL, L"\nSelect camera point", asDblArray(ptCamera)))
    return;
    AcGePoint3d ptTarget;
  if (RTNORM != acedGetPoint(
    NULL, L"\nSelect target point", asDblArray(ptTarget)))
    return;
    resbuf cvport;
  acedGetVar(L"CVPORT", &cvport);
    AcGsView * view = acgsGetGsView(cvport.resval.rint, true); 
    double aspectRatio = view->fieldWidth() / view->fieldHeight();
  double newWidth, newHeight;
  if (aspectRatio > 1)
  {
    // The height of the green circle we want to include in
    // the picture is 40
    newHeight = 40;
    newWidth = newHeight * aspectRatio;
  }
  else
  {
    newWidth = 40;
    newHeight = newWidth / aspectRatio;
  }
    view->setView(
    ptCamera,
    ptTarget,
    AcGeVector3d::kZAxis,
    newWidth,
    newHeight,
    AcGsView::kPerspective);
  view->update();
    acgsSetViewParameters(cvport.resval.rint, view, true, true);
}
You could also achieve the same using AcDbViewTableRecord and acedSetCurrentView:
static void TransformTest_SetModelView2(void)
{
  AcDbDatabase * pDb =
    acdbHostApplicationServices()->workingDatabase();
    if (!pDb->tilemode())
  {
    acutPrintf(
      L"\nThis command is only for Model space (i.e tilemode)\n");
    return;
  }
    AcGePoint3d ptCamera;
  if (RTNORM != acedGetPoint(NULL,
    L"\nSelect camera point", asDblArray(ptCamera)))
    return;
    AcGePoint3d ptTarget;
  if (RTNORM != acedGetPoint(NULL,
    L"\nSelect target point", asDblArray(ptTarget)))
    return;
    Acad::ErrorStatus err = acedVports2VportTableRecords();
  {
    AcDbViewportTableRecordPointer
      ptrVp(acedActiveViewportId(), AcDb::kForRead);
      // Copy data from the ViewportTableRecord
    AcDbViewTableRecord vtr;   
    vtr.setBackClipDistance(ptrVp->backClipDistance()); 
    vtr.setBackClipEnabled(ptrVp->backClipEnabled());  
    vtr.setElevation(ptrVp->elevation());  
    vtr.setFrontClipAtEye(ptrVp->frontClipAtEye());  
    vtr.setFrontClipDistance(ptrVp->frontClipDistance()); 
    vtr.setPerspectiveEnabled(ptrVp->perspectiveEnabled()); 
    vtr.setRenderMode(ptrVp->renderMode()); 
    vtr.setUcs(ptrVp->ucsName());  
    vtr.setViewTwist(ptrVp->viewTwist());   
    vtr.setCenterPoint(ptrVp->centerPoint()); 
    vtr.setLensLength(ptrVp->lensLength());  
      // The main settings
    double aspectRatio = vtr.width() / vtr.height();
    double newWidth, newHeight;
    if (aspectRatio > 1)
    {
      // The height of the green circle we want to include in
      // the picture is 40
      newHeight = 40;
      newWidth = newHeight * aspectRatio;
    }
    else
    {
      newWidth = 40;
      newHeight = newWidth / aspectRatio;
    }
    vtr.setWidth(newWidth);
    vtr.setHeight(newHeight);
    vtr.setTarget(ptTarget);
    vtr.setViewDirection(ptCamera - ptTarget); 
      acedSetCurrentView(&vtr, NULL);
  }
}

