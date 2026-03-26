---
title: "Entity selection to modify properties"
date: 2015-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Palette
  - Selection
description: "To select entities and to have their properties displayed in the property palette, it is necessary for your command to use CommandFlags.Redraw. Thi..."
author: Autodesk
---
# Entity selection to modify properties

发布日期: 2015-01-01

原始链接: https://adndevblog.typepad.com/autocad/2015/01/entity-selection-to-modify-properties.html

## 文章内容

By Balaji Ramamoorthy
To select entities and to have their properties displayed in the property palette, it is necessary for your command to use CommandFlags.Redraw. This ensures that AutoCAD highlights the selection. You can then modify their common properties if you wish.
Here is a small code snippet to select all entities :
 [CommandMethod("SelectAll" , CommandFlags.Redraw)]
 static  public  void  SelectMethod()
 {
     Editor ed 
  = Application.DocumentManager.MdiActiveDocument.Editor;
       PromptSelectionResult psr = ed.SelectAll();
       using  (SelectionSet ss = psr.Value)
     {
         ed.SetImpliedSelection(ss.GetObjectIds());
     }
 }
  Here is a screenshot in AutoCAD :

