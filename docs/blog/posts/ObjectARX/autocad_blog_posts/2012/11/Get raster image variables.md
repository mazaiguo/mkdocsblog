---
title: "Get raster image variables"
date: 2012-11-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
description: "Is it possible to access, from AutoLISP, the raster image variables IMAGEFRAME and IMAGEQUALITY? It seems there are no 'real' AutoCAD variables and..."
author: Autodesk
---
# Get raster image variables

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/get-raster-image-variables.html

## 文章内容

By Augusto Goncalves
Is it possible to access, from AutoLISP, the raster image variables IMAGEFRAME and IMAGEQUALITY? It seems there are no 'real' AutoCAD variables and that I am not able to access them via (getvar) and (setvar).
The ImageEngine stores these variables in an AutoCAD dictionary. The dictionary has the name "ACAD_IMAGE_VARS". To access this dictionary, you have to get the named object dictionary with (namedobjdict).
The following function gets the "ACAD_IMAGE_VARS" dictionary:
(defun GetImageVarsDict () 
  (setq dict (dictsearch (namedobjdict) "ACAD_IMAGE_VARS")) 
)
Group code 70 contains the value of IMAGEFRAME. If it is '0', the frames are off, if it is '1', the frames are on. Group code 71 contains the value of IMAGEQUALITY. If it is '0', the quality is <draft>, if it is '1', the quality is <high>.
To get the current settings, you can use the following:
(defun GetImageFrame () 
  (setq frames (cdr (assoc 70 (GetImageVarsDict)))) 
)

(defun GetImageQuality () 
  (setq quality (cdr (assoc 71 (GetImageVarsDict)))) 
)

To change the settings, use the following code:
(defun SetImageFrame (flag) 
  (entmod (subst (cons 70 flag)
  (assoc 70 (GetImageVarsDict)) (GetImageVarsDict))) 
  (princ) 
)

(defun SetImageQuality (flag) 
  (entmod (subst (cons 71 flag)
  (assoc 71 (GetImageVarsDict)) (GetImageVarsDict))) 
  (princ) 
)
NOTE: You have to update the AutoCAD display list if you change IMAGEFRAME. You can do this with a REGEN, or you can select all images with (ssget) and update the single raster images with (entupd).

