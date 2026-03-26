---
title: "Identify the running command in document using AutoCAD.NET"
date: 2012-12-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "You can use “Autodesk.AutoCAD.ApplicationServices.Document” class’s property “CommandInProgress” to identify the running command name inside a docu..."
author: Autodesk
---
# Identify the running command in document using AutoCAD.NET

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/identify-the-running-command-in-document-using-autocadnet.html

## 文章内容

By Virupaksha Aithal
You can use “Autodesk.AutoCAD.ApplicationServices.Document” class’s property “CommandInProgress” to identify the running command name inside a document. This string is always returns the English command name.
Document doc = Autodesk.AutoCAD.ApplicationServices.
          Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;
  string str = doc.CommandInProgress;
  if (str != "")
{
    ed.WriteMessage(str + "\n");
}
else
{
    ed.WriteMessage("No command is running" + "\n");
}

## 评论

**内容**: ali said...
Hi Virupaksha,
When "selecting" objects is active it doesn't seem to identify it as a command. Is it right?
Thanks,
Reply
08/19/2013 at 07:40 AM

---
