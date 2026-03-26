---
title: "Identify view change in AutoCAD"
date: 2016-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - ObjectARX
description: "I have received an query from an ADN partner recently on identifying the view change in AutoCAD, like when user pan or zoom using mouse."
author: Autodesk
---
# Identify view change in AutoCAD

发布日期: 2016-05-01

原始链接: https://adndevblog.typepad.com/autocad/2016/05/identify-view-change-in-autocad.html

## 文章内容

By Virupaksha Aithal
I have received an query from an ADN partner recently on identifying the view change in AutoCAD, like when user pan or zoom using mouse.
To identify the view change developers can use the editor rector viewChanged() (AcEditorReactor:: viewChanged()) in ObjectARX . However, in AutoCAD.NET API, the equivalent API is provided in document class Document::ViewChanged
[CommandMethod("ViewChnage")]
public void ViewChnage()
{
    Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
    doc.ViewChanged += doc_ViewChanged;
}

void doc_ViewChanged(object sender, EventArgs e)
{
    //
}

