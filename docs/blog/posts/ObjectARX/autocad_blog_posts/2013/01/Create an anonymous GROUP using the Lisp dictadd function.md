---
title: "Create an anonymous GROUP using the Lisp dictadd function"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
description: "The dictadd function does not accept anonymous names. To work around this, set group code 70 to 1 and create a GROUP with a proper name and then su..."
author: Autodesk
---
# Create an anonymous GROUP using the Lisp dictadd function

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/create-an-anonymous-group-using-the-lisp-dictadd-function.html

## 文章内容

By Gopinath Taget
The dictadd function does not accept anonymous names. To work around this, set group code 70 to 1 and create a GROUP with a proper name and then subsequently change the name to something similar to "*A1". Below is an example that allows you to select two entities that become part of a anonymous GROUP.
NOTE: This example does not check for the prior existence of a GROUP named "AA" or "*A1".
(defun c:Test()
  (setq a (car (entsel "Select first entity: "))
          b (car (entsel "Select second entity: "))
          c (list (cons 0 "GROUP")
                   (cons 100 "AcDbGroup")
                   (cons 340 a)
                   (cons 340 b)
                   (cons 70 1)
                   (cons 71 1))
         d (entmakex c)
         e (dictsearch (namedobjdict) "ACAD_GROUP")
  )
    (dictadd (cdr (assoc -1 e)) "AA" d)
    (setq f (dictsearch (namedobjdict) "ACAD_GROUP"))
  (entmod (subst (cons 3 "*A1") (assoc 3 f) f))
)

