---
title: "What is the right way to an osnap point in snapPoints array in getOsnapInfo (custom osnap mode) for a block reference?"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Block
  - Dimension
  - Plugin
description: "What is the coordinate system of point passed into snapPoints array in getOsnapInfo() for a block reference. Should it be in WCS?"
author: Autodesk
---
# What is the right way to an osnap point in snapPoints array in getOsnapInfo (custom osnap mode) for a block reference?

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/what-is-the-right-way-to-an-osnap-point-in-snappoints-array-in-getosnapinfo-custom-osnap-mode-for-a-block-reference.html

## 文章内容

By Philippe Leefsma
Q:
What is the coordinate system of point passed into snapPoints array in getOsnapInfo() for a block reference. Should it be in WCS?
A:
In the case of block references, you would need to transform a given point to the coordinate system of the block's plane before adding it to snapPoints array. AutoCAD would take that point and re-map it to WCS. Here is an example:
if(pickedObject->isA() !=  AcDbBlockReference::desc() )
   return Acad::eOk;
 
  AcDbBlockReference *pBlRef = AcDbBlockReference::cast(pickedObject);
  AcGePoint3d position(1,1,1);
  AcGeVector3d nor = pBlRef->normal();
  position.transformBy(AcGeMatrix3d::worldToPlane(nor));
  snapPoints.append(position);

