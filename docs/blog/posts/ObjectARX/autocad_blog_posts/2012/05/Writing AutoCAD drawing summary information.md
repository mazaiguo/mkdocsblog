---
title: "Writing AutoCAD drawing summary information"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
description: "Below code shows the procedure to add the drawing properties. The code uses DatabaseSummaryInfoBuilder & DatabaseSummaryInfo class to add the prope..."
author: Autodesk
---
# Writing AutoCAD drawing summary information

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/writing-autocad-drawing-summary-information.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to add the drawing properties. The code uses DatabaseSummaryInfoBuilder & DatabaseSummaryInfo class to add the properties.
[CommandMethod("WriteSummary")]
 static public void WriteSummary()
 {
     Document doc = Application.DocumentManager.MdiActiveDocument;
     Database db = doc.Database;
       DatabaseSummaryInfoBuilder infobuilder =
                            new DatabaseSummaryInfoBuilder();
       infobuilder.Title = "Test";
     infobuilder.Author = "DevTech";
     infobuilder.Comments = "This is a test drawing";
     infobuilder.Subject = "Testing";
       infobuilder.CustomPropertyTable.Add("A", "1");
     infobuilder.CustomPropertyTable.Add("B", "2");
     infobuilder.CustomPropertyTable.Add("C", "3");
       DatabaseSummaryInfo info = infobuilder.ToDatabaseSummaryInfo();
     db.SummaryInfo = info; //set the summary info
 }

## 评论

**内容**: Craig Nicholas said...
Very useful. Thanks.
Why is an intermediate DatabaseSummaryInfo instance required?
Also, do we need to lock the current document and wrap it in a transaction?
Reply
12/17/2012 at 12:21 PM

---
