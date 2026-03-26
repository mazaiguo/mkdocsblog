---
title: "Setting the bulge of a polyline using ActiveX in LISP"
date: 2012-09-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
  - Polyline
description: "This is the Visual LISP code I have used to set a bulge for a polyline:"
author: Autodesk
---
# Setting the bulge of a polyline using ActiveX in LISP

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/setting-the-bulge-of-a-polyline-using-activex-in-lisp.html

## 文章内容

By Xiaodong Liang
Issue
This is the Visual LISP code I have used to set a bulge for a polyline:
Command: !pline
#
Command: !mspace
#
Command: (vla-SetBulge mSpace pline 0 0.5)
; error: ActiveX Server returned the error: unknown name: SetBulge
Command: (vla-put-SetBulge pline 0 0.5)
; error: no function definition: VLA-PUT-SETBULGE
Command: (vlax-invoke-method mspace 'setbulge pline 0 0.5)
; error: ActiveX Server returned the error: unknown name: SETBULGE
Command: (vlax-put-property pline 'setbulge 0 0.5)
; error: ActiveX Server returned an error: Type mismatch
    What is the correct syntax to use?
Solution
The documentation contains the information to answer this question. In the AutoCAD ActiveX and VBA Reference, go to Object Model -> Polyline Object -> SetBulge Method.
Then refer to the Visual LISP Developer's Guide: Using Visual LISP Functions with ActiveX Methods -> Determining How to Call a Function.
After reading these two references, you should notice that SetBulge is a method of the polyline object, not a Property nor a Method of the Model Space Collection (which is what the preceding code shows).
You'll find that the following code will set the bulge of a Polyline Object:
(vla-SetBulge myPolyObj 1 -0.42080)
Because it is easier to see this in context, code was copied from , and modified it to use the SetBulge method for a polyline:
(vl-load-com)
(defun a_Polyline_wArc()

  (setq acadapp (vlax-get-Acad-Object)
     acaddoc (vla-get-ActiveDocument acadapp)
     *ModelSpace*  (vla-get-ModelSpace acaddoc)
  )


  (setq pt1 (list 2.93905 1.87048 0.0))
  (setq pt2 (list 5.54349 4.81627 0.0))
  (setq pt3 (list 8.78096 4.97892 0.0))
  (setq pt4 (list 12.6153 1.20181 0.0))

  (setq Points (apply 'append (list pt1 pt2 pt3 pt4)))
  (setq ptlstlen (length Points))

  (setq PointDataA (vlax-make-safearray vlax-vbDouble (cons 0 (1- ptlstlen))))
  (vlax-safearray-fill PointDataA Points)
  (setq PointData (vlax-make-variant PointDataA (logior vlax-vbarray
vlax-vbDouble)))

  (setq myPolyObj (vla-addPolyline *ModelSpace* PointData))

  (vla-Put-Color myPolyObj acBlue)

  (setq strtWidth 1.0 endWidth 1.0 verticies (1- (/ ptlstlen 3)) indx 0)
  (while (< indx verticies)
       (vla-SetWidth myPolyObj indx strtWidth endWidth)
       (setq indx (1+ indx))
  )
  (vla-SetBulge myPolyObj 1 -0.42080)
  (vla-Update myPolyObj)
  
  (princ)
)
; (a_Polyline_wArc)

