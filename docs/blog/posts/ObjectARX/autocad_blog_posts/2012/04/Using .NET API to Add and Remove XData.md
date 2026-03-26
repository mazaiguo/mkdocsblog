---
title: "Using .NET API to Add and Remove XData"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Database
description: "The read/write property XData of the Autodesk.AutoCAD.DatabaseServices.DBObject class is used to get and set  XData of any database resident object..."
author: Autodesk
---
# Using .NET API to Add and Remove XData

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/using-net-api-to-add-and-remove-xdata-.html

## 文章内容

By Virupaksha Aithal
The read/write property XData of the Autodesk.AutoCAD.DatabaseServices.DBObject class is used to get and set  XData of any database resident object. This example demonstrates the same for an entity.
[CommandMethod("ADDXDATA")]
static public void AddXdata()
{
    Document doc =
        Application.DocumentManager.MdiActiveDocument;
    Database db =
        doc.Database;
    Transaction tr =
        db.TransactionManager.StartTransaction();
    using(tr)
    {
        Editor ed =
            Application.DocumentManager.MdiActiveDocument.Editor;
        // Prompt the user to select an entity
        PromptEntityResult ers =
           ed.GetEntity("Pick entity ");
        // Open the entity
        Entity ent =
          (Entity)tr.GetObject(ers.ObjectId,
                                        OpenMode.ForWrite);
        // Get the registered application names table
        RegAppTable regTable =
           (RegAppTable)tr.GetObject(db.RegAppTableId,
                                        OpenMode.ForRead);
          if(!regTable.Has("ADS"))
        {
            regTable.UpgradeOpen();
     // Add the application names that would be used to add Xdata
            RegAppTableRecord app =
                    new RegAppTableRecord();
            app.Name = "ADS";
            regTable.Add(app);
            tr.AddNewlyCreatedDBObject(app, true);
        }
        // Append the Xdata to the entity - two different
        // applications added.
        ent.XData = new ResultBuffer(new TypedValue(1001, "ADS"),
                                new TypedValue(1070, 100));
        tr.Commit();
    }
}
  [CommandMethod("REMXDATA")]
static public void RemoveXdata() // This method can have any name
{
    Document doc =
        Application.DocumentManager.MdiActiveDocument;
    Database db =
        doc.Database;
    Transaction tr =
        db.TransactionManager.StartTransaction();
    using (tr)
    {
        Editor ed =
            Application.DocumentManager.MdiActiveDocument.Editor;
        try
        {
            // Prompt the user to select an entity
            PromptEntityResult ers =
                ed.GetEntity("Pick entity ");
            // Open the selected entity
            Entity ent =
                (Entity)tr.GetObject(ers.ObjectId,
                            OpenMode.ForRead);
              ResultBuffer buffer =
                ent.GetXDataForApplication("ADS");
            // This call would ensure that the
            //Xdata of the entity associated with ADSK application
            //name only would be removed
            if (buffer != null)
            {
                ent.UpgradeOpen();
                ent.XData =
                    new ResultBuffer(new TypedValue(1001, "ADS"));
                buffer.Dispose();
            }
            tr.Commit();
        }
        catch
        {
            tr.Abort();
        }
    }
}

