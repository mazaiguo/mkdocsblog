---
title: "Quick tip: Getting extended entity data from an xref'ed drawing"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - DWG
  - XREF
description: "An xref'ed DWG file is like an INSERT for AutoCAD. This means that AutoCAD loads the xref'ed DWG file into a AcDbBlockTableRecord (block definition..."
author: Autodesk
---
# Quick tip: Getting extended entity data from an xref'ed drawing

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/quick-tip-getting-extended-entity-data-from-an-xrefed-drawing.html

## 文章内容

By Gopinath Taget
An xref'ed DWG file is like an INSERT for AutoCAD. This means that AutoCAD loads the xref'ed DWG file into a AcDbBlockTableRecord (block definition) in the current drawing. Therefore, if XDATA was attached to a line in the XREF drawing
file, a copy of that line (with XDATA) is present in the block definition. In this case, iterate the block definition to retrieve the XDATA information.

