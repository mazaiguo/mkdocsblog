---
title: "Obtaining the Nominal Diameter as a string distance in Plant3d"
date: 2013-02-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - Plant 3D
description: "Obtaining the Nominal Diameter as a string in Plant3d is done using NominalDiameterMap.csv Excel file found in Program Files\AutoCAD Plant3d 2013 f..."
author: Autodesk
---
# Obtaining the Nominal Diameter as a string distance in Plant3d

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/obtaining-the-nominal-diameter-as-a-string-distance-in-plant3d.html

## 文章内容

by Fenton Webb
Obtaining the Nominal Diameter as a string in Plant3d is done using NominalDiameterMap.csv Excel file found in Program Files\AutoCAD Plant3d 2013 folder. This spreadsheet mainly sets up a logical conversion map between imperial and metric sizes, because the math conversions are not always aligned to the required size strings.
Plant already has this map loaded, you can access it via:
NominalDiameterMap DefaultMap;
You can convert the Nominal Diameter value to a string using this code:
NominalDiameter d = new NominalDiameter(0.125);
string nddDisplay = d.ToDisplayString(null);

