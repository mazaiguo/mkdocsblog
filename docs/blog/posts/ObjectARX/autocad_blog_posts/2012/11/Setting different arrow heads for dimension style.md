---
title: "Setting different arrow heads for dimension style"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
  - Dimension
description: "To set the different arrow heads for dimension style, you need to make the “DimStyleTableRecord .Dimsah = true” and then set the block table record..."
author: Autodesk
---
# Setting different arrow heads for dimension style

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/setting-different-arrow-heads-for-dimension-style.html

## 文章内容

By Virupaksha Aithal
To set the different arrow heads for dimension style, you need to make the “DimStyleTableRecord .Dimsah = true” and then set the block table record ids of the arrow head to “DimStyleTableRecord.Dimblk1” and “DimStyleTableRecord.Dimblk2”. Below code sets the arrow type “dot” and “closed” to current dimension style
[CommandMethod("DimStyle_Arrow")]
public void DimStyle_Arrow()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
        ObjectId id1 = GetArrowObjectId("DIMBLK1", "_DOT");
    ObjectId id2 = GetArrowObjectId("DIMBLK2", "_CLOSED");
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        DimStyleTableRecord dimStyleTable = Tx.GetObject(db.Dimstyle,
                                  OpenMode.ForWrite) as DimStyleTableRecord;
          dimStyleTable.Dimsah = true;
        dimStyleTable.Dimblk1 = id1;
        dimStyleTable.Dimblk2 = id2;
            db.SetDimstyleData(dimStyleTable);
        Tx.Commit();
    }
}
static ObjectId GetArrowObjectId(string arrow, string newArrName)
{
      ObjectId arrObjId = ObjectId.Null;
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
      string oldArrName =
                    Application.GetSystemVariable(arrow) as string;
      Application.SetSystemVariable(arrow, newArrName);
      if (oldArrName.Length != 0)
        Application.SetSystemVariable(arrow, oldArrName);
      Transaction tr = db.TransactionManager.StartTransaction();
      using (tr)
    {
          BlockTable bt = (BlockTable)tr.GetObject(
                                db.BlockTableId, OpenMode.ForRead);
        arrObjId = bt[newArrName];
        tr.Commit();
    }
      return arrObjId;
}

