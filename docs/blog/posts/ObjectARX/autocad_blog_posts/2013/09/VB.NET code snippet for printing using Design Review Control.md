---
title: "VB.NET code snippet for printing using Design Review Control"
date: 2013-09-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Plot
description: "If you are wondering how you could use the Autodesk Design Review control to print a DWF file in a .NET App, here is a code snippet that will help:"
author: Autodesk
---
# VB.NET code snippet for printing using Design Review Control

发布日期: 2013-09-01

原始链接: https://adndevblog.typepad.com/autocad/2013/09/vbnet-code-snippet-for-printing-using-design-review-control.html

## 文章内容

By Gopinath Taget
If you are wondering how you could use the Autodesk Design Review control to print a DWF file in a .NET App, here is a code snippet that will help:
Private Sub SimplePrintButton_Click(
ByVal sender As System.Object,
ByVal e As System.EventArgs) Handles SimplePrintButton.Click
        Dim ctrl As ExpressViewerDll.CExpressViewerControl
        ctrl = AxCExpressViewerControl1.GetOcx()
        Dim plt As EPlotViewer.IAdEPlotViewer
        plt = ctrl.DocumentHandler
        plt.SimplePrint(True, True)
End Sub
Please do make sure you have the “DwfComposer EplotViewer 1.0 Type Library” COM library referenced in your application.

