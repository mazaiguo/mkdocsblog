---
title: "Deleting un-used blocks"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "Below code shows the procedure to purge the block table. To take care of nested block scenario a Do/while loop is used."
author: Autodesk
---
# Deleting un-used blocks

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/deleting-un-used-blocks.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to purge the block table. To take care of nested block scenario a Do/while loop is used.
[CommandMethod("PurgeBlocks")]
public static void PurgeBlocks()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction Tx =
           db.TransactionManager.StartTransaction())
    {
        BlockTable table = Tx.GetObject(db.BlockTableId,
            OpenMode.ForRead) as BlockTable;
          ObjectIdCollection blockIds = new ObjectIdCollection();
          //using do/while loop to purge nested blocks.
        do
        {
            blockIds.Clear();
              foreach (ObjectId id in table)
                 blockIds.Add(id);
              //this function will remove all
            //blocks which are in use
            db.Purge(blockIds);
              foreach (ObjectId id in blockIds)
            {
                DBObject obj = Tx.GetObject(id, OpenMode.ForWrite);
                obj.Erase();
            }
        } while (blockIds.Count != 0);
        Tx.Commit();
    }
}

## 评论

**内容**: David Sparks said...
I tried this approach, but I keep getting a fatal error at the moment I try to open the id for write in the second foreach loop. Any idea why?
FATAL ERROR: Unhandled Access Violation Reading 0x0000 Exception at 8e659ed3h
Reply
01/15/2015 at 12:38 PM

---
**内容**: Virupaksha Aithal said...
Hi,
please let me know which version of AutoCAD you are using? also if possible share non confidential dwg file. You can also think of creating a AutoCAD.NET forum post. http://forums.autodesk.com/t5/net/bd-p/152
Thanks
Viru
Reply
01/19/2015 at 02:34 AM

---
