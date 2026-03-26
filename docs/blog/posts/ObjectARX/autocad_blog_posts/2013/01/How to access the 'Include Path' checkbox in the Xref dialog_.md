---
title: "How to access the 'Include Path' checkbox in the Xref dialog?"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - ObjectARX
  - XREF
description: "There is no variable or user setting that allows access to this checkbox other than what is provided with the XREF command. However, the code behin..."
author: Autodesk
---
# How to access the 'Include Path' checkbox in the Xref dialog?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-access-the-include-path-checkbox-in-the-xref-dialog.html

## 文章内容

By Gopinath Taget
There is no variable or user setting that allows access to this checkbox other than what is provided with the XREF command. However, the code behind this is able to set the path of the xref directly.
For example, the ObjectARX method AcDbBlockTableRecord::setPathName() will do this. You can also use AcDbBlockTableRecord::pathName() to check on the current path setting for a given xref.

