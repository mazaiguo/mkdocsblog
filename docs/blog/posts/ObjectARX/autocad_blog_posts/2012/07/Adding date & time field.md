---
title: "Adding date & time field"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Database
  - Plugin
  - Unicode
description: "Below code shows the procedure to adds a Mtext which shows the date and time. Observe that code calls a API “SetField” taking “Field” object as inp..."
author: Autodesk
---
# Adding date & time field

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/adding-date-time-field.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to adds a Mtext which shows the date and time. Observe that code calls a API “SetField” taking “Field” object as input. The format string %<\AcVar Date \f "M/d/yyyy h:mm:ss tt">% is what makes the AutoCAD to populate the MText with date and time.
[CommandMethod("AddDateTimeField")]
public void AddDateTimeField()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptPointOptions ppo = new
                PromptPointOptions("\nSpecify insertion point: ");
      PromptPointResult ppr = ed.GetPoint(ppo);
      if (ppr.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        //%<\AcVar Date \f "M/d/yyyy h:mm:ss tt">%
        MText text = new MText();
        text.Location = ppr.Value;
        ObjectId ModelSpaceId =
            SymbolUtilityServices.GetBlockModelSpaceId(db);
          BlockTableRecord record = Tx.GetObject(ModelSpaceId,
                             OpenMode.ForWrite) as BlockTableRecord;
        record.AppendEntity(text);
        Tx.AddNewlyCreatedDBObject(text, true);
        Field datetime =
           new Field("%<\\AcVar Date \\f \"M/d/yyyy h:mm:ss tt\">%");
        datetime.Evaluate();
        text.SetField(datetime);
        Tx.AddNewlyCreatedDBObject(datetime, true);
          Tx.Commit();
    }
}

