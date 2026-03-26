---
title: "Using AutoLISP to get scale of an image"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
description: "The scale is calculated from two other values: the width of an image pixel (in AutoCAD units) and the width of the image. This gives the actual wid..."
author: Autodesk
---
# Using AutoLISP to get scale of an image

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/using-autolisp-to-get-scale-of-an-image.html

## 文章内容

By Gopinath Taget
The scale is calculated from two other values: the width of an image pixel (in AutoCAD units) and the width of the image. This gives the actual width, which is the scale. Look at the entity data for an image.
Command: (entget (car (entsel)))

Select object: ((-1 . <Entity name: 27e0540>) (0 . "IMAGE") (5 . "50") (100 . "AcDbEntity") (67 . 0) (8 . "0") (100 . "AcDbRasterImage") (90 . 0) (10 3.81393 1.89337 0.0) (11 0.0102131 0.0 0.0) (12 6.25353e-019 0.0102131 0.0) (13 500.0
333.0) (340 . <Entity name: 27e0530>) (70 . 7) (280 . 0) (281 . 50) (282 . 50) (283 . 0) (360 . <Entity name: 27e0538>) (71 . 1) (91 . 2) (14 -0.5 -0.5) (14 499.5 332.5))
For a simple example, multiply the first value of code 11 (0.0102131) by the first value of code 13 (500.0) to get the scale factor which in this case is 5.10655, the inserted scale factor.
Here's some lisp code that demonstrates how to do this:
(defun C:RAS_SCALE()
(setq le (entget (car (entsel "\nSelect Raster Object: "))))
(if le
(if (= (cdr (assoc '0 le)) "IMAGE")
(progn (setq uv (distance '(0.0 0.0 0.0) (cdr (assoc '11 le))))
(setq pix (nth 1 (assoc '13 le)))
(princ (strcat "\nImage Scale: " (rtos (* uv pix) 2 5)))
)
)
)
(princ))
  Note that you should base your calculations on the following information from the Customization Guide for the version of AutoCAD in use.
The following group codes apply to image entities.
Image group codes
Group codes Description
11 U-vector of a single pixel  (points along the visual bottom of the image, 
starting at the insertion point)  (in OCS). DXF: X value; APP: 3D point
13  Image size in pixels. DXF: U value; APP: 2D point (U and V values)
The AutoLISP code has been coded to account for a rotated image.

