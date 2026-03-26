---
title: "Opening erased Objects"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "When you erase an entity, it is immediately marked as erased. But you can always get back the entity as entity is not removed out of Database. For ..."
author: Autodesk
---
# Opening erased Objects

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/opening-erased-objects.html

## 文章内容

By Virupaksha Aithal
When you erase an entity, it is immediately marked as erased. But you can always get back the entity as entity is not removed out of Database. For opening erased object, you need to specific the true as 3rd parameter to “GetObject” API of “Transaction”.
Refer below code.
static ObjectId entId = ObjectId.Null;
  [CommandMethod("eraseTest")]
public static void eraseTest()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      if (entId == ObjectId.Null)
    {
        PromptEntityResult ers = ed.GetEntity("Pick entity ");
          if (ers.Status != PromptStatus.OK)
        {
            return;
        }
        entId = ers.ObjectId;
    }
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        //check if entity is already in erase state..
        if (entId.IsErased)
        {
            //GetObject, 3rd parameter openErased
            Entity ent = (Entity)tr.GetObject(entId,
                                           OpenMode.ForWrite, true);
            ent.Erase(false);
              entId = ObjectId.Null;
          }
        else
        {
            Entity ent = (Entity)tr.GetObject(entId,
                                              OpenMode.ForWrite);
            ent.Erase();
        }
        tr.Commit();
    }
    }

