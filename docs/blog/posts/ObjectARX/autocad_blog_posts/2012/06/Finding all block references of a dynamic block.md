---
title: "Finding all block references of a dynamic block"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Block
  - C++
  - Database
  - ObjectARX
description: "In a previous post, Balaji showed how to find the name of a dynamic block from one of its block references. This post shows how to navigate in the ..."
author: Autodesk
---
# Finding all block references of a dynamic block

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/finding-all-block-references-of-a-dynamic-block.html

## 文章内容

By Stephen Preston
In a previous post, Balaji showed how to find the name of a dynamic block from one of its block references. This post shows how to navigate in the other direction – finding all the references to a dynamic block.
As a reminder – when you manipulate a dynamic block, the changes are stored behind the scenes as anonymous blocks. An anonymous block is created for each different state of the dynamic block in the drawing. In ObjectARX, you use the the AcDbDybBlockReference and AcDbDynBlockTableRecord classes to work with anonymous blocks. The extra functions they provided are rolled into the BlockReference and BlockTableRecord classes in .NET for simplicity.
[CommandMethod("selb")]
public void selectDynamicBlockReferences()
{
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
  Database db = Application.DocumentManager.MdiActiveDocument.Database;
  using (Transaction trans = db.TransactionManager.StartTransaction())
  {
    //get the blockTable and iterate through all blockDef
    BlockTable bt = (BlockTable)trans.GetObject(db.BlockTableId,
                                              OpenMode.ForRead);
    foreach (ObjectId btrId in bt)
    {
      //get the blockDef and check if is anonymous
      BlockTableRecord btr = (BlockTableRecord)trans.GetObject(btrId,
                                                  OpenMode.ForRead);
      if (btr.IsDynamicBlock)
      {
        //get all anonymous blocks from this dynamic block
        ObjectIdCollection anonymousIds = btr.GetAnonymousBlockIds();
        ObjectIdCollection dynBlockRefs = new ObjectIdCollection();
        foreach (ObjectId anonymousBtrId in anonymousIds)
        {
          //get the anonymous block
          BlockTableRecord anonymousBtr =
                    (BlockTableRecord)trans.GetObject(anonymousBtrId,
                                                  OpenMode.ForRead);
          //and all references to this block
          ObjectIdCollection blockRefIds =
                      anonymousBtr.GetBlockReferenceIds(true, true);
          foreach (ObjectId id in blockRefIds)
          {
            dynBlockRefs.Add(id);
          }
        }
        //Do something with the collection we created
        ed.WriteMessage(String.Format("Dynamic block \"{0}\" found with {1} anonymous block and {2} block references\n",
            btr.Name, anonymousIds.Count, dynBlockRefs.Count));
      }
    }
  }
}

## 评论

**内容**: Barabas said...
Thanks a lot
Reply
10/16/2012 at 01:52 AM

---
**内容**: Sailor said...
I made a customized Block named 'STower' in a 'block.dwg' file and then copied it to the current 'wire.dwg'. Then in the 'wire.dwg' I copied the 'STower' block 10 times.
I followed the code it print like this, 'Dynamic block "STower" found with 1 anonymous block and 11 block references'.
In the AutoCAD I saw 11 'STower' blocks.
I just want to know what is 'anonymous block' and 'block reference'.
What are the differences?
Many thanks!
Reply
05/27/2014 at 11:33 PM

---
**内容**: Vivek Kumar said...
I have a question- I have to convert the below LISP code in .NET code but I don't find any similar method to achieve the same.
---------------------------------------------------
(if (=
(cdr (assoc 0 (entget (cdr (assoc -2 BLOCKLIST)))))
"ENDBLK" )
(progn
(if (setq NB (ssget "x" (list (assoc 2 BLOCKLIST))))
(command "erase" NB "" )
)
)
---------------------------------------------------
I am stuck with "ENDBLK"
How to filter the blocks with "ENDBLK" from the Block LIST?
I have tried a lot to find but I could not get any relevant information.
Please help me out on this.
Thanks.
Reply
11/20/2014 at 10:11 AM

---
**内容**: andred@adc-dao.com said...
Thank you very much, it works like a charm, very usefull. André.
Reply
06/15/2018 at 05:59 AM

---
