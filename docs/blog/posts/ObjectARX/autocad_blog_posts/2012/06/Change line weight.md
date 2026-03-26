---
title: "Change line weight"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
description: "To make the entity line weight visible in model space, you have to make the Database property “LineWeightDisplay” true. Below code shows a simple s..."
author: Autodesk
---
# Change line weight

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/change-line-weight-.html

## 文章内容

By Virupaksha Aithal
To make the entity line weight visible in model space, you have to make the Database property “LineWeightDisplay” true. Below code shows a simple sample which modifies the curves line type and enables the diaply of line weight by setting “LineWeightDisplay = true”.
[CommandMethod("changeLineWeight")]
public void changeLineWeight()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
              new PromptEntityOptions("\nSelect curve : ");
    options.SetRejectMessage("\nSelect only curves");
    options.AddAllowedClass(typeof(Curve), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      using (Transaction tx = db.TransactionManager.StartTransaction())
    {
        Curve ent = tx.GetObject(acSSPrompt.ObjectId,
                               OpenMode.ForWrite) as Curve;
          ent.LineWeight = LineWeight.LineWeight035;
          tx.Commit();
    }
      //make sure you set the LineWeightDisplay flag as true
    db.LineWeightDisplay = true;
}

