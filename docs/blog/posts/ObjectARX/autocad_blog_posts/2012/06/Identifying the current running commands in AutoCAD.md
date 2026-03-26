---
title: "Identifying the current running commands in AutoCAD"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Palette
description: "There are many scenarios like inside modeless dialog box or inside Palette, programmers need to know whether a command is running or a jugging is h..."
author: Autodesk
---
# Identifying the current running commands in AutoCAD

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/identifying-the-current-running-commands-in-autocad.html

## 文章内容

By Virupaksha Aithal
There are many scenarios like inside modeless dialog box or inside Palette, programmers need to know whether a command is running or a jugging is happening in AutoCAD. In such scenarios, to identify the state of AutoCAD, you can use below functions.
To identify the running commands: read the system variable “CMDNAMES”
To identify the jigging status, call the editor function “IsDragging”
//AutoCADAppServices is defined as
//using AutoCADAppServices = Autodesk.AutoCAD.ApplicationServices;
Document doc = AutoCADAppServices.Application.
                    DocumentManager.MdiActiveDocument;
  Editor ed = doc.Editor;
  object names =
        AutoCADAppServices.Application.GetSystemVariable("CMDNAMES");
  string strText = names as string;
  if (strText.Length != 0)
    ed.WriteMessage(strText + " command is running\n");
else
    ed.WriteMessage("No command is running\n");
  if (ed.IsDragging)
{
    ed.WriteMessage("Dragging is in progress\n");
}

