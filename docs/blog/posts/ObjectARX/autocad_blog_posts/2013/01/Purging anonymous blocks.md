---
title: "Purging anonymous blocks"
date: 2013-01-01
categories:
  - AutoCAD VBA
tags:
  - Block
  - VBA
description: "How do I purge all unnamed (and unreferenced) blocks from a drawing programmatically?"
author: Autodesk
---
# Purging anonymous blocks

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/purging-anonymous-blocks-using-vba.html

## 文章内容

By Daniel Du
Issue
How do I purge all unnamed (and unreferenced) blocks from a drawing programmatically?
Solution
To purge all unreferenced objects from a drawing, you can use the PurgeAll command.
Here is the VBA code:
Sub del_all()
 
    ThisDrawing.Application.ActiveDocument.PurgeAll()
 
End Sub
And here is a sample of .net(C#) code which deletes all unreferenced blocks:
[CommandMethod("ClearUnrefedBlocks")]
public void ClearUnrefedBlocks()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
    Database db = doc.Database;
 
    using (Transaction trans = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = trans.GetObject(db.BlockTableId, OpenMode.ForWrite)
            as BlockTable;
 
        foreach (ObjectId oid in bt)
        {
            BlockTableRecord btr = trans.GetObject(oid, OpenMode.ForWrite)
                as BlockTableRecord;
 
            if (btr.GetBlockReferenceIds(false, false).Count == 0
                && !btr.IsLayout)
            {
 
                btr.Erase();
            }
 
        }
 
        trans.Commit();
    }
 
}
Another option is to use Wblock. Any unreferenced symbols in the input database are omitted in the new database (which makes the new database potentially cleaner and smaller than the original).
[CommandMethod("ClrDb")]
public void ClearDatabase()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
    Database db = doc.Database;
 
    Database newDb = db.Wblock();
    newDb.SaveAs(@"c:\temp\clrdb.dwg", DwgVersion.Current);
 
}

## 评论

**内容**: Norman Yuan said...
This is VBA code and it has access to AcadApplication object directly. Why use version specific GetObject(,"AutoCAD.Application.19")? It is completely not necessary to possibly mislead newbies. Code like this from Autodesk dev team is a bit disappointing.
Reply
01/05/2013 at 08:43 AM

---
**内容**: Daniel Du said...
Thanks Norman for the comment, The code was in VB. To be clear, I changed it to VBA code and appended some C# code snippet for reference.
Reply
01/05/2013 at 10:38 PM

---
**内容**: Carlos said...
How about an example launching AcCoreConsole programatically?
Reply
04/26/2013 at 06:06 AM

---
