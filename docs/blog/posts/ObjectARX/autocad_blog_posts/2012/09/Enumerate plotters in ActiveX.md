---
title: "Enumerate plotters in ActiveX"
date: 2012-09-01
categories:
  - AutoCAD VBA
tags:
  - COM
  - Plot
  - VBA
description: "The following VBA function enumerates all plotters that have corresponding .pc3 files, you can use this in your VBA applications:"
author: Autodesk
---
# Enumerate plotters in ActiveX

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/enumerate-plotters-in-activex.html

## 文章内容

By Xiaodong Liang
The following VBA function enumerates all plotters that have corresponding .pc3 files, you can use this in your VBA applications:
Public Function GetPlotters() As Collection
Set GetPlotters = New Collection
Dim strPlotter As String
strPlotter = Dir(Application.Preferences.Files.PrinterConfigPath + "\*.pc3")
While Not strPlotter = ""
   GetPlotters.Add strPlotter
   strPlotter = Dir
   MsgBox strPlotter
Wend
End Function
A method to enumerate system printers (these are also available in the plot dialog of AutoCAD) is available on the following Microsoft knowledge base article:
http://support.microsoft.com/kb/166008

