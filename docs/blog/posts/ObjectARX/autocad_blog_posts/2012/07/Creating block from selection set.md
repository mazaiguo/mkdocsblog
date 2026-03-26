---
title: "Creating block from selection set"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
  - Selection
description: "Below code shows the procedure to create a new block table record from entities selected on screen.  The important function used is “DeepCloneObjec..."
author: Autodesk
---
# Creating block from selection set

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/creating-block-from-selection-set.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to create a new block table record from entities selected on screen.  The important function used is “DeepCloneObjects” which takes collections of object ids to be copy. The second parameter is the “owner” of the copied entities. In the below code, the block table record (“test”) is passed as owner, so that the selected entities clone objects are copied to block table record.
[CommandMethod("CreateBlock")]
public void CreateBlock()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      TypedValue[] filterlist = new TypedValue[1];
    filterlist[0] = new TypedValue(0, "CIRCLE,LINE");
      SelectionFilter filter = new SelectionFilter(filterlist);
      PromptSelectionOptions opts = new PromptSelectionOptions();
    opts.MessageForAdding = "Select entities: ";
    PromptSelectionResult selRes = ed.GetSelection(opts, filter);
      if (selRes.Status != PromptStatus.OK)
    {
        return;
    }
      ObjectId[] ids = selRes.Value.GetObjectIds();
    ObjectId blockId = ObjectId.Null;
    //add a block table record with name test...
    using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = (BlockTable)Tx.GetObject(db.BlockTableId,
                                                   OpenMode.ForRead);
          if (!bt.Has("Test"))
        {
            bt.UpgradeOpen();
            //create new
            BlockTableRecord record = new BlockTableRecord();
            record.Name = "Test";
              bt.Add(record);
            Tx.AddNewlyCreatedDBObject(record, true);
        }
          blockId = bt["Test"];
        Tx.Commit();
    }
      //copy the select entities to block by using deepclone.
    ObjectIdCollection collection = new ObjectIdCollection(ids);
    IdMapping mapping = new IdMapping();
    db.DeepCloneObjects(collection, blockId, mapping, false);
  }

## 评论

**内容**: Anonymoose said...
Code that uses SymbolTable's Has() or this[] indexer needs to avoid failing when either of those methods indicates an entry exists, because they both recognize erased entries.
Reply
07/28/2012 at 09:20 PM

---
**内容**: Virupaksha Aithal said in reply to Anonymoose...
Hi
Can you please check again? I feel “has” and “this[]” should work fine. Means should not recognize the erased items. (AutoCAD 2010 & above)
Thanks
Viru
Reply
08/02/2012 at 02:19 AM

---
