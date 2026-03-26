---
title: "How To Create MTEXT In a Table Cell"
date: 2017-08-01
categories:
  - AutoCAD
tags:
  - Unicode
description: "Here is sample code to add MText when a user picks cell from Table."
author: Autodesk
---
# How To Create MTEXT In a Table Cell

发布日期: 2017-08-01

原始链接: https://adndevblog.typepad.com/autocad/2017/08/how-to-create-mtext-in-a-table-cell.html

## 文章内容

By Madhukar Moogala
Here is sample code to add MText when a user picks cell from Table.
You either pass RTF contents to MText or create string with Format codes.

static public void addMtext() {
  Document document =
  Application.DocumentManager.MdiActiveDocument;
  Editor ed = document.Editor;
  Database db = document.Database;

  PromptNestedEntityOptions pneo
   = new PromptNestedEntityOptions("");
  pneo.Message = "\nSelect a table cell text : ";
  PromptNestedEntityResult pner = ed.GetNestedEntity(pneo);
  if (pner.Status != PromptStatus.OK)
   return;
  Point3d pickedPt = pner.PickedPoint;

  ObjectId tableId = ObjectId.Null;
  ObjectId[] containers = pner.GetContainers();
  if (containers.Length > 0) {
   tableId = containers[0];
  }

  using(Transaction tr = 
  db.TransactionManager.StartTransaction()) {
   Table table = tr.GetObject(
    tableId,
    OpenMode.ForWrite
   ) as Table;

   if (table != null) {
    TableHitTestInfo htinfo = table.HitTest(
     pickedPt,
     Vector3d.ZAxis
    );

    ed.WriteMessage(
     "\nRow : {0} - Column : {1}",
     htinfo.Row,
     htinfo.Column
    );
    //clear any style overrirdes.
    table.Cells[htinfo.Row, htinfo.Column].ClearStyleOverrides();
    //create a Mtext and pass RTF contents 
    MText mt = new MText();
    mt.SetContentsRtf(@ "{\pntext\f0 1.\tab}First Line\par{\pntext\f0 2.\tab}Second Line\par}");
    //or
    //pass contents "1.\tFirst Line\\P2.\tSecond Line\\P"

    table.Cells[htinfo.Row, htinfo.Column].TextString =
     "1.\tFirst Line\\P2.\tSecond Line\\P"; //mt.Contents;


   }
   tr.Commit();
  }
Result:

## 评论

**内容**: kürtaj said...
nice
Reply
10/09/2021 at 03:09 AM

---
**内容**: fethiye otel said...
Thanks
Reply
10/09/2021 at 03:12 AM

---
