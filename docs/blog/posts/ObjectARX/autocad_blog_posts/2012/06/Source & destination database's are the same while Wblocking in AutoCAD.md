---
title: "Source & destination database's are the same while Wblocking in AutoCAD"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Database
description: "Why is it that the source and destination databases are the same in 'otherWblock' method of AcRxEventReactor? This happens while wblocking an entir..."
author: Autodesk
---
# Source & destination database's are the same while Wblocking in AutoCAD

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/source-destination-databases-are-the-same-while-wblocking-in-autocad.html

## 文章内容

by Fenton Webb
Issue
Why is it that the source and destination databases are the same in 'otherWblock' method of AcRxEventReactor? This happens while wblocking an entire database.
Solution
This behavior is as designed. For performance reasons, there are certain cases where it will wblockClone() into the same database, write the cloned objects into the drawing file and then erase the cloned objects.
If you do not wish so then you have to call for AcDbDatabase::forceWblockDatabaseCopy().
Note: This method is non-functional unless called from within the AcRxEventReactor::wblockNotice() or
AcEditorReactor::wblockNotice() sent out for the wblock operation on which this method is to force the database copy.
For a more detailed description please refer to ObjectARX help files.

