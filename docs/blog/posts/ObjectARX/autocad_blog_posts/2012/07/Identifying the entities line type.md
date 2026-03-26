---
title: "Identifying the entities line type"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Database
  - Layer
description: "Each curve entity stores the line type it uses to draw. The information is stored as object id (“LinetypeId”) in each curve object. But some cases,..."
author: Autodesk
---
# Identifying the entities line type

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/identifying-the-entities-line-type.html

## 文章内容

By Virupaksha Aithal
Each curve entity stores the line type it uses to draw. The information is stored as object id (“LinetypeId”) in each curve object. But some cases, the curve will be using its layer’s line type.  In such cases, you need to get the layer line type to identify the actual line type used be the curve.
[CommandMethod("LineTypeName")]
public void LineTypeName()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
              new PromptEntityOptions("\nSelect curve : ");
    options.SetRejectMessage("\nSelect only curves");
    options.AddAllowedClass(typeof(Curve), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      using (Transaction tx = db.TransactionManager.StartTransaction())
    {
        Curve ent = tx.GetObject(acSSPrompt.ObjectId,
                               OpenMode.ForRead) as Curve;
          ObjectId id = ent.LinetypeId;
          if (id == db.ByLayerLinetype)
        {
            //get the layer..
            ObjectId layerId = ent.LayerId;
            LayerTableRecord layer = tx.GetObject(layerId,
                               OpenMode.ForRead) as LayerTableRecord;
              id = layer.LinetypeObjectId;
        }
        //open the linetype table record
        LinetypeTableRecord linetype = tx.GetObject(id,
                            OpenMode.ForRead) as LinetypeTableRecord;
          ed.WriteMessage("Line type used by curve is " +
                                               linetype.Name + "\n");
          tx.Commit();
    }
}

