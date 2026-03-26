---
title: "Convert 3dface to polyline"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Dimension
  - Polyline
  - Selection
description: "To convert 3dFaces to polylines, what you'll need to do is"
author: Autodesk
---
# Convert 3dface to polyline

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/convert-3dface-to-polyline.html

## 文章内容

By Xiaodong Liang
To convert 3dFaces to polylines, what you'll need to do is
collect the 3dFace vertex data, and create a polyline using that information. Since a 3dFace will probably be construced with differing X,Y, and Z coordinates you can only re-create them as a 3dPolyline. If the face's Z coordinates are on the same elevation, you could re-create them as a 2d polyline. Here's some lisp
code to demonstrate this:
defun C:3DFtoPL(/ ss1 sl i)
  (setq ss1 (ssget "X" (list (cons '0 "3DFACE"))))
  (setq sl (sslength ss1))
  (setq i 0)
  (while (< i sl)
     (setq ent1 (entget (setq e1 (ssname ss1 i))))
     (setq pt1 (cdr (assoc '10 ent1)))
     (setq pt2 (cdr (assoc '11 ent1)))
     (setq pt3 (cdr (assoc '12 ent1)))
     (setq pt4 (cdr (assoc '13 ent1)))
     ;  Plain 2D Polylines
     ;(command "PLINE" pt1 pt2 pt3)
     ; 3dPolylines ->
     (command "3DPOLY" pt1 pt2 pt3)
     (if (/= pt3 pt4) (command pt4 "c") (command "c") )
     (entdel e1)
     (setq i (1+ i))
  )
  (setq ss1 nil)
  (princ)
)

(princ "\nC:3DFtoPL loaded, to run type 3DFtoPL.")
(princ)

## 评论

**内容**: Eddy said...
Top! thnx
Reply
06/24/2015 at 08:51 AM

---
**内容**: Chi said...
This is very helpful! Thank you so much!!!
Reply
03/27/2017 at 08:25 PM

---
