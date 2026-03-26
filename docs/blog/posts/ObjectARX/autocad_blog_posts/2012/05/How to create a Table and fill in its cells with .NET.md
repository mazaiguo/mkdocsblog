---
title: "How to create a Table and fill in its cells with .NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Database
description: "The code below shows how to create a table and fill in its cells. Some obsolete methods of Table are still visible. You will receive a warning in c..."
author: Autodesk
---
# How to create a Table and fill in its cells with .NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-create-a-table-and-fill-in-its-cells-with-net.html

## 文章内容

By Xiaodong Liang
The code below shows how to create a table and fill in its cells. Some obsolete methods of Table are still visible. You will receive a warning in compiling if using obsolete methods. Please use the newest methods.
[CommandMethod("testaddtable")]
public void testaddtable()
{
    Database  db =
        HostApplicationServices.WorkingDatabase;
        using (Transaction tr =
        db.TransactionManager.StartTransaction())
    {
        BlockTable bt =
            (BlockTable)tr.GetObject(db.BlockTableId,
                                    OpenMode.ForRead);
        ObjectId msId =
            bt[BlockTableRecord.ModelSpace];
          BlockTableRecord btr =
            (BlockTableRecord)tr.GetObject(msId,
                                OpenMode.ForWrite);
          // create a table
        Table tb = new Table();
        tb.TableStyle = db.Tablestyle;
          // row number
        Int32 RowsNum = 5;
        // column number
        Int32 ColumnsNum = 5;
          // row height
        double rowheight = 3;
        // column width
        double columnwidth = 20;
          // insert rows and columns
        tb.InsertRows(0,
                    rowheight,
                    RowsNum);
        tb.InsertColumns(0,
                    columnwidth,
                    ColumnsNum);
          tb.SetRowHeight(rowheight);
        tb.SetColumnWidth(columnwidth);
          Point3d eMax = db.Extmax;
        Point3d eMin = db.Extmin;
        double CenterY =
            (eMax.Y + eMin.Y) * 0.5;
        tb.Position =
            new Point3d(10, 10, 0);
          // fill in the cell one by one
        for (int i = 0;
            i < RowsNum;
            i++)
        {
            for (int j = 0;
                j < ColumnsNum;
                j++)
            {
                tb.Cells[i, j].TextHeight =  1;
                if (i == 0 && j == 0)
                    tb.Cells[i, j].TextString =
                        "The Title";
                else
                    tb.Cells[i, j].TextString =
                        i.ToString() + "," + j.ToString();
                  tb.Cells[i,j].Alignment =
                    CellAlignment.MiddleCenter;
            }
        }
          tb.GenerateLayout();
        btr.AppendEntity(tb);
        tr.AddNewlyCreatedDBObject(tb, true);
        tr.Commit();
    }
  }

## 评论

**内容**: David said...
Hi, How can I apply line spacing and letter spacing for the text in a cell?
Reply
09/17/2013 at 03:26 PM

---
**内容**: Smith said...
Sory i don't know html and I've used
for (int i = 0;i < RowsNum;i++){
for (int j = 0;
'...
}
tb.SetAlignment(CellAlignment.MiddleCenter, 1)
}
Can I set up CellAlignment.MiddleCenter once?
Thanks you.
Reply
11/11/2019 at 04:48 PM

---
