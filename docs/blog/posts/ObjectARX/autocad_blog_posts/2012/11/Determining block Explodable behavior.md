---
title: "Determining block Explodable behavior"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
  - Plot
description: "The “Explodable” property of a block will allow you to determine if block can be exploded or not. Below code prints names of the blocks which can b..."
author: Autodesk
---
# Determining block Explodable behavior

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/determining-block-explodable-behavior.html

## 文章内容

By Virupaksha Aithal
The “Explodable” property of a block will allow you to determine if block can be exploded or not. Below code prints names of the blocks which can be exploded.
[CommandMethod("FindBlockExplode")]
public void FindBlockExplode()
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
              if (btr.Explodable)
            {
                ed.WriteMessage(btr.Name + "\n");
            }
        }
          Tx.Commit();
    }
}

