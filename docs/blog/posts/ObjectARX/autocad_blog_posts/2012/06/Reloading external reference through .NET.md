---
title: "Reloading external reference through .NET"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Block
  - Database
  - XREF
description: "You can use “Database.ReloadXrefs” API to reload the external referenced drawing files. “ReloadXrefs” takes a collection of object ids, which can b..."
author: Autodesk
---
# Reloading external reference through .NET

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/reloading-external-reference-through-net.html

## 文章内容

By Virupaksha Aithal
You can use “Database.ReloadXrefs” API to reload the external referenced drawing files. “ReloadXrefs” takes a collection of object ids, which can be prepared by traversing through the block table as shown in below code.
[CommandMethod("ReloadXRefs")]
static public void ReloadXRefs()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
         ObjectIdCollection ids = new ObjectIdCollection();
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable table = tr.GetObject(db.BlockTableId,
                                    OpenMode.ForRead) as BlockTable;
            foreach (ObjectId id in table)
        {
            BlockTableRecord record = tr.GetObject(id,
                               OpenMode.ForRead) as BlockTableRecord;
              if (record.IsFromExternalReference)
            {
                ids.Add(id);
            }
        }
          tr.Commit();
    }
      //now relaod the xrefs
    if (ids.Count != 0)
    {
        db.ReloadXrefs(ids);
    }
  }

