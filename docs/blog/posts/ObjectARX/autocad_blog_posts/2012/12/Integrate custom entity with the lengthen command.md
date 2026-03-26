---
title: "Integrate custom entity with the lengthen command"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Polyline
description: "The LENGTHEN command can only work with the following classes, or any custom classes derived from them:"
author: Autodesk
---
# Integrate custom entity with the lengthen command

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/integrate-custom-entity-with-the-lengthen-command.html

## 文章内容

By Augusto Goncalves
The LENGTHEN command can only work with the following classes, or any custom classes derived from them:
AcDbLine
AcDbArc
AcDbCircle
AcDb2dPolyline
AcDb3dPolyline
AcDbEllipse
AcDbSpline
AcDbPolyline
If the custom entity is derived from any of these, LENGTHEN will automatically work, but if not, unfortunately there is nothing we can do to implement the command.

