---
title: "How do I specify that a row in the table is a Header or Title or Data?"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Can I set an arbitrary row in a table as a Header? Or Title?"
author: Autodesk
---
# How do I specify that a row in the table is a Header or Title or Data?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-do-i-specify-that-a-row-in-the-table-is-a-header-or-title-or-data.html

## 文章内容

By Marat Mirgaleev
Issue
Can I set an arbitrary row in a table as a Header? Or Title?
Solution
Yes, it can be done.
The type of a row can be set using the CellRange.Style property.
The CellRange for a row can be obtained with this call: Table.Cells[ rowNumber, -1 ].
There are predefined styles for title, header and data cells, called "_TITLE", "_HEADER", "_DATA".
Here is a code sample:
    [CommandMethod("_STRS")]
    public static void setTableRowStyle()
    {
      Document doc = Application.DocumentManager.MdiActiveDocument;
      Editor ed = doc.Editor;
      try
      {
        PromptEntityOptions opts1 =
          new PromptEntityOptions("\nSelect a Table: ");
        opts1.SetRejectMessage("This is not a Table.");
        opts1.AddAllowedClass(typeof(Table), false);
        opts1.AllowNone = false;
        PromptEntityResult res1 = ed.GetEntity(opts1);
        if (res1.Status != PromptStatus.OK)
          return;
          using (Transaction tr =
                           doc.TransactionManager.StartTransaction())
        {
          Table tb =
             tr.GetObject(res1.ObjectId, OpenMode.ForWrite) as Table;
            const int ROW_TO_SET_HEADER = 3, ROW_TO_SET_TITLE = 4,
                    ROW_TO_SET_DATA = 1;
          tb.Cells[ROW_TO_SET_HEADER, -1].Style = "_HEADER";
          tb.Cells[ROW_TO_SET_TITLE,  -1].Style = "_TITLE";
          tb.Cells[ROW_TO_SET_DATA,   -1].Style = "_DATA";
            tr.Commit();
        }
      }
      catch (System.Exception e)
      {
        ed.WriteMessage("\nERROR: " + e.ToString());
      }
    } // End of setTableRowStyle()

