---
title: "Where is acdbSaveAs2007?"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - Database
description: "I can see acdbSaveAs2004, acdbSaveAs2000, etc., but not acdbSaveAs2007, so I wonder how I can save the file to DWG 2007 format?"
author: Autodesk
---
# Where is acdbSaveAs2007?

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/where-is-acdbsaveas2007.html

## 文章内容

By Adam Nagy
I can see acdbSaveAs2004, acdbSaveAs2000, etc., but not acdbSaveAs2007, so I wonder how I can save the file to DWG 2007 format?
Solution
The acdbSaveAsXXX() functions are only there for compatibility reasons, and since AutoCAD 2010 they simply call AcDbDatabase::saveAs() underneath as you can see in dbmain.h
inline Acad::ErrorStatus acdbSaveAs2004(AcDbDatabase* pDb,
                                        const ACHAR* fileName)
{
    return pDb->saveAs(fileName, false, AcDb::kDHL_1800);
}

