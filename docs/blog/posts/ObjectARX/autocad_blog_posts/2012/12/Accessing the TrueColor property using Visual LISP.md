---
title: "Accessing the TrueColor property using Visual LISP"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Layer
description: "How to access the TrueColor property of an entity in AutoCAD? Also, is there a way to set an object's color back to "ByLayer"?"
author: Autodesk
---
# Accessing the TrueColor property using Visual LISP

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/accessing-the-truecolor-property-using-visual-lisp.html

## 文章内容

By Philippe Leefsma
Q:
How to access the TrueColor property of an entity in AutoCAD? Also, is there a way to set an object's color back to "ByLayer"?
A:
First, it is necessary to access the object's TrueColor property, using vlax-get-property.  The RGB (Red, Green and Blue) values of TrueColor are read-only, so you can not individually modify them.  You must invoke the SetRGB method and set all three values at once.  Then, using vlax-put-property, you can set the object's TrueColor property to reflect the new RGB values.  You will notice that an object whose color is "ByLayer" returns RGB values of R=0, G=0, B=0.  However, setting these values explicitly, with SetRGB, will not restore the color to "ByLayer".  To reset the color to "ByLayer", it is necessary to set TrueColor's ColorIndex property to acBylayer.  The example below creates a line, whose color is initially "ByLayer".  We then change it to blue, and finally back to ByLayer:
(defun c:TestTrueClr()
   (vl-load-com)
   (setq oApp (vlax-get-Acad-Object)
           oDoc (vla-get-ActiveDocument oApp)
           oMSp (vla-get-ModelSpace oDoc)
   )
   ;; Add a Line
   (setq oLine (vla-AddLine oMSp  (vlax-3d-point '(1.0 1.0 0.0))  (vlax-3d-point '(10.0 10.0 0.0))))
    (vla-update oLine)

   ;; Get the current color values
   (setq oColor (vlax-get-property oLine 'TrueColor)
           clrR (vlax-get-property oColor 'Red)
           clrG (vlax-get-property oColor 'Green)
           clrB (vlax-get-property oColor 'Blue)
   )
   (alert (strcat "Old Color - Red: " (itoa clrR) " Green: " (itoa clrG) " Blue: " (itoa clrB)))

   ;; Set TrueColor to blue (R=0, G=101, B=204)
   (vlax-invoke-method oColor 'SetRGB 0 101 204)
   (vlax-put-property oLine 'TrueColor oColor)
   (vla-update oLine)

   ;; Inspect the new color values
   (setq oColor (vlax-get-property oLine 'TrueColor)
           clrR (vlax-get-property oColor 'Red)
           clrG (vlax-get-property oColor 'Green)
           clrB (vlax-get-property oColor 'Blue)
   )
   (alert (strcat "New Color - Red: " (itoa clrR) " Green: " (itoa clrG) " Blue: " (itoa clrB)))
  
   ;; Reset color to acBylayer
   (vlax-put-property oColor 'ColorIndex acByLayer)
   (vlax-put-property oLine 'TrueColor oColor)
   (vla-update oLine)

   ;; Inspect the color values
   (setq oColor (vlax-get-property oLine 'TrueColor)
           clrR (vlax-get-property oColor 'Red)
           clrG (vlax-get-property oColor 'Green)
           clrB (vlax-get-property oColor 'Blue)
   )
   (alert (strcat "New Color - Red: " (itoa clrR) " Green: " (itoa clrG) " Blue: " (itoa clrB)))
)

