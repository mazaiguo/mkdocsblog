---
title: "Making a copy of an entity"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Database
description: "Below code demonstrates the use “DeepCloneObjects” in coping the object present in database. The code first selects a single entity, makes the deep..."
author: Autodesk
---
# Making a copy of an entity

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/making-a-copy-of-an-entity.html

## 文章内容

By Virupaksha Aithal
Below code demonstrates the use “DeepCloneObjects” in coping the object present in database. The code first selects a single entity, makes the deep copy of the entity and changes the color of the copied entity to red. To identify the new entity, the code makes use of “IdMapping” class which will have map between original entity and its copy.
[CommandMethod("copyEnt")]
public void copyEnt()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
            new PromptEntityOptions("\nSelect entity to copy");
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      ObjectIdCollection collection = new ObjectIdCollection();
    collection.Add(acSSPrompt.ObjectId);
      //make model space as owner for new entity
    ObjectId ModelSpaceId =
            SymbolUtilityServices.GetBlockModelSpaceId(db);
      IdMapping mapping = new IdMapping();
    db.DeepCloneObjects(collection, ModelSpaceId, mapping, false);
      //now open the new entity and change the color...
    using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        //get the map.
        IdPair pair1 = mapping[acSSPrompt.ObjectId];
          //new object
        Entity ent = Tx.GetObject(pair1.Value,
                                        OpenMode.ForWrite) as Entity;
          //change the color to red
        ent.ColorIndex = 1;
          Tx.Commit();
    }
  }

## 评论

**内容**: Mehdi said...
it's not just a code it's an Art
thanks a lot
Reply
01/06/2016 at 12:20 PM

---
