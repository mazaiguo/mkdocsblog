---
title: "Create Section Object using VLISP"
date: 2018-02-01
categories:
  - AutoLISP
tags:
  - API
  - AutoLISP
description: "I have received a query using entmake lisp API to create a section object with same color for both entity and plane indicator."
author: Autodesk
---
# Create Section Object using VLISP

发布日期: 2018-02-01

原始链接: https://adndevblog.typepad.com/autocad/2018/02/create-section-object-using-vlisp.html

## 文章内容

By Madhukar Moogala
I have received a query using entmake lisp API to create a section object with same color for both entity and plane indicator.
For some reason, following lisp code, is not updating plane indicator color.
(entmake
(list
'(0 . "SECTIONOBJECT")
'(100 . "AcDbEntity")
'(100 . "AcDbSection")
'(67 . 0) 
'(410 . "Model")
'(8 . "CAT");Layer
'(62 . 1) ; Entity Color
'(90 . 1) ; Section State
'(91 . 5) ; Section Flags
'(1 . "v1") ; Name
'(10 0.0 0.0 -1.0) ; vertical direction
'(40 . 10) 
'(41 . 5) ;
'(70 . 5) ; Transparency
'(62 . 1) ; Plane Indicator Color
'(92 . 2) ; Num of Vertices
'(11 -5 3 2) ; Cutting height start point of the baseline
'(11 5 3 2) ; Target point of the baseline
)
)
Using ActiveX Visual Lisp we can ensure to have same color for the Section Entity and Section Plane Indicator
(defun c:createsection ( / acadObj doc point1 point2 vec modelSpace sectionObj fillColor)
 (vl-load-com) ; always make sure the COM system is loaded
    (setq acadObj (vlax-get-acad-object))
    (setq doc (vla-get-ActiveDocument acadObj))
    (setq point1 (vlax-3d-point -5 3 2)
          point2 (vlax-3d-point 5 3 2)
    vec    (vlax-3d-point 0 0 -1)
 ) 
    (setq modelSpace (vla-get-ModelSpace doc))
    (setq sectionObj (vla-AddSection modelSpace point1 point2 vec))
 (vlax-put-property sectionObj 'Color 2)
 (setq fillColor (vlax-create-object "AutoCAD.AcCmColor.22"))
 (vla-put-ColorIndex fillColor 2)
 (vlax-put-property sectionObj 'IndicatorFillColor fillColor)
 (vla-ZoomExtents acadObj)
 )

