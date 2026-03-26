---
title: "Creating a new dimension style and make it as current"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - Database
  - Dimension
description: "Below code create a new dimension style and make the newly created dimension style as current."
author: Autodesk
---
# Creating a new dimension style and make it as current

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/creating-a-new-dimension-style-and-make-it-as-current.html

## 文章内容

By Virupaksha Aithal
Below code create a new dimension style and make the newly created dimension style as current.
[CommandMethod("NewDimStyle")]
 public void NewDimStyle()
 {
     Database db =
         Application.DocumentManager.MdiActiveDocument.Database;
     using (Transaction trans =
         db.TransactionManager.StartTransaction())
     {
         DimStyleTable DimTabb =
             (DimStyleTable)trans.GetObject(db.DimStyleTableId,
                            OpenMode.ForRead);
         ObjectId dimId = ObjectId.Null;
           if (!DimTabb.Has("Test"))
         {
             DimTabb.UpgradeOpen();
             DimStyleTableRecord newRecord =
                            new DimStyleTableRecord();
             newRecord.Name = "Test";
             dimId = DimTabb.Add(newRecord);
             trans.AddNewlyCreatedDBObject(newRecord, true);
         }
         else
         {
             dimId = DimTabb["Test"];
         }
         DimStyleTableRecord DimTabbRecaord =
             (DimStyleTableRecord)trans.GetObject(dimId,
                                            OpenMode.ForRead);
           if (DimTabbRecaord.ObjectId != db.Dimstyle)
         {
             db.Dimstyle = DimTabbRecaord.ObjectId;
             db.SetDimstyleData(DimTabbRecaord);
         }
         trans.Commit();
     }
   }

## 评论

**内容**: Matus Brlit said...
When I create a new dimension style, it looks like override of the previously current one. In the description, it says ISO-25 + 'all the overriden properties'
It then causes problem when changing arrow type. Is there a way to create new dimension style without any relation to an existing one?
Reply
11/27/2012 at 02:46 AM

---
**内容**: Nathan R said in reply to Matus Brlit...
I know this is quite old but for future searchers like me: I ran into the same issue (existing drawing, adding a new style and changing some of the dims to use the new style).
I commented out the db.SetDimstyleData line and it stopped overriding the existing style.
Reply
01/14/2022 at 10:51 AM

---
**内容**: Viru said...
Hi,
above code should create a new dimension style without any relation to exiting one. So, not sure about steps you are following to create the new dim style
regards
Viru
Reply
12/04/2012 at 01:06 AM

---
**内容**: owen gayo said...
how can i use dimension style from another drawing to the current drawing
Reply
01/29/2014 at 03:43 AM

---
