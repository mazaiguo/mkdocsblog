---
title: "Iterating through the AutoCAD symbol tables"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Database
  - Layer
  - UCS
description: "AutoCAD symbol tables are ViewTable, ViewportTable , BlockTable, DimStyleTable, LayerTable, LinetypeTable, RegAppTable, TextStyleTable and UCSTable..."
author: Autodesk
---
# Iterating through the AutoCAD symbol tables

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/iterating-through-the-autocad-symbol-tables.html

## 文章内容

By Virupaksha Aithal
AutoCAD symbol tables are ViewTable, ViewportTable , BlockTable, DimStyleTable, LayerTable, LinetypeTable, RegAppTable, TextStyleTable and UCSTable. Below sample shows the procedure to iterate AutoCAD layer symbol table
[CommandMethod("accessLayers")]
 public void accessLayers()
 {
     Document doc = Application.DocumentManager.MdiActiveDocument;
     Database db = doc.Database;
     Editor ed = doc.Editor;
       using (Transaction tr =
                        db.TransactionManager.StartTransaction())
     {
         try
         {
             LayerTable layerTable = tr.GetObject(db.LayerTableId
                                , OpenMode.ForRead) as LayerTable;
             foreach (ObjectId LTRid in layerTable)
             {
                 LayerTableRecord LTR =
                            (LayerTableRecord)tr.GetObject(LTRid,
                                                OpenMode.ForRead);
                 ed.WriteMessage(LTR.Name + " is Frozen = " +
                                    LTR.IsFrozen.ToString() + "\n");
                 ed.WriteMessage(LTR.Name + " is Off = " +
                                        LTR.IsOff.ToString() + "\n");
                 ed.WriteMessage(LTR.Name + " is Locked = " +
                                    LTR.IsLocked.ToString() + "\n");
             }
             tr.Commit();
         }
         catch (System.Exception exception)
         {
             ed.WriteMessage(exception.Message);
             tr.Abort();
         }
     }
 }

