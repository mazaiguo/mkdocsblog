---
title: "Why Some Methods in C# fail with an Error "cannot explicitly call operator or accessor"?"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C#
  - Database
  - Layer
description: "When using C# in .NET., one developer got an error “"cannot explicitly call operator or accessor" when he tried to build his project that uses cert..."
author: Autodesk
---
# Why Some Methods in C# fail with an Error "cannot explicitly call operator or accessor"?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/why-some-methods-in-c-fail-with-an-error-cannot-explicitly-call-operator-or-accessor.html

## 文章内容

By Barbara Han
When using C# in .NET., one developer got an error “"cannot explicitly call operator or accessor" when he tried to build his project that uses certain functions. Both utodesk.AutoCAD.DatabaseServices.Entity.get_LayerId and Autodesk.AutoCAD.DatabaseServices.Entity.get_Layer fail with this error.
The reason is that you should not use any get_ methods. To get an entity's layer name, use the Entity.Layer property instead, as demonstrated in the following sample:
    // Modal Command with localized name
    [CommandMethod("MyGroup", "MyCommand", "MyCommandLocal", CommandFlags.Modal)]
    public void MyCommand() // This method can have any name
    {
      // Put your command code here
      Document curDoc = Application.DocumentManager.MdiActiveDocument;
      Database db = curDoc.Database;
      Autodesk.AutoCAD.DatabaseServices.TransactionManager tm = db.TransactionManager;
        using (Transaction myT = tm.StartTransaction())
      {
        BlockTable bt = (BlockTable)tm.GetObject(db.BlockTableId, OpenMode.ForRead, false);
        BlockTableRecord btr = (BlockTableRecord)tm.GetObject(bt[BlockTableRecord.ModelSpace], OpenMode.ForRead,false);
        foreach (ObjectId acObjId in btr)
        {
          Entity ent = (Entity)myT.GetObject(acObjId, OpenMode.ForRead);
          string myLayName;
          myLayName = ent.Layer;
        }
          myT.Commit();
      }   
    }
This is same for other methods, for example get_LinetypeScale().
          double myScale;
          //myScale = ent.get_LinetypeScale();
          //Use .LinetypeScale instead
          myScale = ent.LinetypeScale;

## 评论

**内容**: G Switch said...
There is a big question in me, can I try another method on Java?
Reply
04/12/2023 at 11:43 PM

---
