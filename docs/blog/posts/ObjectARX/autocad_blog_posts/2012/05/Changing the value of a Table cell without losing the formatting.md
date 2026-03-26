---
title: "Changing the value of a Table cell without losing the formatting"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I'm trying to change the value of a Table cell which has some formatting that keeps the value in fractional format."
author: Autodesk
---
# Changing the value of a Table cell without losing the formatting

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/changing-the-value-of-a-table-cell-without-losing-the-formatting.html

## 文章内容

By Adam Nagy
I'm trying to change the value of a Table cell which has some formatting that keeps the value in fractional format.
When I change the value the following way then the ["] sign will be missing from the end of the value and also when the user edits the value it will not be formatted to fractional anymore, i.e. the cell loses its formatting. What is the solution?
table.SetValue(row, col, "6 1/2", ParseOption.SetDefaultFormat);
Solution
The cell's Value type is double, but when you use SetValue() and pass in a string the Value type will be converted to string.
Another thing is that no matter what ParseOption you pass in, the DataFormat of that cell will be erased.
So you need to store the Format and pass in a double value, then restore the Format. This way the value will be formatted as it should be.
[CommandMethod("ChangeTableValue")]
static public void ChangeTableValue()
{
  Document doc = Application.DocumentManager.MdiActiveDocument;
  Database db = doc.Database;
  Editor ed = doc.Editor;
    PromptEntityResult per = ed.GetEntity("\nSelect a table");
  if (per.Status == PromptStatus.OK)
  {
    int row = 1, col = 2;
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
      Table table =
        (Table)tr.GetObject(per.ObjectId, OpenMode.ForWrite);
        // table.SetValue(), table.GetDataFomat()
      // and table.SetDataFormat() are obsolete.
      // Use below functions instead
      CellContent cont = table.Cells[row, col].Contents[0];
        string format = cont.DataFormat;
      cont.SetValue(8.5, ParseOption.SetDefaultFormat);
      cont.DataFormat = format;
        tr.Commit();
    }
  }
}

