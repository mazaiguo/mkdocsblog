---
title: "Point display in AutoCAD"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
description: "“PDMODE” system variable controls the point display in AutoCAD. This system variable can take values between 0 to 5 or 32 to 36 or 64 to 68 or 96 t..."
author: Autodesk
---
# Point display in AutoCAD

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/point-display-in-autocad.html

## 文章内容

By Virupaksha Aithal
“PDMODE” system variable controls the point display in AutoCAD. This system variable can take values between 0 to 5 or 32 to 36 or 64 to 68 or 96 to 100. You can change this system variable using database property “Pdmode”.
[CommandMethod("PointDisplay")]
public void PointDisplay()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptPointOptions ppo = new
                PromptPointOptions("\nSpecify insertion point: ");
      PromptPointResult ppr = ed.GetPoint(ppo);
      if (ppr.Status != PromptStatus.OK)
        return;
      //set the point display mode
    db.Pdmode = 35;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        ObjectId ModelSpaceId =
            SymbolUtilityServices.GetBlockModelSpaceId(db);
          BlockTableRecord record = Tx.GetObject(ModelSpaceId,
                             OpenMode.ForWrite) as BlockTableRecord;
          DBPoint pt = new DBPoint(ppr.Value);
        record.AppendEntity(pt);
        Tx.AddNewlyCreatedDBObject(pt, true);
          Tx.Commit();
    }
}

