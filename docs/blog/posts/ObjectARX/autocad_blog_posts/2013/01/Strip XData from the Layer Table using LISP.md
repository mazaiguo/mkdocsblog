---
title: "Strip XData from the Layer Table using LISP"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Layer
description: "How do I remove the XDATA that is attached to my Layer Table ?"
author: Autodesk
---
# Strip XData from the Layer Table using LISP

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/strip-xdata-from-the-layer-table-using-lisp.html

## 文章内容

By Fenton Webb
Issue
How do I remove the XDATA that is attached to my Layer Table ?
Solution
The following AutoLISP code will remove all the XData attached to the Layer Table:

(defun StripLayerXdata ()
 (setq aLayerLst (tblnext "LAYER" T))
 (while aLayerLst
   (setq aLayerName (cdr (assoc '2 aLayerLst)))
   (setq aLayerELst (entget (tblobjname "LAYER" aLayerName) '("*")))
   (if (setq xdata (assoc '-3 aLayerELst))
     (progn
    (setq newLayerLst (subst (cons (car xdata) (list (list (caadr xdata))))
xdata aLayerELst))
    (entmod newLayerLst)
     )
   )
   (setq aLayerLst (tblnext "LAYER"))
 )
 (princ)
)
(vl-doc-export 'StripLayerXdata)
(princ "\nStripLayerXdata loaded, type (StripLayerXdata) to run.")
(princ)

