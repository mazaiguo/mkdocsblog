---
title: "Find the shx file used in an Line type (LineTypeTableRecord)"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Database
  - Plot
  - Unicode
description: "If a line type uses a shx file it will reference an AcDbTextStyleTableRecord. Here is an example that prints the names of the shx file used by the ..."
author: Autodesk
---
# Find the shx file used in an Line type (LineTypeTableRecord)

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/find-the-shx-file-used-in-an-line-type-linetypetablerecord.html

## 文章内容

By Virupaksha Aithal
If a line type uses a shx file it will reference an AcDbTextStyleTableRecord. Here is an example that prints the names of the shx file used by the ZIGZAG linetype.
[CommandMethod("getShpName")]
 static public void getShpName()
 {
     Document doc = Application.DocumentManager.MdiActiveDocument;
     Database db = doc.Database;
     Editor ed = doc.Editor;
       using (Transaction Tx =
        db.TransactionManager.StartTransaction())
     {
         LinetypeTable tbl =
             (LinetypeTable)Tx.GetObject(db.LinetypeTableId
                                            , OpenMode.ForRead);
         //check for ZigZag.
         if (tbl.Has("ZigZag"))
         {
             LinetypeTableRecord lt =
                 (LinetypeTableRecord)Tx.GetObject(tbl["ZigZag"],
                                                   OpenMode.ForRead);
               int nDash = lt.NumDashes;
               ed.WriteMessage(lt.Name + "\n");
               for (int i = 0; i < nDash; i++)
             {
                 int iShpNum = lt.ShapeNumberAt(i);
                   if (iShpNum != 0)
                 {
                     ObjectId txtId = lt.ShapeStyleAt(i);
                     TextStyleTableRecord txt =
                         (TextStyleTableRecord)Tx.GetObject(txtId,
                                                    OpenMode.ForRead);
                       ed.WriteMessage("   " + txt.FileName + "\n");
                 }
             }
         }
           Tx.Commit();
     }
 }

