---
title: "Setting layer color override for a viewport using AccoreConsole"
date: 2015-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - DWG
  - Layer
  - Plugin
description: "Here is a code snippet to set the layer color override for the viewports in all the layouts in a drawing. AccoreConsole can be used to automate set..."
author: Autodesk
---
# Setting layer color override for a viewport using AccoreConsole

发布日期: 2015-08-01

原始链接: https://adndevblog.typepad.com/autocad/2015/08/setting-layer-color-override-for-a-viewport-using-accoreconsole.html

## 文章内容

By Balaji Ramamoorthy
Here is a code snippet to set the layer color override for the viewports in all the layouts in a drawing. AccoreConsole can be used to automate setting this override, if you need to repeat this for several drawings in a folder. Here is the AutoCAD script and the custom command to set the override for a layer named "Layer 1" :
 ;<--- Script starts here
 (command "_.Netload"  "D:\\\\Temp\\\\CustomPlugin.dll" )
 SetLayerColorOverride
 SAVEAS
 2013
 D:\\Temp\\Test_1.dwg
   ;<--- Script ends here
   using  Autodesk.AutoCAD.Runtime; 
 using  Autodesk.AutoCAD.EditorInput; 
 using  Autodesk.AutoCAD.DatabaseServices; 
 using  Autodesk.AutoCAD.ApplicationServices; 
 using  Autodesk.AutoCAD.Colors;
   [CommandMethod("SetLayerColorOverride" )]
 public  void  SetLayerColorOverride()
 {
     DocumentCollection docs 
     = Autodesk.AutoCAD.ApplicationServices
         .Core.Application.DocumentManager;
       Document doc = docs.MdiActiveDocument;
     Editor ed = doc.Editor;
     Database db = doc.Database;
       db.TileMode = false ;
     LayoutManager lm = LayoutManager.Current;
     using  (Transaction tr 
         = db.TransactionManager.StartTransaction())
     {
         LayerTable lt = tr.GetObject(
             db.LayerTableId, 
             OpenMode.ForWrite, false ) as  LayerTable;
           String layerName = "Layer1" ;
         if  (!lt.Has(layerName))
             return ;
           LayerTableRecord ltr = tr.GetObject(
             lt[layerName], 
             OpenMode.ForWrite) as  LayerTableRecord;
           using  (DBDictionary layoutDict = tr.GetObject(
             db.LayoutDictionaryId, 
             OpenMode.ForRead) as  DBDictionary)
         {
             foreach  (DBDictionaryEntry entry in  layoutDict)
             {
                 ObjectId layoutId = entry.Value;
                   Layout layout = tr.GetObject(
                     layoutId, 
                     OpenMode.ForRead) as  Layout;
                 lm.CurrentLayout = layout.LayoutName;
                   BlockTableRecord btr = tr.GetObject(
                     layout.BlockTableRecordId, 
                     OpenMode.ForRead) as  BlockTableRecord;
                 foreach  (ObjectId id in  btr)
                 {
                     if  (id.ObjectClass 
                         == RXClass.GetClass(typeof (Viewport)))
                     {
                         Viewport vp = tr.GetObject(
                             id, OpenMode.ForRead) as  Viewport;
                         if  (vp != null  && vp.Number > 1)
                         {
                             LayerViewportProperties lvp 
                                 = ltr.GetViewportOverrides(id);
                             lvp.Color 
                                 = Color.FromColorIndex(
                                 ColorMethod.ByAci, (short )vp.Number);
                             vp.UpdateDisplay();
                         }
                     }
                 }
             }
         }
         tr.Commit();
     }
 }

