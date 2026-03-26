---
title: "Copying Dimstyles between drawings using C#"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - Block
  - C#
  - DWG
  - Database
description: "This sample code demonstrates how to use WblockCloneObjects to copy objects between DWG Databases – a set of dimstyles  in this case. It also (quit..."
author: Autodesk
---
# Copying Dimstyles between drawings using C#

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/copying-dimstyles-between-drawings-using-c.html

## 文章内容

By Stephen Preston
This sample code demonstrates how to use WblockCloneObjects to copy objects between DWG Databases – a set of dimstyles  in this case. It also (quite arbitrarily) demonstrates a little know function for retrieving the most recently used dimstyles – GetDimRecentStyleList (or at least I’d not come across this function before ).
As an aside, a common mistake many people make when cloning DBObjects is to call their clone function. This must be used with care because it makes a shallow copy of the object. Depending what you’re doing with the clone, its usually best to wblockclone or deepclone instead.
   [CommandMethod("ImportStyles")]
    static public void importStyles()
    {
      Database db = new Database(false, false);
      db.ReadDwgFile("C:\\Styles.dwg", System.IO.FileShare.Read, true, "");
      // Get up to 6 most recently used styles
      ObjectIdCollection dimStyles = db.GetDimRecentStyleList();
      Database destDb =
              Application.DocumentManager.MdiActiveDocument.Database;
      ObjectId destDictId = destDb.DimStyleTableId;
      IdMapping iMap = new IdMapping();
      // Replace any existing styles
      destDb.WblockCloneObjects(dimStyles, destDictId, iMap,
                              DuplicateRecordCloning.Replace, false);
    }

## 评论

**内容**: Sanjay Kulkarni said...
Stephen,
1. I see that the drawing in which the styles are copied (destDb) is opened in AutoCAD. Is it essential? Can we do it silently by opening its database with RealDwg? It should be possible since we are not creating any geometry in destDb.
2. This is not really directly connected to AutoCAD but with VB, still I'll ask it.
Does it make any difference if 'db' is already being used by another process not started through VB and hence not using 'System.IO.FileShare.Read' (say manually).
In other words, does the db have to be opened using 'System.IO.FileShare.Read' and only then can be shared by other processes?
Of course I can try it and find out. But if you already know ......
Reply
08/11/2012 at 05:26 AM

---
