---
title: "Use of Explode API"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - Block
  - Database
description: "Below code shows the use of “Explode” API to explode the block reference through API. Explode API will return array of non database resident DBObje..."
author: Autodesk
---
# Use of Explode API

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/use-of-explode-api.html

## 文章内容

By Virupaksha Aithal
Below code shows the use of “Explode” API to explode the block reference through API. Explode API will return array of non database resident DBObject. If required, the DBObject array return from “Explode” API can be added to database.
[CommandMethod("explodeRef")]
static public void explodeRef()
{
 Document doc = Application.DocumentManager.MdiActiveDocument;
 Database db = doc.Database;
 Editor ed = doc.Editor;
   PromptEntityOptions options =
           new PromptEntityOptions("\nSelect block reference");
 options.SetRejectMessage("\nSelect only block reference");
 options.AddAllowedClass(typeof(BlockReference), false);
   PromptEntityResult acSSPrompt =
         ed.GetEntity(options);
   using (Transaction tx =
                     db.TransactionManager.StartTransaction())
 {
     BlockReference blockRef = tx.GetObject(acSSPrompt.ObjectId,
                            OpenMode.ForRead) as BlockReference;
       DBObjectCollection entitySet = new DBObjectCollection();
     blockRef.Explode(entitySet);
       BlockTableRecord table = (BlockTableRecord)tx.GetObject(
                          db.CurrentSpaceId, OpenMode.ForWrite);
     foreach (DBObject obj in entitySet)
     {
         if (obj is Entity)
         {
             table.AppendEntity((Entity)obj);
             tx.AddNewlyCreatedDBObject(obj, true);
         }
     }
       tx.Commit();
 }
}

## 评论

**内容**: Pete Elliott said...
Just wondering the difference between this method and blockRef.ExplodeToOwnerSpace?
Reply
05/16/2012 at 11:26 AM

---
**内容**: Virupaksha aithal said...
Hi
explodeToOwnerSpace function works similar to “explode” function, except that it appends the resulting entities to the block that owns the reference on which this method was called.
This API also, retains the xdata attached to basic entities which constituted the block.
Thanks
Viru
Reply
05/16/2012 at 11:24 PM

---
**内容**: petcon said...
my english is very poor，still can not understand the difference between the two functions
Reply
05/17/2012 at 03:33 AM

---
**内容**: Virupaksha aithal said...
Hi,
Yes, there is no big difference between two functions except one (explode) returns a array of in-memory objects and other (explodeToOwnerSpace) adds the objects directly to database.
Thanks
Viru
Reply
05/17/2012 at 04:33 AM

---
**内容**: petcon said in reply to Virupaksha aithal...
i see thx
Reply
05/17/2012 at 10:20 PM

---
**内容**: Madhukar Moogala said...
The code posted here is a simple usage example. It adds the exploded entity collection to the current space, so it is basically reproducing the functionality of ExplodeToOwnerSpace. In many cases you'll use Explode when you don't want to add all the entities back to the same BlockTableRecord the exploded entity came from, or if you want to perform some transformations on the exploded entities before adding them to the drawing, or if you don't want to add them to the drawing at all.
Its up to you to decide which function you want to use in any given scenario.
Reply
05/17/2012 at 08:05 AM

---
**内容**: B2D2 said...
Also note that exploding block references with attribute references would lose the attribute value. Using an approach such as this would allow you to do extra processing to replace the definisions with DBText or MText.
Reply
05/22/2012 at 07:50 PM

---
