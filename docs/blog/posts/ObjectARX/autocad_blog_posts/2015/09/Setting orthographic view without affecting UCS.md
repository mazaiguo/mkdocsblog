---
title: "Setting orthographic view without affecting UCS"
date: 2015-09-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - UCS
description: "Here is a previous blog post on a similar topic for setting an orthographic view. The limitation with the code snippet posted in that blog post is ..."
author: Autodesk
---
# Setting orthographic view without affecting UCS

发布日期: 2015-09-01

原始链接: https://adndevblog.typepad.com/autocad/2015/09/setting-orthographic-view-without-affecting-ucs.html

## 文章内容

By Balaji Ramamoorthy
Here is a previous blog post on a similar topic for setting an orthographic view. The limitation with the code snippet posted in that blog post is that it modifies the active ViewportTableRecord and after the view change, the name of current UCS does not get displayed under the View Cube. When changing the view using AutoCAD's View Cube and switching to Top View, it only changes the view without affecting the UCS. Also, the X and Y axes are aligned horizontally and vertically. To get a similar behavior using the API, here is a code snippet that sets the viewing direction along +Z axis and aligns the X and Y axes just as the View Cube does.
 [DllImport("accore.dll" , 
     CallingConvention = CallingConvention.Cdecl, 
     EntryPoint = "acedTrans" )]
 private  static  extern  int  acedTrans(
     double [] point, 
     IntPtr fromRb, 
     IntPtr toRb, 
     int  disp, 
     double [] result);
    [CommandMethod("SetViewDir" )]
 public  static  void  SetViewDirMethod()
 {
     Document doc 
         = Application.DocumentManager.MdiActiveDocument;
     Database db = doc.Database;
     Editor ed = doc.Editor;
       Matrix3d ucs = ed.CurrentUserCoordinateSystem;
     using  (Transaction tr 
         = db.TransactionManager.StartTransaction())
     {
         ViewportTable vt = tr.GetObject(
             db.ViewportTableId, 
             OpenMode.ForWrite) as  ViewportTable;
         ViewportTableRecord activeVTR = 
             tr.GetObject(ed.ActiveViewportId, 
             OpenMode.ForRead) as  ViewportTableRecord;
         using  (ViewTableRecord vtr = new  ViewTableRecord())
         {
             vtr.Target = activeVTR.Target;
             vtr.ViewDirection = activeVTR.ViewDirection;
             vtr.Height = activeVTR.Height;
             vtr.CenterPoint = activeVTR.CenterPoint;
                                   vtr.ViewDirection = ucs.CoordinateSystem3d.Zaxis;
               ed.SetCurrentView(vtr);
         }
         tr.Commit();
     }
       ucs = ed.CurrentUserCoordinateSystem;
       double [] resVec = new  double [] { 0, 0, 0 };
     ResultBuffer rbFrom
         = new  ResultBuffer(new  TypedValue(5003, 0));
     ResultBuffer rbTo 
         = new  ResultBuffer(new  TypedValue(5003, 2));
       Vector3d yAxisUCS = ucs.CoordinateSystem3d.Yaxis;
     int  res = acedTrans(
         yAxisUCS.ToArray(),
         rbFrom.UnmanagedObject,
         rbTo.UnmanagedObject,
         1,
         resVec
     );
     Vector3d yAxisDCS 
         = new  Vector3d(resVec[0], resVec[1], resVec[2]);
       double  twistAngle 
         = (Math.PI * 0.5) 
         - Math.Atan2(yAxisDCS.Y, yAxisDCS.X);
     using  (ViewTableRecord vtr 
         = doc.Editor.GetCurrentView())
     {
         vtr.ViewTwist = twistAngle;
         ed.SetCurrentView(vtr);
     }
 }
  Here is a screenshot of the View cube before and after the View change while retaining the UCS :

