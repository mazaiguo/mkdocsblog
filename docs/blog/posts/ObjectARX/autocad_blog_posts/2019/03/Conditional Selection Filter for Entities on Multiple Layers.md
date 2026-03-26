---
title: "Conditional Selection Filter for Entities on Multiple Layers"
date: 2019-03-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Layer
  - Selection
  - Unicode
description: "This post shows a simple way of drafting your selection filter, if you want to select a single entity of type A on specific layer L, and another en..."
author: Autodesk
---
# Conditional Selection Filter for Entities on Multiple Layers

发布日期: 2019-03-01

原始链接: https://adndevblog.typepad.com/autocad/2019/03/conditional-selection-filter-for-entities-on-multiple-layers.html

## 文章内容

By Madhukar Moogala
This post shows a simple way of drafting your selection filter, if you want to select a single entity of type A on specific layer L, and another entity of type B on several layers L1, L2, L3…. so on.
Lisp Code:
(defun C:FCTest()
(setq sel1 (ssget "_X" '(
                    (-4 . "<OR")  
                                 (-4 . "<AND")
                                        (0 . "TEXT")
                                        (8 . "Centro")
                                 (-4 . "AND>")
                                 (-4 . "<AND")
                                        (0 . "LWPOLYLINE")
                                               (-4 . "<OR")
                                                     (8 . "Secao_Projeto")
                                                     (8 . "Pontos_AcimaTolerancia")
                                                     (8 . "Pontos_AbaixoTolerancia")
                                                     (8 . "Pontos_ForaTolerancia")
                                                     (8 . "Pontos_NaTolerancia")
                                               (-4 . "OR>")
                                 (-4 . "AND>")
                    (-4 . "OR>"))
             )
)
(sslength sel1)
)
.NET code
public static void FC() {
 // Get the current document editor
 Editor acDocEd = Autodesk.AutoCAD.ApplicationServices.Core.Application.DocumentManager.MdiActiveDocument.Editor;

 // Create a TypedValue array to define the filter criteria

 //All objects meeting any of the Four criteria will get selected 
 TypedValue[] acTypValAr = {
  new TypedValue((int) DxfCode.Operator, "<or"),
  //Criteria 1
  new TypedValue((int) DxfCode.Operator, "<and"),
  new TypedValue((int) DxfCode.Start, "TEXT"),
  new TypedValue((int) DxfCode.LayerName, "Centro"),
  new TypedValue((int) DxfCode.Operator, "and>"),
  //Criteria 2
  new TypedValue((int) DxfCode.Operator, "<and"),
  new TypedValue((int) DxfCode.Start, "LWPOLYLINE"),
  new TypedValue((int) DxfCode.Operator, "<or"),
  new TypedValue((int) DxfCode.LayerName, "Secao_Projeto"),
  new TypedValue((int) DxfCode.LayerName, "Pontos_AcimaTolerancia"),
  new TypedValue((int) DxfCode.LayerName, "Pontos_AbaixoTolerancia"),
  new TypedValue((int) DxfCode.LayerName, "Pontos_ForaTolerancia"),
  new TypedValue((int) DxfCode.LayerName, "Pontos_NaTolerancia"),
  new TypedValue((int) DxfCode.Operator, "or>"),
  new TypedValue((int) DxfCode.Operator, "and>"),
  new TypedValue((int) DxfCode.Operator, "or>")
 };

 // Assign the filter criteria to a SelectionFilter object
 SelectionFilter acSelFtr = new SelectionFilter(acTypValAr);

 // Request for objects to be selected in the drawing area
 PromptSelectionResult acSSPrompt;
 acSSPrompt = acDocEd.GetSelection(acSelFtr);

 // If the prompt status is OK, objects were selected
 if (acSSPrompt.Status == PromptStatus.OK) {
  SelectionSet acSSet = acSSPrompt.Value;

  Autodesk.AutoCAD.ApplicationServices.Core.Application.ShowAlertDialog("Number of objects selected: " +
   acSSet.Count.ToString());
 } else {
  Autodesk.AutoCAD.ApplicationServices.Core.Application.ShowAlertDialog("Number of objects selected: 0");
 }
}
}

