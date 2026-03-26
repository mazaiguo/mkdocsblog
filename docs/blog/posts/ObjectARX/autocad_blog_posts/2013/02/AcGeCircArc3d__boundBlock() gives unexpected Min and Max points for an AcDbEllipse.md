---
title: "AcGeCircArc3d::boundBlock() gives unexpected Min and Max points for an AcDbEllipse"
date: 2013-02-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Block
  - Dimension
description: "Using AcGeCircArc3d (or CircularArc3d in .NET) to generate a curve, I find that the boundBlock() returns strange results."
author: Autodesk
---
# AcGeCircArc3d::boundBlock() gives unexpected Min and Max points for an AcDbEllipse

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/acgecircarc3dboundblock-gives-unexpected-min-and-max-points-for-an-acdbellipse.html

## 文章内容

By Fenton Webb
Issue
Using AcGeCircArc3d (or CircularArc3d in .NET) to generate a curve, I find that the boundBlock() returns strange results.
Solution
boundBlock() does not necessarily return a bounding box whose sides are parallel to the entity coordinate system (ECS). In fact for ellipses, it returns a bounding box whose edges are parallel to the ellipse major and minor axes... all other bounding boxes are generated parallel to the ECS... orthoBoundBlock(), on the other hand, returns points of a bounding box whose edges are parallel to the ECS - so use orthoBoundBlock() instead.

