---
title: "Using the align command in AutoLISP"
date: 2013-03-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Selection
description: "The wiki help introduces how to use this command in LISP. The following is a more code. It asks the user to select a 3D object, three pairs of poin..."
author: Autodesk
---
# Using the align command in AutoLISP

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/using-the-align-command-in-autolisp.html

## 文章内容

By Xiaodong Liang
The wiki help introduces how to use this command in LISP. The following is a more code. It asks the user to select a 3D object, three pairs of points and align the object with them.
(defun c:test1 ( / 3DOject)
(setq 3DObject (ssget))
(setq 3DObject (ssname 3DObject 0))
(if (= p1 nil)
 (progn
  (setq p1 (getpoint "select point pt1: "))
  (setq p2 (getpoint "select point pt2: "))
  (setq p3 (getpoint "select point pt3: "))
  (setq p4 (getpoint "select point pt4: "))
  (setq p5 (getpoint "select point pt5: "))
  (setq p6 (getpoint "select point pt6: "))
 )
)
(command "._align" 3DObject "" p1 p2 p3 p4 p5 p6)
(command "zoom" "e")
)

