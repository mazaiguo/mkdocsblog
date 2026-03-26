---
title: "Use an Open LW Polyline as the Boundary for a Hatch in VBA"
date: 2012-12-01
categories:
  - AutoCAD VBA
tags:
  - Hatch
  - Plugin
  - Polyline
  - VBA
description: "How can I use a lightweight polyline that is open to define the boundary for a"
author: Autodesk
---
# Use an Open LW Polyline as the Boundary for a Hatch in VBA

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/use-an-open-lw-polyline-as-the-boundary-for-a-hatch-in-vba.html

## 文章内容

by Fenton Webb
Issue
How can I use a lightweight polyline that is open to define the boundary for a
new hatch entity? Can I also use the AddVertex method for adding vertexes to the
lightweight polyline?
Solution
The following code contains a function that creates a lightweight polyline
(using AddVertex) that is left "open" (although its start and end points
coincide). This polyline is then used in the outerloop of the hatch entity
created below.
Option Base 0
Sub TestLWPline ()       
   'build the initial array for two points        
   Dim Pt(0 To 3) As Double        
   Pt(0) = 0#: Pt(1) = 0#: Pt(2) = 0#: Pt(3) = 10#        
   'create a lwpline based on the two points        
   Dim LWpline As Object        
   Set LWpline = ThisDrawing.ModelSpace.AddLightWeightPolyline(Pt)        
   'add further points        
   Pt(0) = 10#: Pt(1) = 10#        
   LWpline.AddVertex 2, Pt        
   'add a the start point to lwpline again so        
   'that the start and end points coincide but its Closed        
   'property is false        
   Pt(0) = 0#: Pt(1) = 0#        
   LWpline.AddVertex 3, Pt        
   'you can check here if it is really false        
   Dim bClosed As Boolean        
   bClosed = LWpline.closed        
   'add a hatch to modelspace        
   Dim MyHatch As Object        
   Set MyHatch = ThisDrawing.ModelSpace.AddHatch
(acHatchPatternTypePreDefined,"ANSI31", True)       
   'create and append outer loop        
   Dim outerLoop As Variant
   Dim outerLoopArray(0) As Object       
   Set outerLoopArray(0) = LWpline
   outerLoop = outerLoopArray       
   MyHatch.AppendOuterLoop (outerLoop)
End Sub

