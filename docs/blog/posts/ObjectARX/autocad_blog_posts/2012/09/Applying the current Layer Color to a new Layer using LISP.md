---
title: "Applying the current Layer Color to a new Layer using LISP"
date: 2012-09-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Layer
description: "To apply the current Layer’s colour to a newly created Layer using LISP can be done very simply like this:"
author: Autodesk
---
# Applying the current Layer Color to a new Layer using LISP

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/applying-the-current-layer-color-to-a-new-layer-using-lisp.html

## 文章内容

by Fenton Webb
To apply the current Layer’s colour to a newly created Layer using LISP can be done very simply like this:
; get the current layer name
(setq currentLayer (getvar "CLAYER"))
; get the ename of the current layer from the Layer table
(setq currentLayerEname (tblobjname "LAYER" currentLayer))
; extract the group code 62 (colour) from the ename using entget
(setq currentLayerColour (cdr (assoc 62 (entget currentLayerEname))))
; finally create the new layer using (command "LAYER")
(command "_.-LAYER" "_N" "TEST2" "_C" currentLayerColour "TEST2" "")

