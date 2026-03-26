---
title: "Difference between acdbOpenAcDbEntity and acdbOpenAcDbObject"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Database
  - ObjectARX
description: "acdbOpenAcDbEntity() provides a means to open database resident objects that are derived from AcDbEntity."
author: Autodesk
---
# Difference between acdbOpenAcDbEntity and acdbOpenAcDbObject

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/difference-between-acdbopenacdbentity-and-acdbopenacdbobject-.html

## 文章内容

By Balaji Ramamoorthy
acdbOpenAcDbEntity() provides a means to open database resident objects that are derived from AcDbEntity.
acdbOpenAcDbObject() provides a means to open database resident objects that are NOT derived from AcDbEntity, ones derived from AcDbObject.
However, you can still use acdbOpenAcDbObject() to open an AcDbEntity sub-class object provided that you do the (AcDbObject*&) cast. But YOU CANNOT USE acdbOpenAcDbEntity to open an AcDbObject level object.
ObjectARX also has acdbOpenObject(), this function implements further function definitions, among which are a template function definition which means that you do not need to cast the object if you use this function. It is available for all classes using the ACRX_DECLARE_MEMBERS macro either directly or indirectly through other macros.

