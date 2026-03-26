---
title: "Allowing only “required” type of objects during the selection."
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - Block
  - Database
  - Selection
description: "You can use “PromptEntityOptions.AddAllowedClass()” API, to allow users to select a particular type of entity during selection. Also you need to se..."
author: Autodesk
---
# Allowing only “required” type of objects during the selection.

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/allowing-only-required-type-of-objects-during-the-selection.html

## 文章内容

By Virupaksha Aithal
You can use “PromptEntityOptions.AddAllowedClass()” API, to allow users to select a particular type of entity during selection. Also you need to set the “SetRejectMessage” message before calling “AddAllowedClass”. For example, below code allows users to select only block references.
 [CommandMethod("SelectBlockRef")]
 static public void SelectBlockRef()
 {
     Document doc = Application.DocumentManager.MdiActiveDocument;
     Database db = doc.Database;
     Editor ed = doc.Editor;
       PromptEntityOptions options =
                new PromptEntityOptions("select block reference");
     options.SetRejectMessage(
                          "Select block referencees only" + "\n");
     options.AddAllowedClass(typeof(BlockReference), true);
     PromptEntityResult result = ed.GetEntity(options);
       if (result.Status != PromptStatus.OK)
         return;
       // obtain transaction manager
     using (Transaction tx =
                            db.TransactionManager.StartTransaction())
     {
         BlockReference bRef = tx.GetObject(result.ObjectId,
                                 OpenMode.ForRead) as BlockReference;
         BlockTableRecord block = tx.GetObject(bRef.BlockTableRecord,
                                OpenMode.ForRead) as BlockTableRecord;
         ed.WriteMessage("selected block is :" + block.Name + "\n");
         tx.Commit();
     }
 }

