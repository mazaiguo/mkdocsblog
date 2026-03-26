---
title: "How to find the Model Space Viewport View Directions using Visual LISP in AutoCAD"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - AutoCAD
  - AutoLISP
description: "Someone asked how to obtain the Model Space Vports’ View Direction using LISP. I found it pretty tricky. I say tricky, because I actually was not a..."
author: Autodesk
---
# How to find the Model Space Viewport View Directions using Visual LISP in AutoCAD

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-find-the-model-space-viewport-view-directions-using-visual-lisp-in-autocad.html

## 文章内容

by Fenton Webb
Someone asked how to obtain the Model Space Vports’ View Direction using LISP. I found it pretty tricky. I say tricky, because I actually was not able to find a clean solution (without toggling TILEMODE) – perhaps some of you LISP “Jedi masters” will know of a better way?
The problem is that, for performance reasons, the table which contains the View Direction data is only updated when you switch TILEMODE. Now in ObjectARX or .NET of course, you have full control when those tables will be updated (using acedVports2VportTableRecords) but for LISP it’s not so easy (unless, of course, you use .NET to expose a LispFunction which calls acedVports2VportTableRecords).
Anyway, here’s the LISP Code…
(defun c:vptest ()
   (vl-load-com) ; always make sure the COM system is loaded
   ; This is done to synchronize the viewports with the Viewport Table records
   ; In ObjectARX this is done with acedVports2VportTableRecords() 
   (setvar "tilemode" 0)
   (setvar "tilemode" 1)
 
  ;Get the Viewports collection
  (setq objAcad   (vlax-get-acad-object)
        objDoc    (vla-get-ActiveDocument objAcad)
        objVports (vla-get-viewports objDoc)
  )
  ; use a for loop and loop through the viewports
  (vlax-for objVport objVports
    ;(vlax-dump-object objVport)   ; Print out objects properties
    ; get the direction of the viewport
    (setq directionVariant (vla-get-direction objVport))
    (setq safArray (vlax-variant-value directionVariant))
    ; Get the x,y,z values of the direction
    ; this can be used to determine the view
    (setq x (vlax-safearray-get-element safArray 0))
    (print (strcat "X=" (rtos x)))
    (setq y (vlax-safearray-get-element safArray 1))
    (print (strcat "Y=" (rtos y)))
    (setq z (vlax-safearray-get-element safArray 2))
    (print (strcat "Z=" (rtos z)))
    ; this is a simple example of setting the active viewport
    ; if x equals zero then make this viewport the active viewport
    ; this test would need to be enhanced to test the y and z values
    ; y should equal zero and x should be 1 (that is WCS)
    (if (= x 0.0)
      (vla-put-activeviewport objDoc objVport)
    )   
  )
  (princ)
)

## 评论

**内容**: Steve Hill said...
Thanks for posting, this is great. Anyway you can post the .NET version as well?
Reply
05/23/2012 at 10:53 AM

---
