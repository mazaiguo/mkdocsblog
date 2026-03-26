---
title: "get current UCS in a DBX enabler"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - Dimension
  - UCS
  - Unicode
description: "How do I get the current UCS from within an ObjectDBX enabler and don't have access to acedGetCurrentUcs()?"
author: Autodesk
---
# get current UCS in a DBX enabler

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/get-current-ucs-in-a-dbx-enabler.html

## 文章内容

Issue
How do I get the current UCS from within an ObjectDBX enabler and don't have access to acedGetCurrentUcs()?
Solution
The global function acdbUcsMatrix() returns a matrix identical to acedGetCurrentUcs(). It can normally be used in place of acedGetCurrentUcs() and is available in ObjectDBX.
There are some posts which have lines of acdbUcsMatrix, e.g.
Set oblique angle of aligned dimensions to a certain angle relative to an axis in the current UC
Ordinate Dimension Text is incorrect in rotated UCS

