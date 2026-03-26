---
title: "Using the Table cell selected event"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Plugin
description: "When a table cell gets selected, you may interested in knowing the row and column index of the cell that was selected."
author: Autodesk
---
# Using the Table cell selected event

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/using-the-table-cell-selected-event.html

## 文章内容

By Balaji Ramamoorthy
When a table cell gets selected, you may interested in knowing the row and column index of the cell that was selected.
There is no such event in the public API but the "Autodesk.AutoCAD.Internal.Reactors" does provide one such event. Please note that the use of any API which is part of the "Internal" namespace is unsupported and subject to change. So, if you decide to use it, please test it thoroughly to see if it works correctly in your plugin.
Here is the sample code to use the "CellSelected" event from the "Autodesk.AutoCAD.Internal.Reactors.TableSubSelectFilter" class.
using Autodesk.AutoCAD.Internal.Reactors;
  void IExtensionApplication.Initialize()
{
    TableSubSelectFilter tsf = TableSubSelectFilter.Instance();
    if (tsf != null)
    {
        tsf.CellSelected
            += new TableSubSelectFilterEventHandler(tsf_CellSelected);
    }
}
  void IExtensionApplication.Terminate()
{
    TableSubSelectFilter tsf = TableSubSelectFilter.Instance();
    if (tsf != null)
    {
        tsf.CellSelected
            -= new TableSubSelectFilterEventHandler(tsf_CellSelected);
    }
}
  void  tsf_CellSelected(object sender, TableSubSelectFilterEventArgs e)
{
    if (! e.TableId.IsNull)
    {
        using (Transaction tr
            = e.TableId.Database.TransactionManager.StartTransaction())
        {
            Table table
                = tr.GetObject(e.TableId, OpenMode.ForRead) as Table;
              if (table.HasSubSelection)
            {
                CellRange cr = table.SubSelection;
                  System.Diagnostics.Debug.WriteLine
                    (
                        String.Format("\nSingle Cell ? : {0}",
                        cr.IsSingleCell)
                    );
                  System.Diagnostics.Debug.WriteLine
                    (
                        String.Format("\nTop row : {0}",
                        cr.TopRow)
                    );
                  System.Diagnostics.Debug.WriteLine
                    (
                        String.Format("\nLeft column : {0}",
                        cr.LeftColumn)
                    );
                  System.Diagnostics.Debug.WriteLine
                    (
                        String.Format("\nBottom Row : {0}",
                        cr.BottomRow)
                    );
                 System.Diagnostics.Debug.WriteLine
                    (
                        String.Format("\nRight column : {0}",
                        cr.RightColumn)
                    );
            }
            tr.Commit();
        }
    }
}

## 评论

**内容**: Tony Tanzillo said...
Thanks for your example.
While it may never be different in this case, when you have an ObjectId passed into an event handler, you should get the containing Database you're going to work with from the ObjectId's Database property, rather than assume it is the Database of the active document.
Reply
02/24/2013 at 08:19 PM

---
**内容**: Balaji said in reply to Tony Tanzillo...
Thanks, thats a valid point. I have made the change.
Reply
02/24/2013 at 10:04 PM

---
**内容**: Claudia Shoebridge said...
An auto and subject mean is struck for the formation of the routine for the citizens. The skills of the tech support austin for the future times. The manual report is submit for the terms for theatre diems for people.
Reply
06/03/2023 at 07:59 AM

---
