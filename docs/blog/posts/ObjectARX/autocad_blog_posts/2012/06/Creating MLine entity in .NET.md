---
title: "Creating MLine entity in .NET"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Database
description: "Below code shows the procedure to at the Mline entity through .NET in AutoCAD. The important points to remember here is to set the Mline style and ..."
author: Autodesk
---
# Creating MLine entity in .NET

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/creating-mline-entity-in-net.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to at the Mline entity through .NET in AutoCAD. The important points to remember here is to set the Mline style and the setting of normal. In the below code, the database current mline style is used. You can get/set the current mlstyle using property “CmlstyleID”.
[CommandMethod("AddMline")]
public static void AddMline()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        //get the mline style
        Mline line = new Mline();
        //get the current mline style
        line.Style = db.CmlstyleID;
        line.Normal = Vector3d.ZAxis;
          line.AppendSegment(new Point3d(0, 0, 0));
        line.AppendSegment(new Point3d(10, 10, 0));
        line.AppendSegment(new Point3d(20, 10, 0));
          //open modelpace
        ObjectId ModelSpaceId =
            SymbolUtilityServices.GetBlockModelSpaceId(db);
          BlockTableRecord model = Tx.GetObject(ModelSpaceId,
                         OpenMode.ForWrite) as BlockTableRecord;
        model.AppendEntity(line);
        Tx.AddNewlyCreatedDBObject(line, true);
        Tx.Commit();
    }
}

