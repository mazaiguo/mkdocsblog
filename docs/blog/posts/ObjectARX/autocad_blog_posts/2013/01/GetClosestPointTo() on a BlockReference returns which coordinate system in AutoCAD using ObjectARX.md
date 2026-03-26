---
title: "GetClosestPointTo() on a BlockReference returns which coordinate system in AutoCAD using ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - Block
  - C++
  - Dimension
  - ObjectARX
description: "Why are the coordinates of a closest point (using GetClosestPointTo()) obtained from a block reference relative to neither WCS nor UCS?."
author: Autodesk
---
# GetClosestPointTo() on a BlockReference returns which coordinate system in AutoCAD using ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/getclosestpointto-on-a-blockreference-returns-which-coordinate-system-in-autocad-using-objectarx.html

## 文章内容

By Fenton Webb
Issue
Why are the coordinates of a closest point (using GetClosestPointTo()) obtained from a block reference relative to neither WCS nor UCS?.
Solution
The points that you receive are relative to the coordinate system of the owning
AcDbBlockTableRecord. If you want to convert them to coordinate system of the
AcDbBlockTableRecord in which you have the AcDbBlockReference, you must
transform them by the AcDbBlockReference::blockTransform().
You probably first want to transform the "specified point" by the inverse of
AcDbBlockReference::blockTransform(), do the closest point calculation, then
convert the resulting point back to the original space.

