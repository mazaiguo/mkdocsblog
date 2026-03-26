---
title: "Rotation angle of MText using Lisp"
date: 2012-06-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Unicode
description: "The angle of the MTEXT entity is contained in the group code 11 entry."
author: Autodesk
---
# Rotation angle of MText using Lisp

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/rotation-angle-of-mtext-using-lisp.html

## 文章内容

By Balaji Ramamoorthy
The angle of the MTEXT entity is contained in the group code 11 entry.
Consider this MTEXT entity:
Command: MTEXT
Specify first corner: 5,5
Specify opposite corner or [Height/Justify/Line spacing/Rotation/Style/Width/Columns]: R
Specify rotation angle <0>: 30
Specify opposite corner or [Height/Justify/Line spacing/Rotation/Style/Width/Columns]: @10,10
MText: Welcome
Command: (entget (entlast)) ((-1 . ) (0 . "MTEXT") (5 . "2B") (100 . "AcDbEntity") (67 . 0) (8 . "0") (100 . "AcDbMText") (10 5.0 5.0 0.0) (40 . 0.619107) (41 . 5.0) (71 . 1) (72 . 1) (1 . "Welcome") (7 . "STANDARD") (210 0.0 0.0 1.0) (11 0.866025 0.5 0.0))
The rotation of the MTEXT was 30 degrees and in group code 11 we can see the values 0.866 and 0.5. These values are simply cos(30) and sin(30).
Here is a sample Lisp code :
;; Find the MText angle of rotation
(defun c:mtangle()
    (setq ed (entget (car(entsel))))
    (if (equal (cdr (assoc 0 ed)) "MTEXT")
        (progn
            (princ (* 180.0 (/ (acos (nth 1 (assoc 11 ed))) pi)))
            (princ "\n")
            (princ (* 180.0 (/ (asin (nth 2 (assoc 11 ed))) pi)))
            (princ)
        )
    )
)
  ;; Based on relation between atan and asin
;; http://en.wikipedia.org/wiki/Inverse_trigonometric_functions#Relationships_among_the_inverse_trigonometric_functions
(defun asin (x)
    (cond
        (    (equal x -1 1e-6)
            (/ pi -2)
        )
          (    (equal x 1 1e-6)
            (/ pi 2)
        )
          (    (< -1 x 1)
            (atan x (sqrt (- 1 (* x x))))
        )
    )
 )
  ;; Based on relation between atan and acos
;; http://en.wikipedia.org/wiki/Inverse_trigonometric_functions#Relationships_among_the_inverse_trigonometric_functions
(defun acos (x)
    (cond
        (    (equal x -1 1e-6)
            pi
        )
          (    (equal x 1 1e-6)
            0.0
        )
          (    (< -1 x 1)
            (atan (sqrt (- 1 (* x x))) x)
        )
    )
 )

## 评论

**内容**: Kerry Brown said...

or with VLisp

(if (and (setq ent (vlax-ename->vla-object (car (entsel))))
(vlax-property-available-p ent 'Rotation)
)
(/ (* (vla-get-rotation ent) 180.0) pi)
)
(though the elegance is sort of spoiled by the lack of formatting on the blog) :-)
Reply
06/02/2012 at 03:24 AM

---
**内容**: Balaji said...
Thanks for sharing the vla method to the do the same.
I am sure, this will help the readers of this blog post.
Reply
06/03/2012 at 10:58 PM

---
