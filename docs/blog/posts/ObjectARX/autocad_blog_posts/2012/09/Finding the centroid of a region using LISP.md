---
title: "Finding the centroid of a region using LISP"
date: 2012-09-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
  - Polyline
description: "When a polyline is changed to a REGION you can get the center of gravity using MASSPROP. Variables exist for PERIMETER and AREA but not for the Cen..."
author: Autodesk
---
# Finding the centroid of a region using LISP

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/finding-the-centroid-of-a-region-using-lisp.html

## 文章内容

By Xiaodong Liang
Issue
When a polyline is changed to a REGION you can get the center of gravity using MASSPROP. Variables exist for PERIMETER and AREA but not for the Center of Gravity. How can an Auto LISP routine extract the Center of Gravity from a region ?
Solution
Use the ActiveX interface to return the Cenroid property for a region. The following AutoLISP code does this:
(defun GetCentroid ()
 (vl-load-com)
 (setq anEnt (entsel "\nSelect A Region: "))
 (if anEnt
    (progn
      (setq anObj (vlax-ename->vla-object (car anEnt)))
      (princ (strcat "\nObject Name: " (setq objName (vla-Get-ObjectName
anObj))))
      (if (equal objName "AcDbRegion")
        (progn
          (setq vCentroid (vla-Get-Centroid anObj))
          (setq strCentroidProp (vl-princ-to-string (setq CentroidLst
(vlax-safearray->list (vlax-variant-value vCentroid)))))
          (if (< (length CentroidLst) 3)
           (setq CentroidLst (append CentroidLst (list 0.0)))
          )
          (princ (strcat "\nRegion Centroid: " strCentroidProp))
          (setvar "PDMODE" 3)
          (setq *MS* (vla-Get-ModelSpace (setq acadDoc
(vla-Get-ActiveDocument (setq acadApp (vlax-get-acad-object))))))
          (setq ptObj (vla-AddPoint *MS* (vlax-3d-Point CentroidLst)))
          (vla-Put-Color ptObj acYellow)
        )
        (princ "\nRegion was not selected !")
      )
    )
 )
 (princ)
)

(princ "\nGetCentroid loaded, type (GetCentroid) to run.")
(princ)

## 评论

**内容**: Yasir said...
Thank you so much for sharing this extremely useful routine. It made my life a lot easier :)
Reply
05/31/2015 at 05:58 AM

---
