---
title: "Getting field code from field object"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - Unicode
description: "Below code shows the procedure to get the field code from text object. Code first checks whether field object is associated with text object or not..."
author: Autodesk
---
# Getting field code from field object

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/getting-field-code-from-field-object.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to get the field code from text object. Code first checks whether field object is associated with text object or not using API “HasFields”. Then, uses “GetField” API of Mtext object to get the field object and shows the field code using API “GetFieldCode”.
[CommandMethod("GetFieldcode")]
public void GetFieldcode()
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
        //get the mleader
        MText mtext = Tx.GetObject(acSSPrompt.ObjectId,
                                   OpenMode.ForRead) as MText;
          if (!mtext.HasFields)
        {
            ed.WriteMessage("\nObject does not contain fields.");
            return;
        }
          ObjectId id = mtext.GetField("TEXT");
        Field field = Tx.GetObject(id, OpenMode.ForRead) as Field;
          string fldCode = field.GetFieldCode(FieldCodeFlags.AddMarkers
                                         | FieldCodeFlags.FieldCode);
        ed.WriteMessage("\nField code: " + fldCode);
          Tx.Commit();
    }
}

