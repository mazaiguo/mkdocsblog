---
title: "Create four split modelspace viewports and set different orthographic views"
date: 2015-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Recently, a developer wanted to modify the sample code from here to create split model space viewports and set different orthographic view in each ..."
author: Autodesk
---
# Create four split modelspace viewports and set different orthographic views

发布日期: 2015-08-01

原始链接: https://adndevblog.typepad.com/autocad/2015/08/create-four-split-modelspace-viewports-and-set-different-orthographic-views.html

## 文章内容

By Balaji Ramamoorthy
Recently, a developer wanted to modify the sample code from here to create split model space viewports and set different orthographic view in each of them. Here is a sample code to do that. The below code creates four split modelspace viewports. When creating the new ViewportTableRecords that represent the newly created split viewports, its view parameters are set from the active ViewportTableRecord. This ensures that the ViewportTableRecord is correctly setup for us to set the orthographic view. Finally, each modelspace viewport is zoomed to extents. Here is a screenshot of the resulting viewport arrangement.
 // Create 4 split modelspace viewports, 
 // set different orthographic view direction in each  
 // and zoom to extents. 
 [CommandMethod("SplitMVP" )]
 public  static  void  SplitAndSetViewModelViewports()
 {
     Document doc 
         = Application.DocumentManager.MdiActiveDocument;
     Database db = doc.Database;
       db.UpdateExt(true );
     Extents3d dbExtent 
         = new  Extents3d(db.Extmin, db.Extmax);
       using  (Transaction tr 
         = db.TransactionManager.StartTransaction())
     {
         ViewportTable vt = tr.GetObject(
             db.ViewportTableId, OpenMode.ForWrite) 
             as  ViewportTable;
           ViewportTableRecord vtr1 = tr.GetObject(
             doc.Editor.ActiveViewportId, 
             OpenMode.ForWrite) as  ViewportTableRecord;
           Point2d ll = vtr1.LowerLeftCorner;
         Point2d ur = vtr1.UpperRightCorner;
           vtr1.LowerLeftCorner = ll;
         vtr1.UpperRightCorner = new  Point2d(
             ll.X + (ur.X - ll.X) * 0.5, 
             ll.Y + (ur.Y - ll.Y) * 0.5);
         vtr1.SetViewDirection(OrthographicView.LeftView);
         ZoomExtents(vtr1, dbExtent);
           ViewportTableRecord vtr2 = 
             CreateVTR(vt, vtr1, 
             new  Point2d(ll.X + (ur.X - ll.X) * 0.5, ll.Y), 
             new  Point2d(ur.X, ll.Y + (ur.Y - ll.Y) * 0.5), 
             dbExtent, OrthographicView.RightView);
         vt.Add(vtr2);
         tr.AddNewlyCreatedDBObject(vtr2, true );
           ViewportTableRecord vtr3 = 
             CreateVTR(vt, vtr1, 
             vtr1.UpperRightCorner, ur, 
             dbExtent, OrthographicView.BottomView);
         vt.Add(vtr3);
         tr.AddNewlyCreatedDBObject(vtr3, true );
           ViewportTableRecord vtr4 = 
             CreateVTR(vt, vtr1, 
             new  Point2d(ll.X, ll.Y + (ur.Y - ll.Y) * 0.5), 
             new  Point2d(ll.X + (ur.X - ll.X) * 0.5, ur.Y), 
             dbExtent, OrthographicView.TopView);
         vt.Add(vtr4);
         tr.AddNewlyCreatedDBObject(vtr4, true );
           // Update the display with new tiled viewports 
         doc.Editor.UpdateTiledViewportsFromDatabase();
           // Commit the changes  
         tr.Commit();
     }
 }
   // Create a model space viewport and uses the  
 // view parameters from a reference viewport 
 // before setting the orthographic view and zooming to extents 
 public  static  ViewportTableRecord CreateVTR(
     ViewportTable vt, ViewportTableRecord refVTR, 
     Point2d ll, Point2d ur, Extents3d dbExtent, 
     OrthographicView ov)
 {
     ViewportTableRecord newVTR = new  ViewportTableRecord();
       newVTR.LowerLeftCorner = ll;
     newVTR.UpperRightCorner = ur;
     newVTR.Name = "*Active" ;
       newVTR.ViewDirection = refVTR.ViewDirection;
     newVTR.ViewTwist = refVTR.ViewTwist;
     newVTR.Target = refVTR.Target;
     newVTR.BackClipEnabled = refVTR.BackClipEnabled;
     newVTR.BackClipDistance = refVTR.BackClipDistance;
     newVTR.FrontClipEnabled = refVTR.FrontClipEnabled;
     newVTR.FrontClipDistance = refVTR.FrontClipDistance;
     newVTR.Elevation = refVTR.Elevation;
     newVTR.SetViewDirection(ov);
       ZoomExtents(newVTR, dbExtent);
       return  newVTR;
 }
   public  static  void  ZoomExtents
     (ViewportTableRecord vtr, Extents3d dbExtent)
 {
     //get the screen aspect ratio to  
     // calculate the height and width 
     double  scrRatio = (vtr.Width / vtr.Height);
    //prepare Matrix for DCS to WCS transformation 
     Matrix3d matWCS2DCS 
         = Matrix3d.PlaneToWorld(vtr.ViewDirection);
    //for DCS target point is the origin 
     matWCS2DCS = Matrix3d.Displacement
         (vtr.Target - Point3d.Origin) * matWCS2DCS;
    //WCS Xaxis is twisted by twist angle 
     matWCS2DCS = Matrix3d.Rotation(-vtr.ViewTwist,
                                     vtr.ViewDirection,
                                     vtr.Target
                                 ) * matWCS2DCS;
    matWCS2DCS = matWCS2DCS.Inverse();
    //tranform the extents to the DCS  
     // defined by the viewdir 
  dbExtent.TransformBy(matWCS2DCS);
    //width of the extents in current view 
  double  width 
         = (dbExtent.MaxPoint.X - dbExtent.MinPoint.X);
    //height of the extents in current view 
  double  height 
         = (dbExtent.MaxPoint.Y - dbExtent.MinPoint.Y);
    //get the view center point 
  Point2d center = new  Point2d(
         (dbExtent.MaxPoint.X + dbExtent.MinPoint.X) * 0.5,
   (dbExtent.MaxPoint.Y + dbExtent.MinPoint.Y) * 0.5);
    //check if the width' in current window 
  //if not then get the new height as per the  
     // viewports aspect ratio 
  if  (width > (height * scrRatio))
   height = width / scrRatio;
       vtr.Height = height;
     vtr.Width = height * scrRatio;
     vtr.CenterPoint = center;
 }

## 评论

**内容**: heardle game said...
I appreciate your involvement and counsel in this matter, as I now sense I have a better understanding of the situation.
Reply
09/24/2022 at 08:43 PM

---
**内容**: Pou said...
i just found cool to know more by reading this.
Reply
10/23/2022 at 08:10 PM

---
**内容**: Wordle unlimited said...
I value your involvement and advice in this subject since I feel that I now have a clearer knowledge of the circumstances. Thank you very much
Reply
11/15/2022 at 05:13 AM

---
**内容**: df said...
google cool
Reply
11/27/2022 at 06:40 PM

---
**内容**: papa's freerezia said...
Thank you very much for the useful information. It has been challenging for me to come up with numerous questions about this subject. I'll be right behind you!
Reply
12/15/2022 at 12:09 AM

---
