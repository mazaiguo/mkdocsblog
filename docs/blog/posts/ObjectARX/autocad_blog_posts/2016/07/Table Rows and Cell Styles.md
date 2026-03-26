---
title: "Table Rows and Cell Styles"
date: 2016-07-01
categories:
  - AutoCAD
tags:
  - Database
description: "Each row or cell in a table can have a specific style attached to it. You can get/set this style using CellRange.Style property. Refer below code"
author: Autodesk
---
# Table Rows and Cell Styles

发布日期: 2016-07-01

原始链接: https://adndevblog.typepad.com/autocad/2016/07/table-rows-and-cell-styles.html

## 文章内容

By Virupaksha Aithal
Each row or cell in a table can have a specific style attached to it. You can get/set this style using CellRange.Style property. Refer below code
[CommandMethod("GetRowType")]
public void GetRowType()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;

    PromptEntityOptions peo = new PromptEntityOptions("\nSelect Table: ");
    peo.SetRejectMessage("\nInvalid selection...");
    peo.AddAllowedClass(typeof(Table), true);

    PromptEntityResult per = ed.GetEntity(peo);

    if (per.Status != PromptStatus.OK)
        return;

    using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        Table table = Tx.GetObject(per.ObjectId, OpenMode.ForRead) as Table;

        for (int row = 0; row < table.Rows.Count; row++)
        {
            ed.WriteMessage("\nRow[{0}]: {1}", row, table.Cells[row, -1].Style);
        }

        Tx.Commit();
    }
}

## 评论

**内容**: neyton luiz dalle molle said...
table.Cells[row, -1].Style = "Data"
not working => eNotApplicable
yes, table is open "forwrite"
Reply
12/15/2016 at 08:47 AM

---
**内容**: Daniel Avi said...
Hi.
I have a question.
I want trans Table in AutoCAD to Excel, how to get value cell merged in table trans to Excel
Reply
07/01/2017 at 08:34 AM

---
**内容**: Amazon said...
Hey,
I have an E_commerce store affiliate with Amazon. I am listing quality product on my store. These products available on my store in very cheap price. If you want to visit my store.
Reply
02/21/2023 at 04:29 AM

---
**内容**: Curated by Phoenix said...
Your blog provides a comprehensive perspective. offering valuable insights and engaging content. I appreciate the depth of research evident throughout, which enhances the credibility of the information presented. If you're looking to buy props, check out https://curatedbyphoenix.com/ for some fantastic options!"
Reply
02/26/2024 at 02:09 AM

---
