---
title: "How to use acdbSetReferenced"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Block
  - DWG
description: "I want to stop an unreferenced anonymous block from being purged. I understood acdbSetReferenced() should do this, but my blocks are still being pu..."
author: Autodesk
---
# How to use acdbSetReferenced

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/how-to-use-acdbsetreferenced.html

## 文章内容

By Philippe Leefsma
Q:
I want to stop an unreferenced anonymous block from being purged. I understood acdbSetReferenced() should do this, but my blocks are still being purged after calling it. What should I do?
A:
Purging of anonymous blocks is done immediately after the drawing containing the block has been loaded. So you need to call acdbSetReferenced() before this happens.
Apparently your  function is being called after the purging has already being done.
What you should do is to sub-class  AcEditorReactor and call acdbSetReferenced() from within the dwgFileOpened() callback function of your new class as in the code snippet below:
-
void MyEditorReactor::dwgFileOpened(AcDbDatabase* x0, ACHAR* fileName)
{
        Acad::ErrorStatus stat;
        AcDbBlockTable *pBlockTable;
        x0->getSymbolTable(pBlockTable, AcDb::kForRead);
          AcDbBlockTableRecord *pBlockTableRecord;
        stat = pBlockTable->getAt(
            _T("*U1"),
            pBlockTableRecord, 
            AcDb::kForRead);
        pBlockTable->close();
          if (stat != Acad::eOk)
        {
                acutPrintf(_T("\nRecord not found"));
                return;
        }
          AcDbObjectId obId;
        obId = pBlockTableRecord->objectId();
        pBlockTableRecord->close();
        stat = acdbSetReferenced(obId);
          if (stat != Acad::eOk)
        {
                acutPrintf(_T("\nacdbSetReferenced() failed"));
                return;
        }
}

