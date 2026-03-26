---
title: "Lock a viewport using Visual LISP"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
description: "It is not possible to lock the viewport by using (entmod).  However, it can be successfully done using ActiveX functions.  The following sample cod..."
author: Autodesk
---
# Lock a viewport using Visual LISP

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/lock-a-viewport-using-visual-lisp.html

## 文章内容

By Augusto Goncalves
It is not possible to lock the viewport by using (entmod).  However, it can be successfully done using ActiveX functions.  The following sample code checks the viewport object's DisplayLocked property and, if currently unlocked, proceeds to lock it:
(defun c:LockVP ()
    (vl-load-com)
    (setq app (vlax-get-acad-object)
         doc (vla-get-activedocument app)
         ent (car (entsel "\nSelect a viewport:"))
         obj (vlax-ename->vla-object ent)
    )
 
   (if (= (vlax-get-property obj 'objectName) "AcDbViewport")
     (progn


       (setq vpLk (vlax-get-property obj 'DisplayLocked))
       (if (= vpLk :vlax-false)
        (progn
            (vlax-put-property obj 'DisplayLocked :vlax-true)
            (setq vpLk (vlax-get-property obj 'DisplayLocked))
            (alert "Viewport is now locked")
         )
       (alert "Viewport was already locked")
       )
     )
   (alert "Not a viewport")
   )
)

