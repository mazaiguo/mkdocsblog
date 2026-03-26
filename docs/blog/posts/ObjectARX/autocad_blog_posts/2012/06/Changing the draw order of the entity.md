---
title: "Changing the draw order of the entity"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Block
  - Database
description: "Each block in AutoCAD can maintain draw order information of the entities belongs to it. The draw order (DrawOrderTable) is stored as extension dic..."
author: Autodesk
---
# Changing the draw order of the entity

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/changing-the-draw-order-of-the-entity.html

## 文章内容

By Virupaksha Aithal
Each block in AutoCAD can maintain draw order information of the entities belongs to it. The draw order (DrawOrderTable) is stored as extension dictionary in the block table record. In .NET, you can access this dictionary using API “BlockTableRecord.DrawOrderTableId”. Draw order (DrawOrderTable), provides API’s like MoveToBottom, MoveToTop, MoveBelow, MoveAbove and etc to change the draw order of entities inside the block.
[CommandMethod("DrawOrderTest")]
static public void DrawOrderTest()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
    string message = "\nSelect a entity to move to bottom";
    PromptEntityOptions options = new PromptEntityOptions(message);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        Entity ent = tr.GetObject(acSSPrompt.ObjectId,
                                        OpenMode.ForRead) as Entity;
        //get the block
        BlockTableRecord block = tr.GetObject(ent.BlockId,
                               OpenMode.ForRead) as BlockTableRecord;
          //get the draw oder table of the block
        DrawOrderTable drawOrder =
                                 tr.GetObject(block.DrawOrderTableId,
                                OpenMode.ForWrite) as DrawOrderTable;
          ObjectIdCollection ids = new ObjectIdCollection();
        ids.Add(acSSPrompt.ObjectId);
          //move the selected entity so that entity is
        //drawn in the beginning of the draw order.
        drawOrder.MoveToBottom(ids);
          tr.Commit();
      }
}

## 评论

**内容**: John Lockhart said...
Wow, can't believe some of these changes. How does this make me more productive? Are we getting away from short commands? ...and replace the simple pull-down with typing out "drawing order" really? Who stayed up late dreaming up this?
My favorite is where you changed the sequence of Change properties. Sure why not?
Reply
03/05/2015 at 05:42 PM

---
