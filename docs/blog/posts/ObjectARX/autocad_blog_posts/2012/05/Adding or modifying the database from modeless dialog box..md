---
title: "Adding or modifying the database from modeless dialog box."
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Plugin
  - Unicode
description: "As modeless dialog runs in application (or session) context, you have to lock the document before modifying the AutoCAD database. Refer below code...."
author: Autodesk
---
# Adding or modifying the database from modeless dialog box.

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/adding-or-modifying-the-database-from-modeless-dialog-box.html

## 文章内容

By Virupaksha Aithal
As modeless dialog runs in application (or session) context, you have to lock the document before modifying the AutoCAD database. Refer below code. Code adds a line to active document from a button click of a modeless dialog box. If document locking is not done, AutoCAD throws an eLockViolation exception while opening model space for writing
private void Add_ent_Click(object sender, EventArgs e)
{
    try
    {
//AutoCADAppServices is defined as
//using AutoCADAppServices = Autodesk.AutoCAD.ApplicationServices;
        Document doc = AutoCADAppServices.Application.
                            DocumentManager.MdiActiveDocument;
        Database db = doc.Database;
        Editor ed = doc.Editor;
        //lock the document
         using (DocumentLock docLock = doc.LockDocument())
        {
            using (Transaction Tx =
                      db.TransactionManager.StartTransaction())
            {
                ObjectId ModelSpaceId =
                    SymbolUtilityServices.GetBlockModelSpaceId(db);
                  Line line = new Line(new Point3d(0, 0, 0),
                                    new Point3d(10, 10, 0));
                  BlockTableRecord model = Tx.GetObject(ModelSpaceId,
                             OpenMode.ForWrite) as BlockTableRecord;
                  model.AppendEntity(line);
                Tx.AddNewlyCreatedDBObject(line, true);
                  Tx.Commit();
            }
        }
    }
    catch(System.Exception ex)
    {
        MessageBox.Show(ex.Message);
    }
}

