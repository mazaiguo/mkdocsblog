---
title: "Custom file selection obeying FILEDIA sysvar"
date: 2015-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Selection
description: "When we create a custom command, we want it to integrate with AutoCAD built-in behavior. One of those expected behaviors is the FILEDIA system vari..."
author: Autodesk
---
# Custom file selection obeying FILEDIA sysvar

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/custom-file-selection-obeying-filedia-sysvar.html

## 文章内容

By Augusto Goncalves
When we create a custom command, we want it to integrate with AutoCAD built-in behavior. One of those expected behaviors is the FILEDIA system variable, that indicates if a dialog will show when selecting files.
Many developer make direct use of Autodesk.AutoCAD.Windows.OpenFileDialog class, but this will call directly a dialog. The alternative is PromptSaveFileOptions, that can used with the Editor and has the FILEDIA behavior implemented.
The following code snippet show how to implement it.
Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
PromptSaveFileOptions pfso = new PromptSaveFileOptions("Select a file: ");
PromptFileNameResult pfnr = ed.GetFileNameForSave(pfso);
if (pfnr.Status != PromptStatus.OK) return;
 
string fileName = pfnr.StringResult;
// do something with the file

