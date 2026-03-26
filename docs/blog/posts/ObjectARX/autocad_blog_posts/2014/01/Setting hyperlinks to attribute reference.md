---
title: "Setting hyperlinks to attribute reference"
date: 2014-01-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "At present, the hyperlink set at a block reference is not getting reflected in attributes associated with block reference. One workaround for this ..."
author: Autodesk
---
# Setting hyperlinks to attribute reference

发布日期: 2014-01-01

原始链接: https://adndevblog.typepad.com/autocad/2014/01/setting-hyperlinks-to-attribute-reference.html

## 文章内容

By Virupaksha Aithal
At present, the hyperlink set at a block reference is not getting reflected in attributes associated with block reference. One workaround for this issue is to set the hyperlinks to the associated attributes separately as shown in the below code.
[CommandMethod("SetHpLinkToAttRef")]
static public void SetHpLinkToAttRef()
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
          if(blockRef.Hyperlinks.Count != 0)
        {
            AttributeCollection collection =
                                       blockRef.AttributeCollection;
              foreach (ObjectId id in collection)
            {
                AttributeReference attRef = tx.GetObject(id,
                        OpenMode.ForWrite) as AttributeReference;         
                attRef.Hyperlinks.Add(blockRef.Hyperlinks[0]);
             }
        }
        tx.Commit();
    }
}

