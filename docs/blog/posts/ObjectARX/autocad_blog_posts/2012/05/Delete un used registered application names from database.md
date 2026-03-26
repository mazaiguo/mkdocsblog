---
title: "Delete un used registered application names from database"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "Database.Purge API can be used to identify the un-used registered applications. Once un used registered application names are identified, use “eras..."
author: Autodesk
---
# Delete un used registered application names from database

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/delete-un-used-registered-application-names-from-database.html

## 文章内容

By Virupaksha Aithal
Database.Purge API can be used to identify the un-used registered applications. Once un used registered application names are identified, use “erase” API to remove the registered application names from the drawing file.
[CommandMethod("PurgeApplicationName")]
public static void PurgeApplicationName()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction Tx =
           db.TransactionManager.StartTransaction())
    {
        RegAppTable table = Tx.GetObject(db.RegAppTableId,
            OpenMode.ForRead) as RegAppTable;
          ObjectIdCollection regIds = new ObjectIdCollection();
        foreach (ObjectId id in table)
        {
            regIds.Add(id);
        }
          //this function will remove all
        //app names which are used in the drawing file
        db.Purge(regIds);
          foreach (ObjectId id in regIds)
        {
            DBObject obj = Tx.GetObject(id, OpenMode.ForWrite);
            obj.Erase();
        }
        Tx.Commit();
    }
}

## 评论

**内容**: Joshua Hunt said...
How is this different or better than...
-PURGE
REGAPPS
*
Reply
02/07/2014 at 01:40 PM

---
**内容**: Madhukar Moogala said...
Not better - different. For example ...
- It can be used on AutoCAD versions that don't have that purge option.
- It demonstrates how to perform an operation using the API.
Reply
02/11/2014 at 09:00 PM

---
