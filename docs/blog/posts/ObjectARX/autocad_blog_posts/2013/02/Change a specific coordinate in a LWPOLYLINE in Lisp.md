---
title: "Change a specific coordinate in a LWPOLYLINE in Lisp"
date: 2013-02-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Dimension
  - Polyline
description: "The LWPOLYLINE (or light weight polyline) will typically have multiple coordinates and it is not easy to modify these vertices. What is the easiest..."
author: Autodesk
---
# Change a specific coordinate in a LWPOLYLINE in Lisp

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/change-a-specific-coordinate-in-a-lwpolyline-in-lisp.html

## 文章内容

By Gopinath Taget
The LWPOLYLINE (or light weight polyline) will typically have multiple coordinates and it is not easy to modify these vertices. What is the easiest way to access specific coordinates in a LWPOLYLINE and modify it?
The following lisp code demonstrates an easy way. The lisp code snippet increments the Y values of the LWPOLYLINE vertices by 5 units:
(defun Test (e ed / i vt)
(setq i 0)
(repeat (length ed)
(if (= (car (nth i ed)) 10) ;if item is a vertex
(progn
(setq vt (cdr (nth i ed))) ; get vertex values
(setq X (car vt)) ; get the x value
(setq Y (cadr vt)) ; get the y value
(setq Y (+ 5 Y)) ; increment the Y value by 5 units
; replace the old y value with the new y value
(setq vt (subst Y (nth 1 vt) vt))
; update the entity definition with new vertex information
(setq ed (subst (cons 10 vt) (nth i ed) ed))
(entmod ed) ; update the drawing
) ;progn
) ;if
(setq i (1+ i))
) ;repeat
) ;Test
  (defun C:MyTest (/ e ed)
(setq e (car (entsel))
ed (entget e)
)
(if (= (cdr (assoc 0 ed)) "LWPOLYLINE")
(test e ed)
) ;if
) ;C:MyTest

