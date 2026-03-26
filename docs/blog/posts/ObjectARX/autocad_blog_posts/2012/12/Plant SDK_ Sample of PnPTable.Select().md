---
title: "Plant SDK: Sample of PnPTable.Select()"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - DWG
  - SQL
  - Selection
description: "What if I want to apply a selection filter to PnPTable.Select()?"
author: Autodesk
---
# Plant SDK: Sample of PnPTable.Select()

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/plant-sdk-sample-of-pnptableselect.html

## 文章内容

By Marat Mirgaleev
Issue
What if I want to apply a selection filter to PnPTable.Select()?
Solution
One of the PnPTable.Select() overloads accepts a filter string as a parameter in a form of the SQLite's SELECT-WHERE clause. Please, note the syntax of the expression: if the field name contains spaces, it must be enclosed in quotes. The value is enclosed in apostrophes (you can find the escape sequences description in the SQLite documentation, if you search it online).
In this sample we are trying to use the PnPDrawings table to filter on the "Dwg Name" field:
  PnPTable tbl = db.Tables["PnPDrawings"];
  const string where = "\"Dwg Name\"='PIP-01-102.dwg'";
  PnPRow[] rows = tbl.Select(where);

