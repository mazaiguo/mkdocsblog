---
title: "Boundary and bhatch on custom entities"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Hatch
  - Polyline
description: "Lets say, you have created a custom entity based on a polyline, but derived from a AcDbEntity, and wish to change the way BHATCH and BOUNDARY find ..."
author: Autodesk
---
# Boundary and bhatch on custom entities

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/boundary-and-bhatch-on-custom-entities.html

## 文章内容

By Gopinath Taget
Lets say, you have created a custom entity based on a polyline, but derived from a AcDbEntity, and wish to change the way BHATCH and BOUNDARY find the edges of my object.
You can do this by overriding the AcDbEntity::explode() virtual method to return the boundaries you want used by the BOUNDARY or BHATCH commands. You would check the CMDNAMES system variable, to see whether one of the two commands was active, and then return the appropriate entities. Note that if you derive from AcDbPolyline, it will not call explode on your entity, but will use
the Polyline data directly.

