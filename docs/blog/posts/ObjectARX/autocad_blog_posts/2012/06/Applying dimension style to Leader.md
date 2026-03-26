---
title: "Applying dimension style to Leader"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
  - Dimension
description: "You can use Leader property DimensionStyle and SetDimstyleData to set the leader simension style. Below code shows the procedure"
author: Autodesk
---
# Applying dimension style to Leader

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/applying-dimension-style-to-leader.html

## 文章内容

By Virupaksha Aithal
You can use Leader property DimensionStyle and SetDimstyleData to set the leader simension style. Below code shows the procedure
[CommandMethod("LeaderDim")]
static public void LeaderDim()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
             new PromptEntityOptions("\nSelect Leader ");
    options.SetRejectMessage("\nSelect only Leader");
    options.AddAllowedClass(typeof(Leader), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      using (Transaction tx = db.TransactionManager.StartTransaction())
    {
        Leader leader = tx.GetObject(acSSPrompt.ObjectId,
                               OpenMode.ForRead) as Leader;
          DimStyleTable dimStyle = (DimStyleTable)tx.GetObject(
                               db.DimStyleTableId, OpenMode.ForRead);
        if(dimStyle.Has("TEST"))
        {
            DimStyleTableRecord dimStyleRec =
                                   (DimStyleTableRecord)tx.GetObject(
                                  dimStyle["TEST"],OpenMode.ForRead);
            leader.UpgradeOpen();
            leader.DimensionStyle = dimStyleRec.ObjectId;
            leader.SetDimstyleData(dimStyleRec);
        }
        tx.Commit();
    }
}

