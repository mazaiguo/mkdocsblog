---
title: "How to Get Default Drawing Format"
date: 2015-06-01
categories:
  - AutoCAD
tags:
  - API
  - DWG
description: "I have recently received a query from an ADN partner whether it is possible to get default Save As format details from an API or Command, I’m not s..."
author: Autodesk
---
# How to Get Default Drawing Format

发布日期: 2015-06-01

原始链接: https://adndevblog.typepad.com/autocad/2015/06/how-to-get-default-drawing-format.html

## 文章内容

By Madhukar Moogala
I have recently received a query from an ADN partner whether it is possible to get default Save As format details from an API or Command, I’m not sure if we have command to get, but we do have a simple API to get the details.
  Following tiny code snippet will give details of
  void testDWGFormatDefault()
{
/*The format mentioned in Options/ Open and Save*/
AcApDocument ::SaveFormat saveFormat =
acDocManagerPtr()->defaultFormatForSave();
AcDb::AcDbDwgVersion dwgVersion;
AcDb::MaintenanceReleaseVersion maintainRelVersion;
AcApDocument* pCurDoc = acDocManagerPtr()->curDocument();
/*To get relevant dwg and mReleaseVersions*/
if( !eOkVerify(pCurDoc->getDwgVersionFromSaveFormat(saveFormat,
dwgVersion,
maintainRelVersion)))
return;
}

## 评论

**内容**: Alexander Rivilis said...
Only ObjectARX 2015 and 2016 have method AcApDocument::getDwgVersionFromSaveFormat
Reply
06/23/2015 at 03:20 AM

---
