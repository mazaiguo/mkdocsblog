---
title: "DxfOut throws eInvalidDwgVersion when trying to save to R14 format"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - DXF
  - Database
description: "I'm using Database.DxfOut() to save a file and it works fine except when trying to save to R14 format. Then it throws eInvalidDwgVersion exception...."
author: Autodesk
---
# DxfOut throws eInvalidDwgVersion when trying to save to R14 format

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/dxfout-throws-einvaliddwgversion-when-trying-to-save-to-r14-format.html

## 文章内容

By Adam Nagy
I'm using Database.DxfOut() to save a file and it works fine except when trying to save to R14 format. Then it throws eInvalidDwgVersion exception. Why?
Solution
The reason is that saving to R14 DXF format has not been supported since AutoCAD 2006. But you can save to other DXF formats all the way back to R12.

