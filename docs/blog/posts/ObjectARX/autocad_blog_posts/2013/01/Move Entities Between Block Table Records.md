---
title: "Move Entities Between Block Table Records"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "You can use the assumeOwnershipOf method to change the ownership of the entities. Using this method you can set the owner of given entities as any ..."
author: Autodesk
---
# Move Entities Between Block Table Records

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/move-entities-between-block-table-records.html

## 文章内容

By Virupaksha Aithal
You can use the assumeOwnershipOf method to change the ownership of the entities. Using this method you can set the owner of given entities as any block table record, thus effectively moving the entities from one block table record to other.
The following code shows how to move existing entities in Model Space to a block named 'Test'.
[CommandMethod("MoveEntToBlock")]
static public void MoveEntToBlock()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptSelectionOptions opts =
                           new PromptSelectionOptions();
    opts.MessageForAdding = "Select entities: ";
      PromptSelectionResult result = ed.GetSelection(opts);
      if (result.Status != PromptStatus.OK)
        return;
        using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        BlockTable blockTable = Tx.GetObject(db.BlockTableId,
                                      OpenMode.ForRead) as BlockTable;
          //set the test as new block if present
        if (!blockTable.Has("TEST"))
        {
            return;
        }
          BlockTableRecord record = Tx.GetObject(blockTable["TEST"],
                               OpenMode.ForRead) as BlockTableRecord;
          ObjectIdCollection ids =
                  new ObjectIdCollection(result.Value.GetObjectIds());
        record.AssumeOwnershipOf(ids);
          Tx.Commit();
      }
      ed.Regen();
}

