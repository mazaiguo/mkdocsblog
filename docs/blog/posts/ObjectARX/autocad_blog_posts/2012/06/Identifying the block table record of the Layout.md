---
title: "Identifying the block table record of the Layout"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "To add entities to layout, you need to identify the block table record associated with layout. Each layout stores an ID to block table record assoc..."
author: Autodesk
---
# Identifying the block table record of the Layout

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/identifying-the-block-table-record-of-the-layout.html

## 文章内容

By Virupaksha Aithal
To add entities to layout, you need to identify the block table record associated with layout. Each layout stores an ID to block table record associated with it. Below code adds a circle to a selected layout.
 [CommandMethod("EntAddLayout")]
 static public void EntAddLayout()
 {
     Document doc = Application.DocumentManager.MdiActiveDocument;
     Database db = doc.Database;
     Editor ed = doc.Editor;
     //get the layiut name
     PromptStringOptions opts =
        new PromptStringOptions("Enter Layout name");
     opts.AllowSpaces = true;
       PromptResult layoutName = ed.GetString(opts);
       if (layoutName.Status != PromptStatus.OK)
         return;
       using (Transaction tx =
                         db.TransactionManager.StartTransaction())
     {
         DBDictionary dLayouts = tx.GetObject(db.LayoutDictionaryId,
                                  OpenMode.ForRead) as DBDictionary;
         //check for layout name
         if (dLayouts.Contains(layoutName.StringResult))
         {
             ObjectId id = dLayouts.GetAt(layoutName.StringResult);
             Layout layout = tx.GetObject(id, OpenMode.ForRead)
                                                as Layout;
               //layout.BlockTableRecordId - gives the block id
             BlockTableRecord bt = tx.GetObject(
                                 layout.BlockTableRecordId,
                              OpenMode.ForWrite) as BlockTableRecord;
               //as a test - add a circle
             Circle circle = new Circle(Point3d.Origin,
                                               Vector3d.ZAxis, 10.0);
               bt.AppendEntity(circle);
             tx.AddNewlyCreatedDBObject(circle, true);
               //make the layout as current
             LayoutManager layoutMgr = LayoutManager.Current;
             layoutMgr.CurrentLayout = layoutName.StringResult;
           }
         tx.Commit();
     }
 }

