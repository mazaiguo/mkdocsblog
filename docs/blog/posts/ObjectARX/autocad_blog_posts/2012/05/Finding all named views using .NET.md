---
title: "Finding all named views using .NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Database
description: "Named views are stored in "ViewTable". Iterating the View Table will give you the named view of the drawing"
author: Autodesk
---
# Finding all named views using .NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/finding-all-named-views-using-net.html

## 文章内容

By Virupaksha Aithal
Named views are stored in "ViewTable". Iterating the View Table will give you the named view of the drawing
[CommandMethod("ListNamedView")]
public void ListNamedView()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction Tx =
                db.TransactionManager.StartTransaction())
    {
        ViewTable table =
            Tx.GetObject(db.ViewTableId,
                OpenMode.ForRead) as ViewTable;
          foreach (ObjectId id in table)
        {
            ViewTableRecord record = Tx.GetObject(id,
                        OpenMode.ForRead) as ViewTableRecord;
            ed.WriteMessage(record.Name + "\n");
        }
          Tx.Commit();
    }
  }

