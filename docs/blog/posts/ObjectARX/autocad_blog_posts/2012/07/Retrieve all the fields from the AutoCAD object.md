---
title: "Retrieve all the fields from the AutoCAD object"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Database
  - Unicode
description: "AutoCAD Objects like (Mtext/Text) can contain more than 1 field.  To access these field objects you need to use “Field” API “GetChildren”. Below co..."
author: Autodesk
---
# Retrieve all the fields from the AutoCAD object

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/retrieve-all-the-fields-from-the-autocad-object.html

## 文章内容

By Virupaksha Aithal
AutoCAD Objects like (Mtext/Text) can contain more than 1 field.  To access these field objects you need to use “Field” API “GetChildren”. Below code shows the procedure to use “GetChildren” API. To get the field object, API “GetField” (without any parameter) is used.
[CommandMethod("GetAllFields")]
public void GetAllFields()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
            new PromptEntityOptions("\nSelect a Mtext object");
    options.SetRejectMessage("\nSelect Mtext object");
    options.AddAllowedClass(typeof(MText), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        //get the mtext
        MText mtext = Tx.GetObject(acSSPrompt.ObjectId,
                                   OpenMode.ForRead) as MText;
          if (!mtext.HasFields)
        {
            ed.WriteMessage("\nObject does not contain fields.");
            return;
        }
          ObjectId id = mtext.GetField();
        Field field = Tx.GetObject(id, OpenMode.ForRead) as Field;
          Field[] fields = field.GetChildren();
          foreach (Field childField in fields)
        {
            string fldCode = childField.GetFieldCode(
                FieldCodeFlags.AddMarkers| FieldCodeFlags.FieldCode);
            ed.WriteMessage("\nField code: " + fldCode);
        }
          Tx.Commit();
    }
}

