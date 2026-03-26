---
title: "How to implement intersectWith with arcs and circle?"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "When you implement my custom entity, the function intersectWith is called when the user enters the TRIM command. Although you implement custom enti..."
author: Autodesk
---
# How to implement intersectWith with arcs and circle?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-implement-intersectwith-with-arcs-and-circle.html

## 文章内容

By Gopinath Taget
When you implement my custom entity, the function intersectWith is called when the user enters the TRIM command. Although you implement custom entity such that it can handle arcs and circles, you will find that the intersectWith function of the custom entity is passed an entity for which isKindOf( AcDbArc::desc() ) and isKindOf(AcDbCircle::desc()) are both False when the arcs and circles are selected. So how can you provide special handling for circles and arcs?
For arcs and circles, the entity passed is actually an AcDbEllipse, which allows functions that handle all elliptical objects generically. If you can handle circles and arcs in a specific way ( not as general ellipses ) then extract their defining data ( such as center, normal, start and end points ) and implement the intersections.

