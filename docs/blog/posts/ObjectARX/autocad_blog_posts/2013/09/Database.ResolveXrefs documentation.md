---
title: "Database.ResolveXrefs documentation"
date: 2013-09-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Database
  - ObjectARX
  - XREF
description: "If you are wondering what the parameters are used for…"
author: Autodesk
---
# Database.ResolveXrefs documentation

发布日期: 2013-09-01

原始链接: https://adndevblog.typepad.com/autocad/2013/09/databaseresolvexrefs-documentation.html

## 文章内容

by Fenton Webb
If you are wondering what the parameters are used for…
public void Database.ResolveXrefs(bool useThreadEngine, bool doNewOnly)
…then here’s the documentation on the equivalent ObjectARX function found in the ObjectARX Reference guide…
acdbResolveCurrentXRefs
Acad::ErrorStatus acdbResolveCurrentXRefs(
    AcDbDatabase* pHostDb, 
    bool useThreadEngine = true, 
    bool doNewOnly = false
);
acdbxref.h
Parameters Description
AcDbDatabase* pHostDb
Input pointer to the AcDbDatabase to be used as the host
bool useThreadEngine = true
Input Boolean indicating whether to use the thread engine for xref resolution
bool doNewOnly = false
Input Boolean indicating whether to process only newly added xrefs
Description
This function resolves existing xrefs in pHostDb.
If useThreadEngine is true, and other factors haven't disabled it, then the multi-thread engine is used for resolving the xrefs.
If doOnlyNew is true, only unresolved xref records are processed. Existing resolved xref AcDbLayerTableRecords, AcDbLinetypeTableRecords, and AcDbBlockTableRecords are ignored. In this case, the useThreadEngine argument also is ignored, and the multi-thread engine is not used.
If pHostDb points to an AcDbDatabase that is the primary database for a document in AutoCAD (in other words, a database that is loaded in the AutoCAD editor), doOnlyNew should be set to true to avoid reprocessing existing xrefs.
Warning
If pHostDb already contains resolved xrefs, then you must set the useThreadEngine argument to false. Otherwise, this function fails.
No document locking is done by this function. If pHostDb is associated with a document, the caller is responsible for locking that document.
This function is available to non-AutoCAD-based host applications.
Returns Acad::eOk if successful.

## 评论

**内容**: Charles Kraus said...
An automatic jump is expected for the running of the affairs. The change of the altcoin investments is piled for the terms. The sequences formed for the turns. Matter is selected out of the variety of the blocks for the field.
Reply
04/01/2023 at 04:04 AM

---
