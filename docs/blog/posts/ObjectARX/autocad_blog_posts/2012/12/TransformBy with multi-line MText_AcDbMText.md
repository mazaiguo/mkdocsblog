---
title: "TransformBy with multi-line MText/AcDbMText"
date: 2012-12-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - DXF
description: "Suppose a a MTEXT entity that has two lines of text: One line of text is formatted with the Arial font at point size 200 and the other line is form..."
author: Autodesk
---
# TransformBy with multi-line MText/AcDbMText

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/transformby-with-multi-line-mtextacdbmtext.html

## 文章内容

By Augusto Goncalves
Suppose a a MTEXT entity that has two lines of text: One line of text is formatted with the Arial font at point size 200 and the other line is formatted with text that uses the Arial font, text size 100. If I transform this entity with the ObjectARX or .NET function, transformBy, the first line is transformed, but the second line of text stays the same.
This is how AutoCAD is designed to work and is not a problem caused by the ObjectARX or .NET API's. To reproduce this behavior, use the "Scale" command in AutoCAD. Moreover: the same effect happens if you change the color or any other setting besides height of the Mtext.
The reason for this is that if you change the settings that were present when the Mtext was created, then any changes to the text settings that are made afterwards are stored as format codes inside the string used for storing the text of the MTEXT entity (DXF code 1).
As an example, suppose we have an entget list for an MTEXT object that contains two lines: the first one has Arial text that has 100 at its height, and and the second line contains Arial text that has 200 as its height:
Command: (entget (entlast))
((-1 . <Entity name: 3470550>) (0 . "MTEXT") (5 . "52") (100 . "AcDbEntity")
(67 . 0) (8 . "0") (100 . "AcDbMText") (10 -0.210389 6.2124 0.0) (40 . 100.0)
(41 . 4.7123) (71 . 1) (72 . 5) (1 . "test\\P\\H200;test") (7 . "STANDARD")
(210 0.0 0.0 1.0) (11 1.0 0.0 0.0) (42 . 734.915) (43 . 366.667) (50 . 0.0))
If you change the properties of this entity, then only the global properties will be changed (DXF code 400 for the text height), but the text string itself will not be changed. As a result, the second line will be displayed using Arial with a height of 200. This occurs regardless of whether you use an API or an AutoCAD command such AS DDEDIT, CHPROP, or SCALE.
Using the API you can work this around only parsing the content of the MTEXT entity and replacing manually the height formatting values. (This cannot be done in AutoCAD from the command line.)
An alternate solution is to use different MTEXT entities for text that has requires different formatting.

