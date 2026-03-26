---
title: "Create new ViewTableRecord with camera and target"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - C#
description: "This C# example prompts for the target and camera positions. The camera position can be found by passing the direction vector of the ViewTableRecor..."
author: Autodesk
---
# Create new ViewTableRecord with camera and target

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/create-new-viewtablerecord-with-camera-and-target.html

## 文章内容

By Augusto Goncalves
This C# example prompts for the target and camera positions. The camera position can be found by passing the direction vector of the ViewTableRecord to the add method of the Point3d target.
[CommandMethod("sampleCameraView", CommandFlags.Transparent)]
public static void CmdViewCamera()
{
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    // select the view target
  PromptPointOptions ppoView =
    new PromptPointOptions("\nEnter view target: ");
  PromptPointResult pprView = ed.GetPoint(ppoView);
  if (pprView.Status != PromptStatus.OK) return;
  Point3d viewPoint = pprView.Value;
    // select the camera point
  PromptPointOptions ppoCamera =
    new PromptPointOptions("\nEnter point for camera: ");
  PromptPointResult pprCamera = ed.GetPoint(ppoCamera);
  if (pprView.Status != PromptStatus.OK) return;
  Point3d cameraPoint = pprView.Value;
    // create the
  ViewTableRecord viewTBR = new ViewTableRecord();
  viewTBR.Target = viewPoint;
  viewTBR.ViewDirection =
    viewPoint.GetVectorTo(cameraPoint);
  viewTBR.Height = 50.0;
  viewTBR.CenterPoint = Point2d.Origin;
    // apply the new view
  ed.SetCurrentView(viewTBR);
  #if DEBUG
  // for debug...
  // http://msdn.microsoft.com/en-us/library/4y6tbswk.aspx
  Point3d cameraPoint3d = viewTBR.Target.Add(viewTBR.ViewDirection);
  ed.WriteMessage("\nCamera X = {0:0.00}", cameraPoint3d.X);
  ed.WriteMessage("\nCamera Z = {0:0.00}", cameraPoint3d.Y);
  ed.WriteMessage("\nCamera Z = {0:0.00}", cameraPoint3d.Z);
#endif
}

