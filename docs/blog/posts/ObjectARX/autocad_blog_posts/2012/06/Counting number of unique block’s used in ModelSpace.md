---
title: "Counting number of unique block’s used in ModelSpace"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "One approach is to use “Editor.SelectAll” to find all the block references in the drawing file. Once you have all the references, then you can get ..."
author: Autodesk
---
# Counting number of unique block’s used in ModelSpace

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/counting-number-of-unique-blocks-used-in-modelspace.html

## 文章内容

By Virupaksha Aithal
One approach is to use “Editor.SelectAll” to find all the block references in the drawing file. Once you have all the references, then you can get the block table records of these references and make a list of unique blocks used in model space. Refer below code sample
[CommandMethod("countBlocks")]
public void countBlocks()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      ObjectIdCollection blockIds = new ObjectIdCollection();
      using (Transaction tr =
                        db.TransactionManager.StartTransaction())
    {
        BlockTable BT =
            (BlockTable)tr.GetObject(db.BlockTableId,
                                            OpenMode.ForRead);
          TypedValue[] filterlist = new TypedValue[1];
        filterlist[0] = new TypedValue(0, "INSERT");
          SelectionFilter filter =
                                new SelectionFilter(filterlist);
          PromptSelectionResult selRes = ed.SelectAll(filter);
          if (selRes.Status != PromptStatus.OK)
        {
            ed.WriteMessage(
                        "\nerror in getting the selectAll");
            return;
        }
          //get the modelspace
        ObjectId ModelSpaceId =
            SymbolUtilityServices.GetBlockModelSpaceId(db);
          foreach (ObjectId id in selRes.Value.GetObjectIds())
        {
            BlockReference blockRef =
             tr.GetObject(id, OpenMode.ForRead) as BlockReference;
              if (blockRef.OwnerId != ModelSpaceId)
                continue;
              //note, no special case for dynamic blocks..
            //please add extra checks if required for dynamic blocks.
            if (!blockIds.Contains(blockRef.BlockTableRecord))
                blockIds.Add(blockRef.BlockTableRecord);
        }
          tr.Commit();
    }
      ed.WriteMessage("Unqiue block reference in ModelSpace : "
                                + blockIds.Count.ToString() + "\n");
}

## 评论

**内容**: Zakaria said...
Hi Virupaksha,
I have an autocad drawing and I need to know how many times a certain block has used in it through a VBA Code.
For example:
how many times the block that its name = "Block1" has used in my drawing?
Thanks a lot & Best Regards
Zakaria
Reply
06/15/2013 at 01:13 AM

---
**内容**: Ben Koshy said in reply to Zakaria...
Simply change the selection filter to add the blockname:
private SelectionFilter GetSelectionFilter()
{
// selection filter. We filter by the name of the panel and also we want only lines
TypedValue[] acTypeValAr = new TypedValue[1] {new TypedValue((int)DxfCode.BlockName, "THE BLOCK NAME YOU WANT HERE")
};
// the instantiating of a selection filter which selects on certain layers and which selects only lines
SelectionFilter sf = new SelectionFilter(acTypeValAr);
return sf;
}
Reply
11/24/2015 at 02:30 PM

---
**内容**: Ben said in reply to Zakaria...
Please ignore the comments - it was a cut and paste
Reply
11/24/2015 at 02:32 PM

---
