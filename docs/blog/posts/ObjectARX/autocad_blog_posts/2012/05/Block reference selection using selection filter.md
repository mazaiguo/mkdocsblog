---
title: "Block reference selection using selection filter"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
  - Selection
description: "This example will prompt the user to select some entities and then filter all the block references named "ABC". It then iterates through the select..."
author: Autodesk
---
# Block reference selection using selection filter

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/block-reference-selection-using-selection-filter.html

## 文章内容

By Virupaksha Aithal
This example will prompt the user to select some entities and then filter all the block references named "ABC". It then iterates through the selection set and calls erase() method on each blockReference.
[CommandMethod("delABC")]
public void delABC()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      try
    {
        using (Transaction tr =
            db.TransactionManager.StartTransaction())
        {
            BlockTable BT =
                (BlockTable)tr.GetObject(db.BlockTableId,
                                        OpenMode.ForRead);
              TypedValue[] filterlist = new TypedValue[2];
            filterlist[0] = new TypedValue(0, "INSERT");
            filterlist[1] = new TypedValue(2, "ABC");
              SelectionFilter filter =
                        new SelectionFilter(filterlist);
              PromptSelectionOptions opts =
                            new PromptSelectionOptions();
            opts.MessageForAdding = "Select entities: ";
              PromptSelectionResult selRes =
                            ed.GetSelection(opts, filter);
              if (selRes.Status != PromptStatus.OK)
            {
                ed.WriteMessage(
                    "\nNo ABC block references selected");
                return;
            }
              if (selRes.Value.Count != 0)
            {
                SelectionSet set = selRes.Value;
                  foreach (ObjectId id in set.GetObjectIds())
                {
                        BlockReference oEnt =
                                (BlockReference)tr.GetObject(id,
                                                OpenMode.ForWrite);
                        oEnt.Erase();
                }
            }
            tr.Commit();
        }
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.ToString());
    }
}

## 评论

**内容**: Vitalich said...
This method doesn't allow choosing my reference block.
I created defenition block, then inserted reference block to drawing and run this function. i tried choose my reference block, but autocad write message 0 object is found. SelectionSet is empty =(
Why?
Reply
12/09/2013 at 08:33 PM

---
**内容**: Vitalich said...
I choose this reference block by another method and BlockName is not "ABC", but "*U30". Is it matter?
Reply
12/09/2013 at 08:35 PM

---
