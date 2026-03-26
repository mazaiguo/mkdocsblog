---
title: "Drawing AcDbWipeout in custom entity worldDraw"
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
  - Plugin
description: "As “AcDbWipeout” uses “AcGiViewportGeometry::rasterImageDc” to draw itself, it is not possible to draw an in memory “AcDbWipeout”. The workaround f..."
author: Autodesk
---
# Drawing AcDbWipeout in custom entity worldDraw

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/drawing-acdbwipeout-in-custom-entity-worlddraw.html

## 文章内容

By Virupaksha Aithal
As “AcDbWipeout” uses “AcGiViewportGeometry::rasterImageDc” to draw itself, it is not possible to draw an in memory “AcDbWipeout”. The workaround for this limitation is to make “AcDbWipeout” object a database resident (like adding to an Anonymous block) and using the database resident “AcDbWipeout” entity to draw inside the custom entity.  Refer attached demo sample

