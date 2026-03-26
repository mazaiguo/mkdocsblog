---
title: "Making a line type current"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Database
description: "To modify the database current line type, you need to modify the database property “Celtype”. Below code shows the procedure to update the current ..."
author: Autodesk
---
# Making a line type current

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/making-a-line-type-current.html

## 文章内容

By Virupaksha Aithal
To modify the database current line type, you need to modify the database property “Celtype”. Below code shows the procedure to update the current line type of the drawing. When run, below code loads the “DASHED” line type first and then makes it as current line type.
[CommandMethod("MakeingLineTypeCurrent")]
public void MakeingLineTypeCurrent()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction Tx =
       db.TransactionManager.StartTransaction())
    {
        ObjectId id = db.Celtype;
        LinetypeTableRecord linetype = Tx.GetObject(id,
                        OpenMode.ForRead) as LinetypeTableRecord;
          ed.WriteMessage("Previous database line type is " +
                                               linetype.Name + "\n");
          LinetypeTable tbl =
            (LinetypeTable)Tx.GetObject(db.LinetypeTableId
                                           , OpenMode.ForRead);
        if (!tbl.Has("DASHED"))
        {
            db.LoadLineTypeFile("DASHED", "acad.lin");
        }
          //now make the linetype  current.
        db.Celtype = tbl["DASHED"];
          linetype = Tx.GetObject(db.Celtype,
                        OpenMode.ForRead) as LinetypeTableRecord;
          ed.WriteMessage("Current database line type is " +
                                               linetype.Name + "\n");
        Tx.Commit();
    }
}

