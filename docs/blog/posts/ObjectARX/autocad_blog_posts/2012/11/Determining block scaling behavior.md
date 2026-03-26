---
title: "Determining block scaling behavior"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
  - Plot
description: "The BlockScaling property of a block will allow you to determine block scaling setting. Below code prints names of the blocks which are created wit..."
author: Autodesk
---
# Determining block scaling behavior

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/determining-block-scaling-behavior.html

## 文章内容

By Virupaksha Aithal
The BlockScaling property of a block will allow you to determine block scaling setting. Below code prints names of the blocks which are created with uniform scaling option.
[CommandMethod("FindBlockScaling")]
public void FindBlockScaling()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = (BlockTable)Tx.GetObject(db.BlockTableId,
                                                  OpenMode.ForRead);
          foreach (ObjectId id in bt)
        {
            BlockTableRecord btr = Tx.GetObject(id,
                          OpenMode.ForRead) as BlockTableRecord;
              if (btr.IsLayout)
                continue;
              if (btr.BlockScaling == BlockScaling.Uniform)
            {
                ed.WriteMessage(btr.Name + "\n");             
            }
        }
          Tx.Commit();
    }
}

