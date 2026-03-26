---
title: "Exporting Table contents"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I would like to save the table contents to a file. How can I do this ?"
author: Autodesk
---
# Exporting Table contents

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/exporting-table-contents.html

## 文章内容

By Balaji Ramamoorthy
Issue
I would like to save the table contents to a file. How can I do this ?
Solution
AutoCAD command “TABLEEXPORT” can be used to save the contents of a table in the CSV format. One way to do this is to send this command using "SendStringToExecute".
You can also do the same thing without sending a command by traversing through the table contents as shown in the following code snippet. Please note that this is not a fully fledged CSV export code and it is only to demonstrate the traversing of the table data. You may want to improve upon it to write the CSV file.
[CommandMethod("TabExp")]
public void commandMethodTest()
{
    Document activeDoc = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      PromptEntityOptions peo
                = new PromptEntityOptions("\nSelect a table : ");
    peo.SetRejectMessage("\nMust be a table...");
    peo.AddAllowedClass(typeof(Table), true);
      PromptEntityResult per = ed.GetEntity(peo);
      if (per.Status != PromptStatus.OK)
        return;
      ObjectId oid = per.ObjectId;
      String fileName = String.Empty;
    SaveFileDialog sfd
            = new SaveFileDialog
                    (
                        "Save As CSV",
                        "Test",
                        "csv",
                        "Export Table As CSV",
                        SaveFileDialog.SaveFileDialogFlags.AllowAnyExtension
                    );
    if (sfd.ShowDialog() != System.Windows.Forms.DialogResult.OK)
    {
        return;
    }
    fileName = sfd.Filename;
      StreamWriter sw = new StreamWriter(fileName);
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        Table table = (Table)tr.GetObject(oid, OpenMode.ForRead);
          int Rows = table.Rows.Count;
        int Cols = table.Columns.Count;
          for (int row = 0; row < Rows; row++)
        {
            String sRow = String.Empty;
            for (int col = 0; col < Cols; col++)
            {
                if(sRow == String.Empty)
                    sRow = String.Format
                            (
                                "{0}",
                                table.Cells[row, col].GetTextString(FormatOption.FormatOptionNone)
                            );
                else
                    sRow = String.Format
                            (
                                "{0}, {1}",
                                sRow,
                                table.Cells[row, col].GetTextString(FormatOption.FormatOptionNone)
                            );
            }
            sw.WriteLine(sRow);
        }
        tr.Commit();
    }
      ed.WriteMessage("\nTable contents exported to " + fileName + " in CSV format.");
    sw.Close();
}

## 评论

**内容**: Andrey said...
Hi Balaji.
Lacks of CSV is the loss of cells formating (merge, cell/row/column styles, border settings). For the solving this problem, better to create XML + XSL. Such result can be looked in the browser like the formatted table, or can be parsed in any programm.
Regards
Reply
09/02/2012 at 12:06 AM

---
**内容**: Balaji said...
Hi Andrey,
You are right, CSV has those limitations.
Thanks for suggesting the XML alternative that can retain the formatting.
Regards
Reply
09/03/2012 at 04:04 AM

---
