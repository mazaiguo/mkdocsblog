---
title: "Identify the number of reference to a block"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - API
  - Block
  - Database
description: "You can use BlockTableRecord:: GetBlockReferenceIds API  to get the object ids of the block references. You can get only direct reference (where th..."
author: Autodesk
---
# Identify the number of reference to a block

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/identify-the-number-of-reference-to-a-block.html

## 文章内容

By Virupaksha Aithal
You can use BlockTableRecord:: GetBlockReferenceIds API  to get the object ids of the block references. You can get only direct reference (where the block is used directely, like in model space or inside another block) by passing true as first parameter.
[CommandMethod("BlockRefCount")]
static public void BlockRefCount()
{
 Document doc = Application.DocumentManager.MdiActiveDocument;
 Database db = doc.Database;
 Editor ed = doc.Editor;
   PromptStringOptions opts =
    new PromptStringOptions("Enter block name");
    opts.AllowSpaces = true;
   PromptResult blockName = ed.GetString(opts);
   if (blockName.Status != PromptStatus.OK)
     return;
   using (Transaction tx =
                     db.TransactionManager.StartTransaction())
 {
     BlockTable blockTable = tx.GetObject(db.BlockTableId,
                                OpenMode.ForRead) as BlockTable;
       if (blockTable.Has(blockName.StringResult))
     {
         BlockTableRecord block = tx.GetObject(
                               blockTable[blockName.StringResult],
                               OpenMode.ForRead) as BlockTableRecord;
         //only direct reference
         ObjectIdCollection ids =
                            block.GetBlockReferenceIds(true, true);
           ed.WriteMessage("Number of reference is "
                                + ids.Count.ToString() + "\n");
     }
     tx.Commit();
 }
}

## 评论

**内容**: Matt Murphy said...

How do you get in an objectID collection the objectID of each unique block in modelspace? This is only blocks (i.e. not layouts etc).
Thanks
Reply
06/15/2012 at 04:17 AM

---
**内容**: Virupaksha Aithal said...
Thanks for the comment.
I think best is to use the editor.SelectAll() API, as shown in blog http://adndevblog.typepad.com/autocad/2012/06/counting-number-of-unique-blocks-used-in-modelspace.html
Thanks
Viru
Reply
06/18/2012 at 01:43 AM

---
