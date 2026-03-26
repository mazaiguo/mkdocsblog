---
title: "Get plotters by LISP"
date: 2012-08-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
  - Plot
description: "In order to retrieve the list of configured plotters, you need"
author: Autodesk
---
# Get plotters by LISP

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/get-plotters-by-lisp.html

## 文章内容

By Xiaodong Liang
In order to retrieve the list of configured plotters, you need
to use the ActiveX Interface, which exposes a list of configured plotters. The best way to do this is to use the ActiveLayout Object's etPlotDeviceNames Property.
The following AutoLISP code demonstrates this:
(defun C:GetPlotters (/ acadObject acadDocument activeLayoutObject plotter
PlotterNames)
 (vl-load-com)
 (setq acadObject (vlax-get-Acad-object))
 (setq acadDocument (vla-get-ActiveDocument acadObject))
 (setq activeLayoutObject (vla-Get-ActiveLayout acadDocument))
 (vla-RefreshPlotDeviceInfo activeLayoutObject)
 (setq PlotterNames (vla-GetPlotDeviceNames activeLayoutObject))
 (vl-princ-to-string (setq plotters (vlax-safearray->list (vlax-variant-value
PlotterNames))))
 (setq i 0)
 (mapcar '(lambda (x) (princ (strcat "\nPlotter No: " (itoa i) " - Device: "
x)) (setq i (1+ i))) plotters)
 (princ)
)

