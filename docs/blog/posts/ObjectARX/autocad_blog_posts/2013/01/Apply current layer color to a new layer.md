---
title: "Apply current layer color to a new layer"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Layer
description: "Using Lisp, is there a way that I can get the current color from the current layer?   I want to apply the color from the current layer to a new lay..."
author: Autodesk
---
# Apply current layer color to a new layer

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/apply-current-layer-color-to-a-new-layer.html

## 文章内容

By Xiaodong Liang
  Issue
Using Lisp, is there a way that I can get the current color from the current layer?   I want to apply the color from the current layer to a new layer, with no user input.  For example:
(SETQ OLDLAYER (GETVAR "CLAYER")) ;Gets the current layer TEST1 

(COMMAND "LAYER" "N" TEST2 "C" )

Solution
The following Lisp code should accomplish what you want:
(setq OLDLAYER (getvar "CLAYER")) ;Gets the current layer TEST1
;Gets the ENAME of the current layer TEST1
(setq OLDLAYERENT (tblobjname "LAYER" OLDLAYER))
 
;Gets the color of the current layer TEST1
(setq OLDCOLOR (cdr (assoc 62 (entget OLDLAYERENT))))
 
;Creates new layer TEST2 and assigns OLDCOLOR to it
(command "LAYER" "N" "TEST2" "C" OLDCOLOR "TEST2" "")

