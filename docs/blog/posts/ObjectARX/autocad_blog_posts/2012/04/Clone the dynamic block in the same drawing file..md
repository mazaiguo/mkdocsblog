---
title: "Clone the dynamic block in the same drawing file."
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - API
  - Block
  - Database
description: "Below code shows the procedure to clone the dynamic block with all its properties to same drawing file."
author: Autodesk
---
# Clone the dynamic block in the same drawing file.

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/clone-the-dynamic-block-in-the-same-drawing-file.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to clone the dynamic block with all its properties to same drawing file.
Steps:
Wblock the present dynamic block to new database using “wblock”.
Use “Insert” API to insert the database (generated in step1) with new block name
[CommandMethod("cloneDynamic")]
static public void cloneDynamic() // This method can have any name
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
    Database db = doc.Database;
    using (Transaction tr =
        db.TransactionManager.StartTransaction())
    {
        BlockTable tb = tr.GetObject(db.BlockTableId,
                        OpenMode.ForRead) as BlockTable;
        BlockTableRecord dynamic = tr.GetObject(tb["DynamicBlock"],
                            OpenMode.ForRead) as BlockTableRecord;
          Database temDB = db.Wblock(dynamic.ObjectId);
          ObjectId copyId = ObjectId.Null;
        using (temDB)
        {
            copyId = db.Insert("DynamicBlockCopy", temDB, true);
        }
        tr.Commit();
      }
}

## 评论

**内容**: Efren said...
Hi, thanks for this post. I've been going around the bushes in confusion which db is source and destination in my own code. Can you please go further just to copy the dynamic block into a different *name* ?
Thanks,
Efren
Reply
12/13/2012 at 04:48 PM

---
**内容**: Efren said in reply to Efren...
ooops. pls forgive my oversight. can i delete my post?
Reply
12/13/2012 at 04:49 PM

---
**内容**: Daniel said...
Hello,
testing this I run into the "eWasErased" Exception. What am I doing wrong?
Any hints are appreciated!
Thank you,
Daniel
Reply
02/03/2013 at 12:33 PM

---
