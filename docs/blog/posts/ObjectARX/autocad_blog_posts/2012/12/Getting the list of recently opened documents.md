---
title: "Getting the list of recently opened documents"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Application class "Autodesk.AutoCAD.ApplicationServices.Application" class exposed a property “RecentDocuments”, which can be used to list out rece..."
author: Autodesk
---
# Getting the list of recently opened documents

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/getting-the-list-of-recently-opened-documents-.html

## 文章内容

By Virupaksha Aithal
Application class "Autodesk.AutoCAD.ApplicationServices.Application" class exposed a property “RecentDocuments”, which can be used to list out recently opened documents.
[CommandMethod("GetRecentDocument")]
static public void GetRecentDocument()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      foreach(RecentDocument recentDoc in Application.RecentDocuments)
    {
        ed.WriteMessage(recentDoc.Path + "\n");
    }
}

