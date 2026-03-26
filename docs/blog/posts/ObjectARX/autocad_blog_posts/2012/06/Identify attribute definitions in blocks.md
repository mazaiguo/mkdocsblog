---
title: "Identify attribute definitions in blocks"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - API
  - Block
  - Database
description: "Attributes definitions are stored along with all the entities which constitute the block table record. But when a reference is added to block, the ..."
author: Autodesk
---
# Identify attribute definitions in blocks

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/identify-attribute-definitions-in-blocks.html

## 文章内容

By Virupaksha Aithal
Attributes definitions are stored along with all the entities which constitute the block table record. But when a reference is added to block, the a corresponding references (Attributes reference) containing Attributes definitions are added. One way to identify the presence of Attributes definitions is by checking the block table record API “BlockTableRecord .HasAttributeDefinitions”.
 [CommandMethod("AttributeDefTest")]
 static public void AttributeDefTest()
 {
     Document doc = Application.DocumentManager.MdiActiveDocument;
     Database db = doc.Database;
     Editor ed = doc.Editor;
       PromptStringOptions opts =
        new PromptStringOptions("Enter block name");
     opts.AllowSpaces = true;
       PromptResult blockName = ed.GetString(opts);
       if (blockName.Status != PromptStatus.OK)
         return;
       using (Transaction tx =
                         db.TransactionManager.StartTransaction())
     {
         BlockTable blockTable = tx.GetObject(db.BlockTableId,
                                    OpenMode.ForRead) as BlockTable;
           if (blockTable.Has(blockName.StringResult))
         {
             BlockTableRecord block = tx.GetObject(
                              blockTable[blockName.StringResult],
                             OpenMode.ForRead) as BlockTableRecord;
             bool bAttDef = block.HasAttributeDefinitions;
               if (bAttDef)
             {
                 ed.WriteMessage("Block" + block.Name +
                             " contains attribute definiations\n");
             }
             else
             {
                 ed.WriteMessage("Block" + block.Name +
                     " does not contains attribute definiations\n");
             }
           }
         tx.Commit();
     }
 }

