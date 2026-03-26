---
title: "AcisIn and acisout in .NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Database
  - Solid
description: "Below code shows the usage of AcisOut & AcisIn API in importing and exporting of Solid3d."
author: Autodesk
---
# AcisIn and acisout in .NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/acisin-and-acisout-in-net.html

## 文章内容

By Virupaksha Aithal
Below code shows the usage of AcisOut & AcisIn API in importing and exporting of Solid3d.
[CommandMethod("acisout_test")]
public void acisout_test() // This method can have any name
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptSelectionResult result = ed.GetSelection();
      if (result.Status != PromptStatus.OK)
    {
     return;
    }
      using (Transaction tran =
                    db.TransactionManager.StartTransaction())
    {
         ObjectId[] Idarray = result.Value.GetObjectIds();
         DBObjectCollection objectCollection =
                                     new DBObjectCollection();
         DBObject dbObject = null;
         foreach (ObjectId Id in Idarray)
         {
             dbObject = tran.GetObject(Id, OpenMode.ForRead);
               if (dbObject is Solid3d || dbObject is
                        Autodesk.AutoCAD.DatabaseServices.Region
                                             || dbObject is Body)
             {
                 objectCollection.Add(dbObject);
             }
         }
           Body.AcisOut("C:\\Temp\\test.sat", objectCollection);
         tran.Commit();
    }
}
  [CommandMethod("acisin_test")]
public void acisin_test() // This method can have any name
{
    //get the working database
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction tran =
                      db.TransactionManager.StartTransaction())
    {
        //get block table
        BlockTable table = (BlockTable)tran.GetObject(
                             db.BlockTableId, OpenMode.ForRead);
          //get model space
        BlockTableRecord model = tran.GetObject(
                        table[BlockTableRecord.ModelSpace],
                          OpenMode.ForWrite) as BlockTableRecord;
          //use static function of body to read a acis file
        DBObjectCollection MyCollection =
                               Body.AcisIn("c:\\temp\\test.sat");
          foreach (DBObject ACISInObject in MyCollection)
        {
            if (ACISInObject is Entity)
            {
                Entity ACISEntity = (Entity)ACISInObject;
                model.AppendEntity(ACISEntity);
                tran.AddNewlyCreatedDBObject(ACISEntity, true);
            }
          }
          tran.Commit();
    }
}

