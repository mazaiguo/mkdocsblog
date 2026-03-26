---
title: "AcDbDictionary is marked as ePermanentlyErased"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - DWG
description: "I have a drawing containing custom objects that I have saved. When I reopen the drawing and try to access some of the dictionaries within the drawi..."
author: Autodesk
---
# AcDbDictionary is marked as ePermanentlyErased

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/acdbdictionary-is-marked-as-epermanentlyerased.html

## 文章内容

By Xiaodong Liang
Issue
I have a drawing containing custom objects that I have saved. When I reopen the drawing and try to access some of the dictionaries within the drawing, I find that they have been marked as ePermanentlyErased. Why?
Solution
This problem usually manifests itself when custom objects do not save themselves correctly. You should review their dwgInFields and dwgOutFields methods to make sure that they are correctly implemented. In addition, when you read/write specific type of data, it is recommended to use the type-specific methods such as writeInt32, readInt32.

