---
title: "Non-ActiveX property get and set functions"
date: 2012-08-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - COM
  - Plot
  - Polyline
  - Unicode
description: "These were introduced in AutoCAD 2012 and you can find explanations in the AutoCAD documentation as well as in Lee' blog and Jimmy's blog. Recently..."
author: Autodesk
---
# Non-ActiveX property get and set functions

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/non-activex-property-get-and-set-functions.html

## 文章内容

By Balaji Ramamoorthy
These were introduced in AutoCAD 2012 and you can find explanations in the AutoCAD documentation as well as in Lee' blog and Jimmy's blog. Recently, I was asked by a developer to provide an explanation for the optional parameter marked as "[or collectionName index name val]" in the documentation.
To understand this parameter, you may try using the “dumpallproperties” on a polyline. The vertices of a polyline is a collection and each vertex has a set of properties that can be retrieved / set. In this context, the optional parameters are useful.
Try this in the AutoCAD command line :
 (command "_pline" "0,0" "3,3" "5,2" "")
(setq e1 (entlast))
(dumpallproperties e1)
From what gets printed in the AutoCAD command window, we now have the name of the collection and the property names of each item in the collection. These can be used to either set / get the property as follows :
; Modify the EndWidth of a Vertex to 1.0
(setpropertyvalue e1 "Vertices" 0 "EndWidth" 1.0)
; Get the "EndWidth" of the first vertex.
(getpropertyvalue e1 "Vertices" 0 "EndWidth")
; Get the "EndWidth" of the second vertex. 
(getpropertyvalue e1 "Vertices" 1 "EndWidth")
; Get the X coordinate of the third vertex.
(getpropertyvalue e1 "Vertices" 2 "Point/X")
; Get the Y coordinate of the third vertex.
(getpropertyvalue e1 "Vertices" 2 "Point/Y")

