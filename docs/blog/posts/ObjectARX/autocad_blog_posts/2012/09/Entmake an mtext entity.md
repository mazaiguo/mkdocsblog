---
title: "Entmake an mtext entity"
date: 2012-09-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Unicode
description: "How can I use entmake in the following AutoLISP code to create an MTEXT entity? I can create a TEXT entity using similar code as below, but it does..."
author: Autodesk
---
# Entmake an mtext entity

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/entmake-an-mtext-entity.html

## 文章内容

By Xiaodong Liang
Issue
How can I use entmake in the following AutoLISP code to create an MTEXT entity? I can create a TEXT entity using similar code as below, but it does not work.
(defun CreateMText ()

 (if 
   (entmake
     (list
    (cons 0 "MTEXT")          ; Entity Type
    (cons 1 "Some Text Here")      ; Text String
    (cons 10 '(0.0 0.0 0.0))      ; Insertion Point
    (cons 40 0.25)              ; Text Height
    )
   )

   (princ "\nText Entity Created.")
   (princ "\nText Entity was NOT Created.")
   )
   (princ)
)
  Solution
For entities such as MTEXT that were created after AutoCAD R12, you will need to add the Entity SubClass Markers, group code 100, for this to work:
 (defun CreateMtext ()

 (if 
   (entmake
     (list
    (cons 0 "MTEXT")       ; Entity Type
    (cons 100 "AcDbEntity")    ; 100 Entity Code
    ;(cons 8 "DIM")         ; The Layer
    (cons 100 "AcDbMText")       ; 100 Entity Code
   
     ; For Other Formatting Codes See the:
     ; ActiveX and VBA Developer's Guide ->
     ; Chapter 4 -- Creating and Editing AutoCAD Entities ->
     ; Adding Text to Drawings ->
     ; Using Multiline Text (Mtext) ->
     ; Formatting Multiline Text
   
    (cons 1 "\\S100^200")       ; Stacked Text
    (cons 10 '(0.0 0.0 0.0))   ; Insertion Point
    )
   )


   (princ "\nMtext Entity Created.")
   (princ "\nMtext Entity NOT Created.")
   )
   (princ)
)
(princ "\nCreateMtext loaded, type (CreateMtext) to run.")
(princ)

