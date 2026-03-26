---
title: "Explode Text Entity"
date: 2012-10-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Unicode
description: "How to explode SHX based AcDbText entities to its constituent lines?"
author: Autodesk
---
# Explode Text Entity

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/explode-text-entity.html

## 文章内容

By Philippe Leefsma
Q:
How to explode SHX based AcDbText entities to its constituent lines?
A:
You can “explode” or tessellate the text entity using the AcGiTextEngine::tessellate() method. But the method returns raw point information which can be used to create individual lines. The method does not honor the text style table properties and the text height, width are assumed to be of one unit.
To get the exact representation of an AcDbText entity, we need to transform this raw point information depending upon the attributes of the text and its text style. In the attached sample, the function fGeneratematrix() creates a transformation matrix which will place the lines drawn using the points exactly at the text location. This transformation matrix will take care of oblique angle, upside down, backward text properties.
NOTE: the true type fonts are not supported.
_ArxTesselateText.zip

