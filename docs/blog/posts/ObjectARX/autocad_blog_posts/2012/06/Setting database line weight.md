---
title: "Setting database line weight"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Block
  - C++
  - Database
description: "You can set the database line weight using API  “Database.Celweight” in .NET API and using “AcDbDatabase::setCelweight()” api in ObjectARX as shown..."
author: Autodesk
---
# Setting database line weight

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/setting-database-line-weight.html

## 文章内容

By Virupaksha Aithal
You can set the database line weight using API  “Database.Celweight” in .NET API and using “AcDbDatabase::setCelweight()” api in ObjectARX as shown in below code.
.NET
Database db = doc.Database;
db.Celweight = LineWeight.ByBlock;
db.LineWeightDisplay = true;
ObjectARX
AcDbDatabase *pDb =
  acdbHostApplicationServices()->workingDatabase();
pDb->setCelweight(AcDb::kLnWt020);
pDb->setLineWeightDisplay(true);

