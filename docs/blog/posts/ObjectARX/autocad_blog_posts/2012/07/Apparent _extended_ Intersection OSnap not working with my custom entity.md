---
title: "Apparent *extended* Intersection OSnap not working with my custom entity"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Polyline
description: "My custom entity explodes itself into AcDbPolylines in the intersectWith() functions, I then call the intersectWith() on each of these AcDbPolyline..."
author: Autodesk
---
# Apparent *extended* Intersection OSnap not working with my custom entity

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/apparent-extended-intersection-osnap-not-working-with-my-custom-entity.html

## 文章内容

By Philippe Leefsma
Q:
My custom entity explodes itself into AcDbPolylines in the intersectWith() functions, I then call the intersectWith() on each of these AcDbPolylines. The problem is that AppInt (apparerent *extended* Intersection) doesn't work... Why?
A:
This should work fine, as long as the AcDbPolyline that you custom entity explodes into isn't *Closed*... If it is then the Apparent *extended* Intersect OSnap will not work with it...
The solution is to explode the AcDbPolyline once more into normal AcDbLines.

