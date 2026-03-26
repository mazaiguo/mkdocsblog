---
title: "Deleting the contents of an AcDbVoidPtrArray used for creating hatch"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Hatch
description: "When I use the AcDbHatch::appendLoop function that takes an AcDbVoidPtrArray of AcGeCurve objects, AutoCAD terminates unexpectedly when the memory ..."
author: Autodesk
---
# Deleting the contents of an AcDbVoidPtrArray used for creating hatch

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/deleting-the-contents-of-an-acdbvoidptrarray-used-for-creating-hatch.html

## 文章内容

By Xiaodong Liang
Issue
When I use the AcDbHatch::appendLoop function that takes an AcDbVoidPtrArray of AcGeCurve objects, AutoCAD terminates unexpectedly when the memory is erased. Do I need to delete the elements of the array?
Solution
The existing documentation does not explicitly mention that once the loop definition array is passed over to AutoCAD, it is then kept internally to store the loop information inside the hatch.
The contents of AcDbVoidPtrArray in this case, should NOT be deleted.

