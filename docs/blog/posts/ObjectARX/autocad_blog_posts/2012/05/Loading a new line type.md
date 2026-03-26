---
title: "Loading a new line type"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "You can use “Database.LoadLineTypeFile” API to load the particular line type to the drawing file. “LoadLineTypeFile” takes the line type file name ..."
author: Autodesk
---
# Loading a new line type

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/loading-a-new-line-type.html

## 文章内容

By Virupaksha Aithal
You can use “Database.LoadLineTypeFile” API to load the particular line type to the drawing file. “LoadLineTypeFile” takes the line type file name and the name of the line type to load.
 [CommandMethod("LoadLineType")]
 static public void LoadLineType()
 {
     Document doc = Application.DocumentManager.MdiActiveDocument;
     Database db = doc.Database;
       using (Transaction Tx =
        db.TransactionManager.StartTransaction())
     {
         LinetypeTable tbl =
             (LinetypeTable)Tx.GetObject(db.LinetypeTableId
                                            , OpenMode.ForRead);
         if (!tbl.Has("DASHED"))
         {
             db.LoadLineTypeFile("DASHED", "acad.lin");
         }
           Tx.Commit();
     }
 }

## 评论

**内容**: Steph said...
Hi,
I hope you could help me.
When I try your code in .NET I get an exception:
eBadLineTypeName ...
Do you have an Idea on what the problem could be ?
I load the file in a method in my custom library.
Not directly from the command code...
Thanks for your help.
Best Regards ...
S.
Reply
06/23/2020 at 11:17 PM

---
