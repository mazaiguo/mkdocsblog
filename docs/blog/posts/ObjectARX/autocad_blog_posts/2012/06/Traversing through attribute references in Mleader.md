---
title: "Traversing through attribute references in Mleader"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "Mleader entity allows users to set the block (including user defined custom block) as the content type. Many times, these blocks contain attribute ..."
author: Autodesk
---
# Traversing through attribute references in Mleader

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/traversing-through-attribute-references-in-mleader.html

## 文章内容

By Virupaksha Aithal
Mleader entity allows users to set the block (including user defined custom block) as the content type. Many times, these blocks contain attribute definitions and hence Mleader maintains attribute references to the contained attribute definitions of the block table record.  Below code show the procedure to get the attribute reference for selected Mleader.
[CommandMethod("mLeaderBlockTest")]
public void mLeaderBlockTest()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
            new PromptEntityOptions("\nSelect a Mleader with block");
    options.SetRejectMessage("\nSelect only Mleader with block");
    options.AddAllowedClass(typeof(MLeader), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        //get the mleader
        MLeader mleader = Tx.GetObject(acSSPrompt.ObjectId,
                                   OpenMode.ForRead) as MLeader;
          ObjectId blockId = mleader.BlockContentId;
        if (blockId == ObjectId.Null)
        {
            ed.WriteMessage("Mleader does not contains block\n");
            return;
        }
          BlockTableRecord record = Tx.GetObject(blockId,
                               OpenMode.ForRead) as BlockTableRecord;
          if(!record.HasAttributeDefinitions)
        {
            ed.WriteMessage("No attributes in block\n");
            return;
        }
        foreach (ObjectId Id in record)
        {
            DBObject dbObj = Tx.GetObject(Id, OpenMode.ForRead) ;
              if (dbObj is AttributeDefinition)
            {
                AttributeDefinition attDef =
                                        dbObj as AttributeDefinition;
                using (AttributeReference attRef =
                                      mleader.GetBlockAttribute(Id))
                {
                    ed.WriteMessage("Reference text for tag " +
                     attDef.Tag + " is " + attRef.TextString + "\n");
                }
            }
        }
          Tx.Commit();
    }
  }

