---
title: "Aligning MText with picked point on a curve"
date: 2015-04-01
categories:
  - AutoCAD
tags:
  - Unicode
description: "In this discussion forum post, the developer wanted an MText to align automatically with the curve without having to provide additional inputs for ..."
author: Autodesk
---
# Aligning MText with picked point on a curve

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/aligning-mtext-with-picked-point-on-a-curve.html

## 文章内容

By Balaji Ramamoorthy
In this discussion forum post, the developer wanted an MText to align automatically with the curve without having to provide additional inputs for specifying the rotation. Kent Cooper's nice reply in that forum post provides all that is necessary to implement that. Since this requirement of aligning an MText along a curve is quite essential in Civil / Survey applications, I am posting a bare-bone implementation of it that you can customize. The key to finding the rotation is to determine the first derivative (slope) of the curve at the point the entity was selected. 
Here is the code snippet :
(vl-load-com)

(setq es    (entsel)
      entpt (osnap (cadr es) "_nea")
      ang   (angle '(0 0 0)
     (vlax-curve-getFirstDeriv
       (vlax-ename->vla-object (car es))
       (vlax-curve-getParamAtPoint
         (vlax-ename->vla-object (car es))
         entpt
       )
     )
     )
)
(if (and (> ang (/ pi 2)) (<= ang (* pi 1.5)))
  (setq ang (+ ang pi))
)
(setq hght (getreal "\nText Height : "))
(setq
  mspace (vla-get-modelspace
    (vla-get-activedocument (vlax-get-acad-object))
  )
)

(setq mtextobj (vla-addMText
   mspace
   (vlax-3d-point entpt)
   0.0
   "AUTOCAD"
        )
)
(vla-put-attachmentPoint
  mtextobj
  acAttachmentPointMiddleCenter
)
(vla-put-insertionPoint mtextobj (vlax-3d-point entpt))
(vla-put-Rotation mtextobj ang)
(vla-put-Height mtextobj hght)
(vla-put-Color mtextobj 7)
(vla-put-backgroundfill mtextobj :vlax-true)
Here is a sample output :

