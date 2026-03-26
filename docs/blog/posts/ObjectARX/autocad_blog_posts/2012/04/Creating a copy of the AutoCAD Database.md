---
title: "Creating a copy of the AutoCAD Database"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Block
  - Database
description: "Use API “Database.Wblock()” to copy the complete database."
author: Autodesk
---
# Creating a copy of the AutoCAD Database

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/how-to-make-a-copy-of-the-autocad-database.html

## 文章内容

By Virupaksha Aithal
Use API “Database.Wblock()” to copy the complete database.
[CommandMethod("CopyDatabase")]
static public void CopyDatabase()
{
    Document doc =
        Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Database newDb = null;
    using (newDb = db.Wblock())
    {
        //use the newDb.
    }
}

