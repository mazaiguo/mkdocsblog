---
title: "Use system variables to get lower left and upper right coordinates of the model space viewport"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Dimension
  - UCS
description: "You can use the system variables VIEWCTR, VIEWSIZE and SCREENSIZE to calculate the lower left and upper right coordinates of the current viewport i..."
author: Autodesk
---
# Use system variables to get lower left and upper right coordinates of the model space viewport

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/use-system-variables-to-get-lower-left-and-upper-right-coordinates-of-the-model-space-viewport.html

## 文章内容

By Gopinath Taget
You can use the system variables VIEWCTR, VIEWSIZE and SCREENSIZE to calculate the lower left and upper right coordinates of the current viewport in the ModelSpace . The VIEWCTR system variable has the view center coordinates reported in current UCS. So steps to follow to get the required coordinates are:
1) Get the VIEWCENTER in current UCS and transform the point to DCS (Display Coordinate System)
2) Get the VIEWSIZE, which is the height of the view.
3) Get the screen aspect ratio using SCREENSIZE system variable. Using the value returned by SCREENSIZE, get the screen width and screen height. SCREENSIZE returns a list of two reals, first one is the screen width and second one is screen height.
4) Calculate the width of the view using the formula: width = height * (screenwidth/screenheight)
5) Calculate the lower left corner as:
LL(x) = center(x) - (width / 2)
LL(y) = center(y) - (height / 2)
6) Calculate the Upper right corner as:
UR(x) = center(x) + (width / 2)
UR(y) = center(y) + (height / 2)
7) Transform the LL and UR coordinates from DCS to WCS. Note that this will return the points that lie in the DCS XY plane, reported in WCS.
The following code shows how to do this using the ActiveX API in VB/A.  It also draws a line joining both the points.
Private Sub fViewExtents()
  Dim pdHeight As Double
  Dim pdWidth As Double
  Dim pvCtr As Variant
  Dim pvScreenSize As Variant
  Dim pdMin(2) As Double
  Dim pdMax(2) As Double
    'Center Point of the View
  pvCtr = ThisDrawing.GetVariable("VIEWCTR")
  pvCtr = ThisDrawing.Utility.TranslateCoordinates(
    pvCtr, acUCS, acDisplayDCS, 0)
    'Screen resolution
  pvScreenSize = ThisDrawing.GetVariable("SCREENSIZE")
    'Screen Height
  pdHeight = ThisDrawing.GetVariable("VIEWSIZE")
    'Screen Length
  pdWidth = pdHeight * (pvScreenSize(0) / pvScreenSize(1))
    'lower left
  pdMin(0) = pvCtr(0) - (pdWidth / 2)
  pdMin(1) = pvCtr(1) - (pdHeight / 2)
    'upper right
  pdMax(0) = pvCtr(0) + (pdWidth / 2)
  pdMax(1) = pvCtr(1) + (pdHeight / 2)
    'draw the line
  ThisDrawing.ModelSpace.AddLine ThisDrawing.Utility.
    TranslateCoordinates(pdMin, acDisplayDCS, acUCS, 0), _
  ThisDrawing.Utility.TranslateCoordinates(
    pdMax, acDisplayDCS, acWorld, 0)
  End Sub

