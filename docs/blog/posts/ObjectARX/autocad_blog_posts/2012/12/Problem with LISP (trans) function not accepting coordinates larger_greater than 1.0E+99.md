---
title: "Problem with LISP (trans) function not accepting coordinates larger/greater than 1.0E+99"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
  - Dimension
description: "In Visual LISP, you will get an error if you use the TRANS function with a large input value - For example, type the following LISP expression at t..."
author: Autodesk
---
# Problem with LISP (trans) function not accepting coordinates larger/greater than 1.0E+99

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/problem-with-lisp-trans-function-not-accepting-coordinates-largergreater-than-10e99.html

## 文章内容

by Fenton Webb
In Visual LISP, you will get an error if you use the TRANS function with a large input value - For example, type the following LISP expression at the command prompt:
(trans (0.0 0.0 3.0e+099) 0 1)
To solve this issue, best thing is to use the ActiveX TranslateCoordinates() method of the Utility class.
The following code shows how the TranslateCoordinates() method is successful for an input point of (0.0 0.0 3e+99), where…
(trans (0.0 0.0 3e+099) 0 1)
…would fail.
(defun c:Test()
  (vl-load-com)
  (setq poActDoc (vla-get-ActiveDocument (vlax-get-acad-object)))
  (setq poUtility(vla-get-Utility poActDoc))
  (setq poTestPoint (vlax-3d-point '(0.0 0.0 3e+99)))
  (setq poRetPoint(vla-TranslateCoordinates poUtility poTestPoint acUCS acWORLD 0))
  (princ (vlax-safearray->list (vlax-variant-value poRetPoint)))
  (princ)
)

