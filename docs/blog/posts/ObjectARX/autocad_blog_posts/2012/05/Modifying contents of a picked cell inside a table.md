---
title: "Modifying contents of a picked cell inside a table"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Database
  - Selection
  - Unicode
description: "Here is a sample code that allows the user to pick a cell in a table and change its cell content. The nested entity selection using the "Editor.Get..."
author: Autodesk
---
# Modifying contents of a picked cell inside a table

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/modifying-contents-of-a-picked-cell-inside-a-table.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code that allows the user to pick a cell in a table and change its cell content. The nested entity selection using the "Editor.GetNestedEntity" method allows us to select the MText entity nested in a table cell. After a MText is selected, the "Table.HitTest" method can be used to identify the row and column numbers of the cell. We can then go-ahead and change the MText contents.
Document document =
        Application.DocumentManager.MdiActiveDocument;
Editor ed = document.Editor;
Database db = document.Database;
  PromptNestedEntityOptions pneo
                = new PromptNestedEntityOptions("");
pneo.Message = "\nSelect a table cell text : ";
  // Note : GetNestedEntity does not select table cell text
// in "2dWireframe" visual style.
// To try this sample code, set Visual style to "Realistic"
PromptNestedEntityResult pner = ed.GetNestedEntity(pneo);
if (pner.Status != PromptStatus.OK)
    return;
Point3d pickedPt = pner.PickedPoint;
  ObjectId tableId = ObjectId.Null;
ObjectId[] containers = pner.GetContainers();
if (containers.Length > 0)
{
    tableId = containers[0];
}
  using (Transaction tr
            = db.TransactionManager.StartTransaction())
{
    Table table = tr.GetObject(
                                tableId,
                                OpenMode.ForWrite
                              ) as Table;
      if (table != null)
    {
        TableHitTestInfo htinfo = table.HitTest
                                        (
                                            pickedPt,
                                            Vector3d.ZAxis
                                        );
          ed.WriteMessage(
                         "\nRow : {0} - Column : {1}",
                         htinfo.Row,
                         htinfo.Column
                       );
          table.Cells [
                        htinfo.Row,
                        htinfo.Column
                    ].Value = "Autodesk";
    }
    tr.Commit();
}

## 评论

**内容**: Amazon said...
Hey,
I have an E_commerce store affiliate with Amazon. I am listing quality product on my store. These products available on my store in very cheap price. If you want to visit my store.
Click on the url
Reply
02/21/2023 at 07:13 AM

---
