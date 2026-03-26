---
title: "Delete un-used layers from database."
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Database
  - Layer
description: "Database.Purge API can be used to identify the un-used layers. Once un-used layer are identified, you can use “erase” API to remove the layers from..."
author: Autodesk
---
# Delete un-used layers from database.

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/delete-un-used-layers-from-database.html

## 文章内容

By Virupaksha Aithal
Database.Purge API can be used to identify the un-used layers. Once un-used layer are identified, you can use “erase” API to remove the layers from the drawing file.
Note, the logic is very similar to post Delete un used registered application names from database @ http://adndevblog.typepad.com/autocad/2012/05/delete-un-used-registered-application-names-from-database.html#tp
[CommandMethod("PurgeLayers")]
public static void PurgeLayers()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction Tx =
           db.TransactionManager.StartTransaction())
    {
        LayerTable table = Tx.GetObject(db.LayerTableId,
            OpenMode.ForRead) as LayerTable;
          ObjectIdCollection layIds = new ObjectIdCollection();
        foreach (ObjectId id in table)
        {
            layIds.Add(id);
        }
          //this function will remove all
        //layers which are used in the drawing file
        db.Purge(layIds);
          foreach (ObjectId id in layIds)
        {
            DBObject obj = Tx.GetObject(id, OpenMode.ForWrite);
            obj.Erase();
        }
        Tx.Commit();
    }
}

## 评论

**内容**: Geo said...
Hi Virupaksha Aithal,
Still works perfectly in CAD2017!
i would only change comment in code :)
used->unused
cheers!
Reply
03/01/2017 at 01:09 AM

---
