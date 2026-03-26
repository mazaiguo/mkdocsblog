---
title: "Insert Block from a different DWG using .NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Block
  - C#
  - DWG
  - Database
description: "Using the WblockCloneObjects() method, its possible to copy a particular block from a drawing in to the other drawing. The C# code snippet that sho..."
author: Autodesk
---
# Insert Block from a different DWG using .NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/insert-block-from-a-different-dwg-using-net-.html

## 文章内容

By Virupaksha Aithal
Using the WblockCloneObjects() method, its possible to copy a particular block from a drawing in to the other drawing. The C# code snippet that shows how to use WblockCloneObjects to copy a specific block "test" from the drawing available at "C:\TEMP\test.dwg".
[CommandMethod("InsertBlock")]
static public void InsertBlock() // This method can have any name
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    using(Database OpenDb = new Database(false, true))
    {
        OpenDb.ReadDwgFile("c:\\temp\\test.dwg",
            System.IO.FileShare.ReadWrite, true, "");
          ObjectIdCollection ids = new ObjectIdCollection();
        using (Transaction tr =
                OpenDb.TransactionManager.StartTransaction())
        {
             //For example, Get the block by name "TEST"
             BlockTable bt;
             bt = (BlockTable)tr.GetObject(OpenDb.BlockTableId
                                            , OpenMode.ForRead);
               if (bt.Has("TEST"))
             {
                 ids.Add(bt["TEST"]);
             }
             tr.Commit();
        }
          //if found, add the block
        if (ids.Count != 0)
        {
            //get the current drawing database
            Database destdb = doc.Database;
              IdMapping iMap = new IdMapping();
            destdb.WblockCloneObjects(ids, destdb.BlockTableId
                   ,iMap,DuplicateRecordCloning.Ignore, false);
        }
    }
}

## 评论

**内容**: Incognito said...
Thanks, really appreciate this snippet!
Reply
11/29/2013 at 04:01 AM

---
**内容**: andrea said...
Hi,
i test WblockCloneObjects in autocad 2013, it works fine,
but memory allocated was not disposed. If you put the code in loop autocad memory increase after every WblockCloneObjects and is not released (even if you close the document).
Is this an autocad bug?
Thank you
Reply
01/12/2015 at 08:39 AM

---
**内容**: Joey said in reply to andrea...
Hey andrea,
Please note my answer in the comment below.
Kind regards,
Joey van Doesburg
Reply
05/18/2016 at 05:57 AM

---
**内容**: Joey said...
Hey andrea,
I suggest you dispose the destdb object at the end of your using.
It might seem redundant but I noticed your problem as well and this fixed it for me.
Kind regards,
Joey van Doesburg
Scanopy
Reply
05/18/2016 at 05:41 AM

---
**内容**: Ravi Rao said...
Hi,
I am new to AutoCAD.NET development, had a requirement to insert
a block into my current drawing from an external dwg file.
I cud convert your code in vb.net and run the same. The compilation and
execution of the comment "Insert Block" went good without errors BUT the
desired block was not inserted....
Am I missing something, the code is as below:

Public Shared Sub InsertBlock()
' This method can have any name
Dim doc As Document = Application.DocumentManager.MdiActiveDocument
Using OpenDb As New Database(False, True)
OpenDb.ReadDwgFile("D:\Documents\TRIAL_1.dwg", System.IO.FileShare.ReadWrite, True, "")
Dim ids As New ObjectIdCollection()
Using tr As Transaction = OpenDb.TransactionManager.StartTransaction()
'For example, Get the block by name "TEST"
Dim bt As BlockTable
bt = DirectCast(tr.GetObject(OpenDb.BlockTableId, OpenMode.ForRead), BlockTable)
If bt.Has("drawing1") Then
ids.Add(bt("drawing1"))
End If
tr.Commit()
End Using
'if found, add the block
If ids.Count <> 0 Then
'get the current drawing database
Dim destdb As Database = doc.Database
Dim iMap As New IdMapping()
destdb.WblockCloneObjects(ids, destdb.BlockTableId, iMap,
DuplicateRecordCloning.Ignore, False)
destdb.Dispose()
End If
End Using
End Sub
Reply
05/20/2016 at 07:04 AM

---
**内容**: viru said in reply to Ravi Rao...
Hi,
Above code only imports the block. So try command insert in AutoCAD after running the above code
regards
Viru
Reply
05/23/2016 at 01:51 AM

---
**内容**: Sergey said in reply to Ravi Rao...
HI. Have you solved the problem? I have same problem :) Will be great if you can share solution!
Reply
10/07/2017 at 11:25 AM

---
