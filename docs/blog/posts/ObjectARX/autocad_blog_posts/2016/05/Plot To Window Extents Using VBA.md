---
title: "Plot To Window Extents Using VBA"
date: 2016-05-01
categories:
  - AutoCAD .NET
tags:
  - Plot
  - VBA
description: "I have received  a query from an ADN partner  that customer code to plot to window doesn’t plot and gives an empty print on certain drawings and sa..."
author: Autodesk
---
# Plot To Window Extents Using VBA

发布日期: 2016-05-01

原始链接: https://adndevblog.typepad.com/autocad/2016/05/plot-to-window-extents-using-vba.html

## 文章内容

By Madhukar Moogala
I have received  a query from an ADN partner  that customer code to plot to window doesn’t plot and gives an empty print on certain drawings and same code works well for rest of drawings.
The root cause of such weird behaviour is that the code doesn’t handle transformation of extent points from WCS to DCS, i.e. When user picks coordinate points from Editor as Window extents, these needs to transformed to DCS coordinate system for correct preview and plot of Drawings.
Important: Always make sure extents points needs to Transformed from WCS to DCS, this true for C++ & .NET API too.
  VBA code:
Public Sub Example_SetWindowToPlot()
        ' This example allows the user to define an area in the current layout
        ' and displays a plot preview of the defined area.
          AppActivate ThisDrawing.Application.Caption
          Dim point1 As Object, point2 As Object
          ' Get first point in window
        point1 = ThisDrawing.Utility.GetPoint(, "Click the lower-left of the window to plot.")
          ' Get second point in window
        point2 = ThisDrawing.Utility.GetPoint(, "Click the upper-right of the window to plot.")
              Dim point1DCS As Object, point2DCS As Object
          'Translate coordinates from WCS to DCS
          point1DCS = ThisDrawing.Utility.TranslateCoordinates(point1, acWorld, acDisplayDCS, False)
        point2DCS = ThisDrawing.Utility.TranslateCoordinates(point2, acWorld, acDisplayDCS, False)
          ReDim Preserve point1DCS(0 To 1)   ' Change this to a 2D array by removing the Z position
        ReDim Preserve point2DCS(0 To 1)   ' Change this to a 2D array by removing the Z position
          ' Send information about window to current layout
        ThisDrawing.ActiveLayout.SetWindowToPlot(point1DCS, point2DCS)
          ' Read back window information
        ThisDrawing.ActiveLayout.GetWindowToPlot(point1DCS, point2DCS)
          MsgBox "Press any key to plot the following window:" & vbCrLf & vbCrLf & _
               "Lower Left: " & point1(0) & ", " & point1(1) & vbCrLf & _
               "Upper Right: " & point2(0) & ", " & point2(1)
          ' Be sure to plot a view, not some other plot style
        ThisDrawing.ActiveLayout.PlotType = acWindow
          ' Send Plot To Window
        ThisDrawing.ActiveLayout.ConfigName = "DWG to PDF.pc3"
        ThisDrawing.Plot.DisplayPlotPreview acFullPreview
      End Sub

## 评论

**内容**: Zouhair said...
Can we have an exemple demonstrating printing window from model tab not layout
Reply
01/05/2021 at 08:10 AM

---
