---
title: "Loading the line types using wild card characters"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
description: "Below code shows the procedure to load all the line types starting with “ACAD” name. if “LoadLineTypeFile” is called with just “”, then all line ty..."
author: Autodesk
---
# Loading the line types using wild card characters

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/loading-the-line-types-using-wild-card-characters.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to load all the line types starting with “ACAD” name. if “LoadLineTypeFile” is called with just “*”, then all line types from the specified file will be loaded.
 [CommandMethod("LoadLineTypeAcad")]
 static public void LoadLineTypeAcad()
 {
     Document doc = Application.DocumentManager.MdiActiveDocument;
     Database db = doc.Database;
       try
     {
         db.LoadLineTypeFile("Acad*", "acad.lin");
           //use * to load all the line types
         //db.LoadLineTypeFile("*", "acad.lin");
     }
     catch
     {
     }
 }

