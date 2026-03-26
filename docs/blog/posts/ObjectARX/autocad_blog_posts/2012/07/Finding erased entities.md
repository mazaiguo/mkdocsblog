---
title: "Finding erased entities"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - Block
  - Database
description: "You can use “BlockTableRecord” API “IncludingErased” to get the block table record with erased entities. Once you have erased entities, you can une..."
author: Autodesk
---
# Finding erased entities

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/indentifying-erased-entities.html

## 文章内容

By Virupaksha Aithal
You can use “BlockTableRecord” API “IncludingErased” to get the block table record with erased entities. Once you have erased entities, you can unease the entities if required as shown in below code.
[CommandMethod("GetErasedEntities")]
public void GetErasedEntities()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
    Database db = doc.Database;
      ObjectId ModelSpaceId =
            SymbolUtilityServices.GetBlockModelSpaceId(db);
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTableRecord record = tr.GetObject(ModelSpaceId,
                               OpenMode.ForRead) as BlockTableRecord;
          BlockTableRecord withErasedBTR = record.IncludingErased;
          foreach (ObjectId Id in withErasedBTR)
        {
            if (!Id.IsErased)
                continue;
              //un erase the entity...
              //GetObject, 3rd parameter openErased
            Entity ent = (Entity)tr.GetObject(Id,
                                           OpenMode.ForWrite, true);
            ent.Erase(false);
        }
        tr.Commit();
    }
}

