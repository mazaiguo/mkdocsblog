---
title: "Setting relative draw order of entities using .NET"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Database
description: "To set the relative draw order of entities with respect to another entity, you can use API “DrawOrderTable.MoveAbove” or “DrawOrderTable”  as shown..."
author: Autodesk
---
# Setting relative draw order of entities using .NET

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/setting-relative-draw-order-of-entities-using-net.html

## 文章内容

By Virupaksha Aithal
To set the relative draw order of entities with respect to another entity, you can use API “DrawOrderTable.MoveAbove” or “DrawOrderTable”  as shown in below code.
[CommandMethod("MoveAbove")]
static public void MoveAbove()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
        string message = "\nSelect a entity to move above";
    PromptEntityOptions optEnt = new PromptEntityOptions(message);
      PromptEntityResult acEnt = ed.GetEntity(optEnt);
      if (acEnt.Status != PromptStatus.OK)
        return;
      message = "\nSelect target entity";
    PromptEntityOptions optTarget = new PromptEntityOptions(message);
      PromptEntityResult acTarget = ed.GetEntity(optTarget);
      if (acTarget.Status != PromptStatus.OK)
        return;
        using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        Entity ent = tr.GetObject(acEnt.ObjectId,
                                        OpenMode.ForRead) as Entity;
        //get the block
        BlockTableRecord block = tr.GetObject(ent.BlockId,
                               OpenMode.ForRead) as BlockTableRecord;
          //get the draw oder table of the block
        DrawOrderTable drawOrder =
                                 tr.GetObject(block.DrawOrderTableId,
                                OpenMode.ForWrite) as DrawOrderTable;
          ObjectIdCollection ids = new ObjectIdCollection();
        ids.Add(acEnt.ObjectId);
          //moves entities above the target entity.
        drawOrder.MoveAbove(ids, acTarget.ObjectId);
          tr.Commit();
      }
}

