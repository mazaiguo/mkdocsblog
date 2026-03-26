---
title: "Using LISP to create a region via ActiveX"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
description: "The main issue is related to the Safearray, so the following code creates a region from an arc and a line and alter its color. You should be able t..."
author: Autodesk
---
# Using LISP to create a region via ActiveX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/using-lisp-to-create-a-region-via-activex.html

## 文章内容

By Augusto Goncalves
The main issue is related to the Safearray, so the following code creates a region from an arc and a line and alter its color. You should be able to easily convert it into just creating a region from a circle:
(defun AddRegion ()
  (vl-load-com)
  (setq acadapp (vlax-get-Acad-Object)
acaddoc (vla-get-ActiveDocument acadapp)
mspace (vla-get-ModelSpace acaddoc)
  )
  (setq arcObj (vla-AddArc
   mspace
   (vlax-3d-point '(5.0 3.0 0.0))
   2.0
   0.0
   pi
        )
  )
  (setq arcClr (vla-Put-Color arcObj acYellow))
  (setq arcStrtPoint (vla-Get-StartPoint arcObj))
  (setq arcEndPoint (vla-Get-EndPoint arcObj))
  (setq lineObj (vla-AddLine mspace arcStrtPoint arcEndPoint))
  (setq lClr (vla-Put-Color lineObj acGreen))

  (setq objArray (vlax-make-safearray vlax-vbObject '(0 . 1)))
  (vlax-safearray-fill objArray (list arcObj lineObj))


  (setq regionObjList (vla-AddRegion mspace objArray))
  (setq rSA (vlax-variant-value regionObjList))
  (setq regionList (vlax-safearray->list rSA))
  (setq regionObj (car regionList))
  (setq rClr (vla-Put-Color regionObj acMagenta))


;;; Release the Objects:
  (if regionObj
    (if (null (vlax-object-released-p regionObj))
      (progn (vlax-release-object regionObj) (setq regionObj nil))
    )
  )
  (if arcObj
    (if (null (vlax-object-released-p arcObj))
      (progn (vlax-release-object arcObj) (setq arcObj nil))
    )
  )
  (if lineObj
    (if (null (vlax-object-released-p lineObj))
      (progn (vlax-release-object lineObj) (setq lineObj nil))
    )
  )
  (if mspace
    (if (null (vlax-object-released-p mspace))
      (progn (vlax-release-object mspace) (setq mspace nil))
    )
  )
  (if acaddoc
    (if (null (vlax-object-released-p acaddoc))
      (progn (vlax-release-object acaddoc) (setq acaddoc nil))
    )
  )
  (if acadapp
    (if (null (vlax-object-released-p acadapp))
      (progn (vlax-release-object acadapp) (setq acadapp nil))
    )
  )
  (princ)
)
(princ "\nAddRegion loaded. Enter (addregion) to run.")
(princ)

