---
title: "Making non-database resident objects work with undo"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - DWG
  - Database
description: "Non-database resident objects do not participate in an Undo/Redo. However, it is fairly easy to take advantage of the built-in Undo/Redo feature wi..."
author: Autodesk
---
# Making non-database resident objects work with undo

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/making-non-database-resident-objects-work-with-undo.html

## 文章内容

By Gopinath Taget
Non-database resident objects do not participate in an Undo/Redo. However, it is fairly easy to take advantage of the built-in Undo/Redo feature with the following procedure:
1. Derive your objects from AcDbObject as if you were creating a custom database-resident object. (You will only need to override the dwgInFields/dwgOutFields methods.)
2. Append the objects to the database using AcDbDatabase::addAcDbObject
The addAcDbObject function appends the object to the database but does not set up an owner for the object so it will not be saved when the database is saved.
You will need to use proper open/close protocol on this object to ensure undo/redo works as expected.

