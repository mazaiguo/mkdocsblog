---
title: "Identifying block Name from the block reference"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Database
  - Selection
description: "Identifying block name from the reference becomes bit tricky when dynamic blocks are involved. When users modify the dynamic block, AutoCAD creates..."
author: Autodesk
---
# Identifying block Name from the block reference

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/identifying-block-name-from-the-block-reference.html

## 文章内容

By Virupaksha Aithal
Identifying block name from the reference becomes bit tricky when dynamic blocks are involved. When users modify the dynamic block, AutoCAD creates an anonymous block first and then creates a reference to it in the drawing. Below code takes care of this scenario and finds the name of the block on selection of block reference.
[CommandMethod("blockName")]
static public void blockName()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
             new PromptEntityOptions("\nSelect block reference");
    options.SetRejectMessage("\nSelect only block reference");
    options.AddAllowedClass(typeof(BlockReference), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      using (Transaction tx =
                        db.TransactionManager.StartTransaction())
    {
        BlockReference blockRef = tx.GetObject(acSSPrompt.ObjectId,
                               OpenMode.ForRead) as BlockReference;
          BlockTableRecord block = null;
        if (blockRef.IsDynamicBlock)
        {
            //get the real dynamic block name.
            block = tx.GetObject(blockRef.DynamicBlockTableRecord,
                    OpenMode.ForRead) as BlockTableRecord;
          }
        else
        {
            block = tx.GetObject(blockRef.BlockTableRecord,
                        OpenMode.ForRead) as BlockTableRecord;
        }
            if (block != null)
        {
            ed.WriteMessage("Block name is : "
                                        + block.Name + "\n");
        }
        tx.Commit();
    }
}

## 评论

**内容**: Matus Brlit said...
you can use DynamicBlockTableRecord even if it's not the anonymous version of the dynamic block, so the check for block.IsAnonymous is redundant
Reply
06/01/2012 at 06:19 AM

---
**内容**: Virupaksha Aithal said in reply to Matus Brlit...
“IsAnonymous” required, AutoCAD creates a “Anonymous” block once user modifies the dynamic block reference. In that case we need to use “DynamicBlockTableRecord” to get the real block name.
-Viru
Reply
06/03/2012 at 11:14 PM

---
**内容**: Matus Brlit said...
what i meant is thet every dynamic block reference has the property DynamicBlockTableRecord, even if it was not modified
you already test if the block is dynamic, so if it's true, just take the DynamicBlockTableRecord
if (blockRef.IsDynamicBlock)
{
block = tx.GetObject(blockRef.DynamicBlockTableRecord,
OpenMode.ForRead) as blockTableRecord;
}
else
{
block = tx.GetObject(blockRef.BlockTableRecord,
OpenMode.ForRead) as BlockTableRecord;
}
Reply
06/03/2012 at 11:29 PM

---
**内容**: Virupaksha Aithal said in reply to Matus Brlit...
Thanks a lot. Yes, you are absolutely correct. I have made changes in the blog post to reflect your suggestion
-Viru
Reply
06/04/2012 at 12:20 AM

---
**内容**: Sailor said...
I'm confused by the Commit()
ObjectId blockRefId; // Picked from CAD
using(Transaction tx = db.TransactionManager.StartTransaction())
{
   BlockReference blockRef = blockRefId.GetObject(OpenMode.ForRead) as BlockReference;
   // Before committing the blockRef.IsDynamicBlock is true
   tx.Commit();
   // After committed the blockRef.IsDynamicBlock is false
}
Why the attribute of the BlockReference had been changed after the Commit()?
Thanks!
Reply
05/28/2014 at 06:19 PM

---
**内容**: Ken said in reply to Sailor...
I'm finding something similar. I can't call IsDynamicBlock and get true for a dynamic block. If I go ahead and get the BlockTableRecord via DynamicBlockTableRecord the BTR tells me that it's dynamic and then I can get the name of it. IsDynamic on the BlockRecord doesn't seem to give the correct information.
Must be something that I'm not understanding?
Reply
02/02/2020 at 08:51 AM

---
**内容**: Igor FUJS said...
I belive that when there is no transaction running, any reference to a dbobject is not valid any more. So reading proprties might give you very strange behaviour and/or tesults
Reply
10/29/2022 at 12:19 PM

---
