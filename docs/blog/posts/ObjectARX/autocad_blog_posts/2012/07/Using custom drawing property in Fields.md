---
title: "Using custom drawing property in Fields"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - C++
  - Database
  - ObjectARX
description: ".NET/ObjectARX API allows you to use the custom properties to be used in fields. Below code sample shows procedure to link the custom property of t..."
author: Autodesk
---
# Using custom drawing property in Fields

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/using-custom-drawing-property-in-fields.html

## 文章内容

By Virupaksha Aithal
.NET/ObjectARX API allows you to use the custom properties to be used in fields. Below code sample shows procedure to link the custom property of the drawing. Below code assumes that the current drawing has a custom property called “Address”.
[CommandMethod("AddCusPropertyField")]
public void AddCusPropertyField()
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
        //%<\AcVar CustomDP.Address \f "%tc4">%
        MText text = new MText();
        text.Location = ppr.Value;
        ObjectId ModelSpaceId =
            SymbolUtilityServices.GetBlockModelSpaceId(db);
          BlockTableRecord record = Tx.GetObject(ModelSpaceId,
                             OpenMode.ForWrite) as BlockTableRecord;
        record.AppendEntity(text);
        Tx.AddNewlyCreatedDBObject(text, true);
          Field custom =
           new Field("%<\\AcVar CustomDP.Address \\f \"%tc4\">%");
          custom.EvaluationOption = FieldEvaluationOptions.Automatic;
        custom.Evaluate((int)(FieldEvaluationOptions.Automatic), db);
        text.SetField(custom);
        Tx.AddNewlyCreatedDBObject(custom, true);
          Tx.Commit();
          ed.Regen();
    }
}

## 评论

**内容**: Patrick said...
Hello from France, is there a way with .NET to create my own category of fields like this:
new Field("%<\\AcVar MyCustomDP.Address \\f \"%tc4\">%".
Thank you.
Reply
07/15/2014 at 07:18 AM

---
