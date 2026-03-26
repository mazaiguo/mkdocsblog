---
title: "What is the purpose of acedConvertEntityToHatch?"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - API
  - Block
  - C++
  - Database
  - Hatch
description: "Here is a common mistake programmers can do when using that API:"
author: Autodesk
---
# What is the purpose of acedConvertEntityToHatch?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/what-is-the-purpose-of-acedconvertentitytohatch.html

## 文章内容

By Philippe Leefsma
  Here is a common mistake programmers can do when using that API:
I am trying to use acedConvertEntityToHatch to create a hatch directly from some lines. Is there additional documentation describing how to use this function?
  This function is for converting old hatches (R13) that were anonymous block (*U and *X) references. The block reference must be database resident and have "ACAD" Xdata containing the old "HATCH" Xdata. A return value of  eNotThatKindOfClass usually indicates a problem processing the Xdata.
Refer to the documentation in the ObjectARX Reference for acedConvertEntityToHatch:
pHatch must be a newly created, and open for write but not added to the database yet. pEnt must be an AcDbBlockReference or AcDbSolid, otherwise you should get the "eIIllegalEntityType" error status.

