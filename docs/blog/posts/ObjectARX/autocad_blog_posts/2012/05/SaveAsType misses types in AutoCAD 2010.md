---
title: "SaveAsType misses types in AutoCAD 2010"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - DWG
  - DXF
  - ObjectARX
description: "The AcSaveAsType enum missed the formats of 2010: ac2010dwg, ac2010dxf , ac2010Template."
author: Autodesk
---
# SaveAsType misses types in AutoCAD 2010

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/saveastype-misses-some-types-of-2010.html

## 文章内容

By Xiaodong Liang
The AcSaveAsType enum missed the formats of 2010: ac2010_dwg, ac2010_dxf , ac2010_Template.
This was fixed in SP1 of AutoCAD 2010. You can download it from
http://usa.autodesk.com/adsk/servlet/ps/dl/item?siteID=123112&id=13760520&linkID=9240618
Please note: SP1 does not update acax18ENU.tlb in ObjectARX package. So if you were using that one, please make sure to refer to the newest updated by SP1. You can find it under e.g.
"C:\Program Files\Common Files\Autodesk Shared\acax18enu.tlb"
From AutoCAD 2011, the three enum are available.

