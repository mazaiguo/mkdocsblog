---
title: "Determine if text is annotative"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - DXF
  - Unicode
description: "It is possible to check the DXF code and the XDATA of the text to determine if a text entity is annotative. Annotative text has XDATA with an appli..."
author: Autodesk
---
# Determine if text is annotative

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/determine-if-text-is-annotative.html

## 文章内容

By Augusto Goncalves
It is possible to check the DXF code and the XDATA of the text to determine if a text entity is annotative. Annotative text has XDATA with an application name "AcadAnnotative". Also the second 1070 DXF code will be 1.
To determine if text is annotative, get the XDATA with the application name and check the second 1070 DXF code. This approach will also apply to other objects that support the annotative feature.
The following lisp code determines if a selected entity is annotative.
(defun IsAnnotative ()
  (setq elst (entget (car (entsel)) '("AcadAnnotative")))
  (setq xlst (assoc -3 elst))
  (if (= xlst nil)
    (print "It's NOT annotative!")
    (progn
      (setq xlst1 (nth 1 xlst))
      (setq bAnnotative (cdr (nth 4 xlst1)))
      (if (= bAnnotative 0)
       (print "It's NOT annotative!")
       (print "It's annotative!")
      )
    )
  )
  (princ)
)

