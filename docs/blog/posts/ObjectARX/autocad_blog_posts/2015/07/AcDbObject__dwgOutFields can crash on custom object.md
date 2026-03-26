---
title: "AcDbObject::dwgOutFields can crash on custom object"
date: 2015-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
description: "When implementing a custom object (derived from AcDbObject or AcDbEntity) the dwgOutFields method is required, otherwise AutoCAD will not save our ..."
author: Autodesk
---
# AcDbObject::dwgOutFields can crash on custom object

发布日期: 2015-07-01

原始链接: https://adndevblog.typepad.com/autocad/2015/07/acdbobjectdwgoutfields-can-crash-on-custom-object.html

## 文章内容

By Augusto Goncalves
When implementing a custom object (derived from AcDbObject or AcDbEntity) the dwgOutFields method is required, otherwise AutoCAD will not save our data. Usually the first step is call the base implementation, but that can crash. Why?
One reason is the safe check implemented to avoid null or erased AcDbDictionary referenced by the object, basically a isNull and isErased check.
Remember to configure and enable AutoCAD Debug Symbols on Visual Studio, that will help spot problems on internal calls.

