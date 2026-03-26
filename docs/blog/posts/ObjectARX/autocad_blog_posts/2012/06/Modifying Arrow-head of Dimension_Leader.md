---
title: "Modifying Arrow-head of Dimension/Leader"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Database
  - Dimension
description: "To modify the arrow head, you need to set the block table record object id of the block you want to see as the arrow head to database property “Dim..."
author: Autodesk
---
# Modifying Arrow-head of Dimension/Leader

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/modifying-arrow-head-of-dimensionleader.html

## 文章内容

By Virupaksha Aithal
To modify the arrow head, you need to set the block table record object id of the block you want to see as the arrow head to database property “Dimblk”. Below code demonstrates the same. Below code, first loads the "_DOTBLANK" block and then sets the “_DOTBLANK” as the current arrow head. To test the below code, first run the command “setArrowHead” and then try to create a leader/dimension through AutoCAD UI.
[CommandMethod("setArrowHead")]
static public void setArrowHead()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable blockTable = tr.GetObject(db.BlockTableId,
                                OpenMode.ForRead) as BlockTable;
        if (!blockTable.Has("_DOTBLANK"))
        {
            //load
            Application.SetSystemVariable("DIMBLK", "_DOTBLANK");
        }
        //now set the arrow head.
        db.Dimblk = blockTable["_DOTBLANK"];
          tr.Commit();
    }
}

## 评论

**内容**: skeletank said...
How could I do this using RealDwg where I don't have the ability to use Application.SetSystemVariable?
Reply
05/30/2017 at 11:42 AM

---
