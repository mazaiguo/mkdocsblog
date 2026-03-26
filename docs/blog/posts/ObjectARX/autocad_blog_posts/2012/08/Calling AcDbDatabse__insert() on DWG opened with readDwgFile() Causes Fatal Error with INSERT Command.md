---
title: "Calling AcDbDatabse::insert() on DWG opened with readDwgFile() Causes Fatal Error with INSERT Command"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - DWG
  - Database
description: "I am using readDwgFile() to open a drawing in memory. I then use AcDbDatabase::insert(). After saving this drawing and opening it in AutoCAD, an er..."
author: Autodesk
---
# Calling AcDbDatabse::insert() on DWG opened with readDwgFile() Causes Fatal Error with INSERT Command

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/maintaining-the-windows-message-loop-when-your-code-is-busy-in-autocad-objectarx.html

## 文章内容

by Fenton Webb
Issue
I am using readDwgFile() to open a drawing in memory. I then use AcDbDatabase::insert(). After saving this drawing and opening it in AutoCAD, an error occurs when I use the INSERT command to insert the block that was inserted. "Error getting linetype from symbol table"
Solution
This problem occurs if the preserveSourceDatabase parameter for the insert() function is set to false. If this parameter is true then the block is added correctly to the database. When this parameter is false, a Hard Pointer to the AcDbLinetypeTableRecord for the entities in the block are missing. Here is a code example.
void ASDKtestSave()
{
  Acad::ErrorStatus es;

  AcDbDatabase *pMasterDb = new AcDbDatabase(false);
  es = pMasterDb->readDwgFile(_T("C:\\test.dwg"));
  pMasterDb->closeInput(true);

  AcDbDatabase *pXrefDb = new AcDbDatabase(false);
  es = pXrefDb->readDwgFile(_T("C:\\test2.dwg"));
  pXrefDb->closeInput(true);

  AcDbObjectId idOut;
  // if the preserverSourceDatabase parameter is false
  // the drawing corruption occurs - use true instead
  //es = pMasterDb->insert(idOut, _T("TestBlock"), pXrefDb, false);
  es = pMasterDb->insert(idOut, _T("TestBlock"), pXrefDb, true);

  es = pMasterDb->saveAs(_T("C:\\TestDrawing2.dwg"));

  delete pXrefDb;
  delete pMasterDb;

}

## 评论

**内容**: Vudv said...
I can not insert
Reply
11/13/2012 at 01:57 AM

---
