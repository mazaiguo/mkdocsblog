---
title: "Setting current view to Orthographic view"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Database
description: "Here is a sample code snippet to set the current view to "Right" view."
author: Autodesk
---
# Setting current view to Orthographic view

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/setting-current-view-to-orthographic-view.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code snippet to set the current view to "Right" view.
On similar lines, the view can be set to any other orthographic view.
[CommandMethod("SetRightView")]
public void SetRightViewMethod()
{
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    Database db = Application.DocumentManager.MdiActiveDocument.Database;
      ed.UpdateTiledViewportsInDatabase();
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        ViewportTable vpTbl
            = tr.GetObject
                        (
                            db.ViewportTableId,
                            OpenMode.ForRead
                        ) as ViewportTable;
          ViewportTableRecord viewportTableRec
            = tr.GetObject
                        (
                            vpTbl["*Active"],
                            OpenMode.ForWrite
                        ) as ViewportTableRecord;
          viewportTableRec.SetViewDirection
                                (
                                    OrthographicView.RightView
                                );
        tr.Commit();
    }
      ed.UpdateTiledViewportsFromDatabase();
}

