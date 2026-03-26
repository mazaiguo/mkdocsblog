---
title: "Making Invisible attribute definition Visible"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "Below code makes the invisible attributes definition visible form block definition and also forces all the references of edited block definition to..."
author: Autodesk
---
# Making Invisible attribute definition Visible

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/making-invisible-attribute-definition-visible.html

## 文章内容

By Virupaksha Aithal
Below code makes the invisible attributes definition visible form block definition and also forces all the references of edited block definition to update the with changes in the attribute definition.
[CommandMethod("AttDefEdit")]
static public void AttDefEdit()
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
      bool bEdited = false;
      using (Transaction tx = db.TransactionManager.StartTransaction())
    {
        BlockTable blockTable = tx.GetObject(db.BlockTableId,
                                   OpenMode.ForRead) as BlockTable;
          if (blockTable.Has(blockName.StringResult))
        {
            BlockTableRecord block = tx.GetObject(
                                  blockTable[blockName.StringResult],
                               OpenMode.ForRead) as BlockTableRecord;
              if (block.HasAttributeDefinitions)
            {
                foreach (ObjectId Id in block)
                {
                    DBObject dbObj =
                                  tx.GetObject(Id, OpenMode.ForRead);
                      if (dbObj is AttributeDefinition)
                    {
                        AttributeDefinition attDef =
                                        dbObj as AttributeDefinition;
                          if (attDef.Invisible)
                        {
                            bEdited = true;
                            attDef.UpgradeOpen();
                            attDef.Invisible = false;
                        }
                      }
                }
            }
          }
        tx.Commit();
    }
      if(bEdited)
        doc.SendStringToExecute("_.attsync " + "Name" + " " +
                    blockName.StringResult + "\n", true, false, true);
}

