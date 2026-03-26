---
title: "Generating preview icons for programmatically created blocks"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Database
description: "Below code shows the procedure to generate the preview icons for programmatically created blocks. Code uses AutoCAD built in command “BLOCKICON” to..."
author: Autodesk
---
# Generating preview icons for programmatically created blocks

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/how-to-generate-preview-icons-for-programmatically-created-blocks.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to generate the preview icons for programmatically created blocks. Code uses AutoCAD built in command “BLOCKICON” to create the icon.
[CommandMethod("BlkPreview", CommandFlags.Session)]
static public void BlkPreview()
{
    Document doc =
        Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
      using (Transaction Tx =
        db.TransactionManager.StartTransaction())
    {
        BlockTable table =
            Tx.GetObject(db.BlockTableId,
                OpenMode.ForRead) as BlockTable;
          //"Test" - block whose preview icon need to Generate.
        BlockTableRecord blk =
            Tx.GetObject(table["Test"],
                    OpenMode.ForRead) as BlockTableRecord;
          object app = Application.AcadApplication;
          object ActiveDocument =
        app.GetType().InvokeMember(
          "ActiveDocument", BindingFlags.GetProperty,
         null, app, null
       );
          object[] dataArry = new object[1];
        dataArry[0] = "_.BLOCKICON " + blk.Name + "\n";
        ActiveDocument.GetType().InvokeMember("SendCommand",
            System.Reflection.BindingFlags.InvokeMethod,
            null, ActiveDocument, dataArry);
          Tx.Commit();
    }
}

## 评论

**内容**: Martin said...
Thanks for sharing
Reply
08/08/2017 at 04:06 AM

---
