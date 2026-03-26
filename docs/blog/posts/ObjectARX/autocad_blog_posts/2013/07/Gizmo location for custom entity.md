---
title: "Gizmo location for custom entity"
date: 2013-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Selection
description: "Gizmo earlier called "grip tools" get displayed at the geometric center of the selection set if the "GTLOCATION" system variable is set to 1. AutoC..."
author: Autodesk
---
# Gizmo location for custom entity

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/gizmo-location-for-custom-entity.html

## 文章内容

By Balaji Ramamoorthy
Gizmo earlier called "grip tools" get displayed at the geometric center of the selection set if the "GTLOCATION" system variable is set to 1. AutoCAD gathers the extents of all the selected entities and determines the geometric center of the combined extents. To have the gizmo correctly located for a custom entity, it is needed to override the "subGetGeomExtents" method and provide the extents.

## 评论

**内容**: waseef said...
Hi,
Could any one provide a sample code .net to get the object center
Thanks & Regards
Reply
02/19/2017 at 11:20 PM

---
