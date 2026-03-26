---
title: "Wblock - Creating new drawing from selected objects"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - API
  - Block
  - Database
description: "Database.Wblock API can be used to copy the objects from one drawing to completely new drawing. Refer below code, where the selected entities are c..."
author: Autodesk
---
# Wblock - Creating new drawing from selected objects

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/wblock-creating-new-drawing-from-selected-objects.html

## 文章内容

By Virupaksha Aithal
Database.Wblock API can be used to copy the objects from one drawing to completely new drawing. Refer below code, where the selected entities are copied to a new database and then the new database is saved.
[CommandMethod("wblockEntity")]
static public void wblockEntity()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptSelectionResult prRes = ed.GetSelection();
      if (prRes.Status != PromptStatus.OK)
        return;
      ObjectIdCollection objIds = new ObjectIdCollection();
    ObjectId[] objIdArray = prRes.Value.GetObjectIds();
      // Copy objectIds to objectIdCollection
    foreach (ObjectId id in objIdArray)
        objIds.Add(id);
      using (Database newDb = new Database(true, false))
    {
        db.Wblock(newDb, objIds, Point3d.Origin,
                                    DuplicateRecordCloning.Ignore);
        string FileName = "C:\\temp\\wblock.dwg";
        newDb.SaveAs(FileName, DwgVersion.Newest);
    }
}

## 评论

**内容**: Raghav Mehta said...
Everytime I select a block, it keeps asking me to select more even if they don't exist so the program never actually fully executes. Any help ?
Reply
07/11/2014 at 11:19 AM

---
