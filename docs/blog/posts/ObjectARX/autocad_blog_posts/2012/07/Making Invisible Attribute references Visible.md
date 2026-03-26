---
title: "Making Invisible Attribute references Visible"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "If the defining block of the block reference has an invisible attribute definition, then block reference will have an invisible attribute reference..."
author: Autodesk
---
# Making Invisible Attribute references Visible

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/making-invisible-attribute-references-visible.html

## 文章内容

By Virupaksha Aithal
If the defining block of the block reference has an invisible attribute definition, then block reference will have an invisible attribute reference. But you can make such attribute references visible through program as shown in below code. Invisible attribute references can be identified using property “AttributeReference.Invisible” 
[CommandMethod("AttRefEdit")]
static public void AttRefEdit()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
              new PromptEntityOptions("\nSelect block reference");
    options.SetRejectMessage("\nSelect only block reference");
    options.AddAllowedClass(typeof(BlockReference), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if(acSSPrompt.Status != PromptStatus.OK)
        return;
      using (Transaction tx = db.TransactionManager.StartTransaction())
    {
        BlockReference blockRef = tx.GetObject(acSSPrompt.ObjectId,
                               OpenMode.ForRead) as BlockReference;
        AttributeCollection collection =
                                        blockRef.AttributeCollection;
          foreach (ObjectId id in collection)
        {
            AttributeReference attRef = tx.GetObject(id,
                         OpenMode.ForRead) as AttributeReference;
              //invisible?
            if (attRef.Invisible)
            {
                //yes, then make it visible
                attRef.UpgradeOpen();
                attRef.Invisible = false;
            }
        }
          tx.Commit();
    }
}

