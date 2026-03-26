---
title: "Setting configname for a layout generates an error"
date: 2013-01-01
categories:
  - AutoCAD VBA
tags:
  - Plot
  - VBA
description: "Why do I get an error when I try to set the ConfigName of a Layout?"
author: Autodesk
---
# Setting configname for a layout generates an error

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/setting-configname-for-a-layout-generates-an-error.html

## 文章内容

By Daniel Du
Issue
Why do I get an error when I try to set the ConfigName of a Layout?
Solution
The usual reason for this error is that you are not calling 'RefreshPlotDeviceInfo' before assigning a 'ConfigName'.
Here is an example of some VBA code that does work:
Sub Test()
Dim Layouts As AcadLayouts
Dim Layout As AcadLayout

' Get the files preferences object
Set Layouts = ThisDrawing.Layouts

' Change plotter configuration file
Layouts("Model").RefreshPlotDeviceInfo
Layouts("Model").ConfigName = "PrinterName"

ThisDrawing.Plot.PlotToDevice
End Sub
If you comment out the line 'Layout("Model").RefreshPlotDeviceInfo', the routine will work sometimes, but not always.
Please note that you will still generate an error if you try to set a ConfigName that AutoCAD cannot find.

