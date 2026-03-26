---
title: "How to list all of the Annotation Style names in Plant3d P&ID using C#.NET"
date: 2012-05-01
categories:
  - Plant 3D
tags:
  - .NET
  - AutoCAD
  - C#
  - Plant 3D
description: "Here’s some code which shows how to list all of the Annotation Styles inside of a P&ID drawing…"
author: Autodesk
---
# How to list all of the Annotation Style names in Plant3d P&ID using C#.NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-list-all-of-the-annotation-style-names-in-plant3d-pid-using-cnet.html

## 文章内容

by Fenton Webb
Here’s some code which shows how to list all of the Annotation Styles inside of a P&ID drawing…
  // create Annotation by Fenton Webb, DevTech, Autodesk 1/5/2012
  [CommandMethod("listAllAnnotationStyles")]
  public void listAllAnnotationStyles()
  {
    // get the AutoCAD Editor object
    Editor ed = AcadApp.DocumentManager.MdiActiveDocument.Editor;
    // list the entries in the Autodesk_PNP dict
    using (DBDictionary annoStylesDict = DictionaryUtils.GetAnnotationStylesDictionaryId(ed.Document.Database, 0).Open(OpenMode.ForRead) as DBDictionary)
      foreach(DBDictionaryEntry entry in annoStylesDict)
        ed.WriteMessage("\n" + entry.Key);
  }

## 评论

**内容**: PDOTeam said...
What namespace is DictionaryUtils in?
Reply
05/22/2012 at 09:59 AM

---
**内容**: PDOTeam said...
Found it. PnPCommonDbxMgd.dll.
Reply
05/22/2012 at 10:07 AM

---
