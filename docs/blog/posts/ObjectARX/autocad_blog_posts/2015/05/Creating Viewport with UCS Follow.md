---
title: "Creating Viewport with UCS Follow"
date: 2015-05-01
categories:
  - AutoCAD
tags:
  - UCS
description: "Here is a sample code to create a viewport with UCS Follow turned on. This should ensure that the viewport displays the plan based on the UCS whene..."
author: Autodesk
---
# Creating Viewport with UCS Follow

发布日期: 2015-05-01

原始链接: https://adndevblog.typepad.com/autocad/2015/05/creating-viewport-with-ucs-follow.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to create a viewport with UCS Follow turned on. This should ensure that the viewport displays the plan based on the UCS whenever it changes.
 [CommandMethod("CreateVP",
     CommandFlags.NoTileMode)]
 public  void CreateVPMethod()
 {
     Document doc 
     = Application.DocumentManager.MdiActiveDocument;
       Database db = doc.Database;
     Editor ed = doc.Editor;
       ObjectId layoutId = LayoutManager.Current.GetLayoutId
                 (LayoutManager.Current.CurrentLayout);
           using  (Transaction Tx 
         = db.TransactionManager.StartTransaction())
     {
         Layout LayoutDest 
         = Tx.GetObject(layoutId, OpenMode.ForRead) 
         as  Layout;
           BlockTableRecord btrDest 
         = Tx.GetObject(LayoutDest.BlockTableRecordId, 
         OpenMode.ForWrite) as  BlockTableRecord;
           ViewportTable vt 
         = Tx.GetObject(db.ViewportTableId, OpenMode.ForRead)
         as  ViewportTable;
           ViewportTableRecord vtr 
         = Tx.GetObject(vt["*Active"], OpenMode.ForRead) 
         as  ViewportTableRecord;
           UcsTable ucsTbl 
         = Tx.GetObject(db.UcsTableId, OpenMode.ForRead) 
         as  UcsTable;
           if  (vtr != null)
         {
             Autodesk.AutoCAD.DatabaseServices.Viewport vpNew 
             = new  Autodesk.AutoCAD.DatabaseServices.Viewport();
               vpNew.SetDatabaseDefaults();
             vpNew.Width = 6.0;
             vpNew.Height = 5.0;
             vpNew.CenterPoint = new  Point3d(3.25, 3, 0);
             if  (ucsTbl.Has("myucs"))
             {
                 ObjectId ucsId = ucsTbl["myucs"];
                 vpNew.SetUcs(ucsId);
             }
             vpNew.StandardScale 
             = StandardScaleType.Scale1To1;
             vpNew.ViewCenter = vtr.CenterPoint;
             vpNew.ViewHeight = vtr.Height;
             vpNew.ViewDirection = vtr.ViewDirection;
             vpNew.ViewTarget = vtr.Target;
             vpNew.TwistAngle = vtr.ViewTwist;
               vpNew.UcsPerViewport = true ;
             vpNew.UcsFollowModeOn = true ;
             vpNew.GridOn = true ;
             vpNew.GridFollow = true ;
             btrDest.AppendEntity(vpNew);
               Tx.AddNewlyCreatedDBObject(vpNew, true );
             vpNew.On = true ;
         }
           Tx.Commit();
     }
 }

## 评论

**内容**: Alexey said...
I`ve tested this code in Autocad 2012 and 2014 - it works improperly.
Right after command execution there is a viewport in paper space, but the view in it is WCS. Then I "double-click" inside the viewport and outside it - after this manipulation the view in the viewport became "myucs". Interesting that switching between model space and paper space doesn`t help in this case.
Is it a bug in Object ARX?
Reply
06/26/2015 at 12:22 AM

---
