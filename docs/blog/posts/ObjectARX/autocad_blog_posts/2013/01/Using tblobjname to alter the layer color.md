---
title: "Using tblobjname to alter the layer color"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Layer
description: "I'm trying to use entmod to update the color of a layer, but I cannot get this code to work:"
author: Autodesk
---
# Using tblobjname to alter the layer color

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/using-tblobjname-to-alter-the-layer-color.html

## 文章内容

By Xiaodong Liang
Issue
I'm trying to use entmod to update the color of a layer, but I cannot get this code to work:
(defun WrongChgLyrClr (laynme layclr / tb3 tb4)
  (if (tblsearch "LAYER" laynme)
    (progn
     (setq tb3 (tblsearch "LAYER" laynme))
     (setq tb4 (subst (cons 62 layclr) (assoc '62 tb3) tb3))
     (if
       (entmod tb4)
         (princ (strcat "\nLayer Color Updated to: " (itoa layclr)))
         (princ "\nLayer Color Was NOT Updated.")
     )
      )
    (princ (strcat "\nLayer: " " was NOT found !"))
  )
 (princ)
)
; (WrongChgLyrClr "CIRCLES" 4)
What am I doing wrong ?
Solution
In order to update the color assigned to a layer you'll need to use the entity list obtained from the entity name returned by the (tblobjname) function, and not the list returned by the tblsearch or tblnext functions. The entmod function will only update the layer with the entity list obtained via the tblobjname entity.
(defun ChgLyrClr (laynme layclr / tb3 tb4)
  (if (tblsearch "LAYER" laynme)
    (progn
     (setq tb3 (entget (tblobjname "LAYER" laynme)))
     (setq tb4 (subst (cons 62 layclr) (assoc '62 tb3) tb3))
     (if
       (entmod tb4)
         (princ (strcat "\nLayer Color Updated to: " (itoa layclr)))
         (princ "\nLayer Color Was NOT Updated.")
     )
    )
    (princ (strcat "\nLayer: " " was NOT found !"))
  )
 (princ)
)

; (ChgLyrClr "CIRCLES" 7)
(princ "\nChgLyrClr loaded, type (ChgLyrClr \"ALayerName\" (setq aLayerColor 7))
to run.")
(princ)

## 评论

**内容**: OneCADUser said...
Exactly what i found out the hard way. Read this after finding the solution on my own hahaha.
I'm glad i was not crazy.
Thanks.
Reply
06/17/2021 at 10:13 AM

---
