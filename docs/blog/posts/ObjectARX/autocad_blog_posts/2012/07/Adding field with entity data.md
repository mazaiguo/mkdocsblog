---
title: "Adding field with entity data"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Plugin
  - Polyline
  - Unicode
description: "Below code shows the procedure to add a field object which shows an object specific data. Code actually shows the area of a polyline. Below code wh..."
author: Autodesk
---
# Adding field with entity data

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/adding-field-with-entity-data.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to add a field object which shows an object specific data. Code actually shows the area of a polyline. Below code when run in AutoCAD, prompts the user to select a ployline and then a location. An Mtext showing area of the selected polyline is created at the specified location.
[CommandMethod("AddAreaField")]
public void AddAreaField()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
           new PromptEntityOptions("\nSelect a polyline");
    options.SetRejectMessage("\nSelect polyline");
    options.AddAllowedClass(
       typeof(Autodesk.AutoCAD.DatabaseServices.Polyline), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      PromptPointOptions ppo = new
                PromptPointOptions("\nSpecify insertion point: ");
      PromptPointResult ppr = ed.GetPoint(ppo);
      if (ppr.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
       //%<\AcObjProp Object(%<\_ObjId 2128995688>%).Area \f "%lu2">%
        string strId = acSSPrompt.ObjectId.OldIdPtr.ToString();
        string str1 = "%<\\AcObjProp Object(%<\\_ObjId ";
        string str2 = ">%).Area \\f \"%lu2\">%";
        string format = str1 + strId + str2;
          MText text = new MText();
        text.Location = ppr.Value;
        ObjectId ModelSpaceId =
            SymbolUtilityServices.GetBlockModelSpaceId(db);
          BlockTableRecord record = Tx.GetObject(ModelSpaceId,
                             OpenMode.ForWrite) as BlockTableRecord;
        record.AppendEntity(text);
        Tx.AddNewlyCreatedDBObject(text, true);
        Field entField =
           new Field(format);
        entField.Evaluate();
        text.SetField(entField);
        Tx.AddNewlyCreatedDBObject(entField, true);
          Tx.Commit();
    }
}

## 评论

**内容**: Andrey Bushman (@AndreyBushman) said...
The example uses the polyline area. The name of a variable shall correspond to contents, otherwise it confuses a developer. In this case the name "datetime" doesn't correspond to contents of the field.
Reply
12/15/2012 at 04:09 AM

---
**内容**: Virupaksha Aithal said...
Hi,
Thanks for the comment. I have corrected the issue.
regards
Viru
Reply
12/17/2012 at 02:16 AM

---
**内容**: Dau Hung said...
How can I find any doccument about Field expression? I want to know structure of string format.
Reply
12/22/2018 at 08:29 PM

---
**内容**: petcon said...
can you trans the code to c++ i use AcDbObjectId::asOldId to replace ObjectId.OldIdPtr in c++ code but i get wrong result
Reply
07/20/2022 at 01:50 AM

---
