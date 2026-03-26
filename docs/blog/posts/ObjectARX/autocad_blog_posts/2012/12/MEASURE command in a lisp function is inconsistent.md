---
title: "MEASURE command in a lisp function is inconsistent"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Polyline
description: "I am using the measure" command in a lisp routine. On some polylines the first mark is incorrect for example if I use 10 for the distance the first..."
author: Autodesk
---
# MEASURE command in a lisp function is inconsistent

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/measure-command-in-a-lisp-function-is-inconsistent.html

## 文章内容

By Philippe Leefsma
Q:
I am using the measure" command in a lisp routine. On some polylines the first mark is incorrect for example if I use 10 for the distance the first mark is not 10 units from the begining of the line. Here is the code I am trying to use:
(Defun c:test (/)
   (setq lineData (entsel "\nSelect a line:")
            lineObj   (car lineData)
   ) ;_ end of setq
   (command "measure" lineObj  10)
) ;_ end of Defun
A:
When you manually use the MEASURE command it starts adding the points nearest to the end of the line where you selected. There does not seem to be a way to consistently control which end of the line the command MEASURE starts measuring from when the entity name is passed to the command in the lisp routine instead of selecting the entity. Another approach to consider would be to use vlax-curve-getPointAtDist. This example places points along the selected polyline at the same location as the Measure command would with a distance of 10.
(Defun c:test (/)
  (vl-load-com)
  (setq acadDoc  (vla-get-ActiveDocument (vlax-get-Acad-Object))
           mSpace   (vla-get-modelspace acadDoc)
           entData   (entsel "\nSelect a polyline:")
           spdata     (car entData)
           plineHandle (cdr (assoc 5 (entget spData)))
           plineObj    (vla-handleToObject acadDoc plineHandle)
           endSpline   (vlax-curve-getEndParam plineObj)
           pLength     (vlax-curve-getDistAtParam plineObj endSpline)
            numOfPoints (fix (/ pLength 10))
  ) ;setq
  (setq count 1)
  (repeat numOfPoints
    (setq dist (* 10 count))
    (setq pnt1 (vlax-curve-getPointAtDist plineObj dist))
    (vla-addpoint mspace (vlax-3d-Point pnt1))
    (setq count (+ count 1))
  ) ;repeat
)
The MEASURE command will also allow you to insert a block along the line. The example below inserts a block named "testBlock" and rotates it so that it is close to the rotation of the angle at that point along the line. This could be changed to get a higher degree of accuracy for the angle. You could get a point that is a little behind and a little ahead to determine the required angle.
NOTE: There is no error checking, and the block named "testBlock" needs to be available in the drawing.
(Defun c:test (/)
  (vl-load-com)
  (setq acadDoc  (vla-get-ActiveDocument (vlax-get-Acad-Object))
           mSpace   (vla-get-modelspace acadDoc)
           entData   (entsel "\nSelect a polyline:")
           spdata     (car entData)
           plineHandle (cdr (assoc 5 (entget spData)))
           plineObj    (vla-handleToObject acadDoc plineHandle)
           endSpline   (vlax-curve-getEndParam plineObj)
           pLength     (vlax-curve-getDistAtParam plineObj endSpline)
           numOfPoints (fix (/ pLength 10))
  ) ;setq
  (setq count 1)
  (repeat numOfPoints
    (setq dist (* 10 count))
    (setq pnt1 (vlax-curve-getPointAtDist plineObj dist))
    (setq dist2 (+ dist 0.1)) 
    ;; get a sample point that is 0.1 ahead of the point that will
    ;;be used for insertion
    (setq pnt2 (vlax-curve-getPointAtDist plineObj dist2))
    ;; get the angle between the insertion point and the sample point
    (setq ang1 (angle pnt1 pnt2))
    (vla-insertblock mspace (vlax-3d-Point pnt1) "testBlock" 1.0 1.0 1.0 ang1)
    (setq count (+ count 1))
  ) ;repeat
)

## 评论

**内容**: Andres said...
Is there a way to modify the routine in order to place a single point at an specific distance?
I need this in order to locate samples in a tunnel.
Regards,
Andres
Reply
04/15/2016 at 09:55 AM

---
**内容**: kumar said...
HI
I am using distance command for measure the bolt to blot distance
(3 points values are 1225 +108+1025) each point I am measure and typing in cad , any lisp is there to n-point measuring and typing automatically like above
Reply
07/08/2016 at 03:35 AM

---
