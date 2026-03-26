---
title: "How to copy cells from one Table to another in .NET?"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
description: "Q: Is there any way to copy the contents of several rows/cells to another Table?"
author: Autodesk
---
# How to copy cells from one Table to another in .NET?

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/how-to-copy-cells-from-one-table-to-another-in-net.html

## 文章内容

By Marat Mirgaleev
Q: Is there any way to copy the contents of several rows/cells to another Table?
  A: Yes. You need to use the Table.CopyFrom method and pass two CellRange objects to it.
The following command copies two rows from a selected table to a new table.
// Copy some cells from a table to a new one.
//=================================================================
[CommandMethod("_copyCells")]
public static void copyCells()
{
  Document doc = Application.DocumentManager.MdiActiveDocument;
  Editor ed = doc.Editor;
    PromptEntityOptions opts =
                    new PromptEntityOptions("\nSelect a Table: ");
  opts.SetRejectMessage("This is not a Table.");
  opts.AddAllowedClass(typeof(Table), false);
  opts.AllowNone = false;
  PromptEntityResult res = ed.GetEntity(opts);
    if (res.Status != PromptStatus.OK)
    return;
    PromptPointResult pr =
            doc.Editor.GetPoint("\nEnter table insertion point: ");
  if (pr.Status != PromptStatus.OK)
    return;
    using (Transaction tr =doc.TransactionManager.StartTransaction())
  {
    BlockTable bt = tr.GetObject(doc.Database.BlockTableId,
                                    OpenMode.ForRead) as BlockTable;
    BlockTableRecord ms = tr.GetObject(
                            bt[BlockTableRecord.ModelSpace],
                            OpenMode.ForWrite) as BlockTableRecord;
    Table sourceTb = tr.GetObject(res.ObjectId,
                                        OpenMode.ForRead) as Table;
      // Create a new Table
    Table newTb = new Table();
    newTb.TableStyle = doc.Database.Tablestyle;
    newTb.SetSize(8, 5); /* In previous versions of AutoCAD
                          * we did it like this:
                              newTb.NumRows = 8;
                              newTb.NumColumns = 5; */
    newTb.Position = pr.Value;
      // Copy two last rows from the selected table to the new one
    newTb.CopyFrom(sourceTb, TableCopyOptions.FillTarget,
        CellRange.Create(sourceTb, sourceTb.Rows.Count-2, 0,
                  sourceTb.Rows.Count-1, sourceTb.Columns.Count-1),
        CellRange.Create(newTb, 3, 0, 4, sourceTb.Columns.Count-1));
    newTb.GenerateLayout();
      newTb.Cells[1, 1].Style = newTb.Cells[1, 1].Style;
      ms.AppendEntity(newTb);
    tr.AddNewlyCreatedDBObject(newTb, true);
      tr.Commit();
  }
} // End of copyCells()

