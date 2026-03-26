---
title: "SelectByPolygon outputs <cr> on commandline"
date: 2012-07-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Selection
description: "I have noticed that each time SelectByPolygon is used via VB AutoCAD gets a <CR> on the command line and things on the command line disappear off i..."
author: Autodesk
---
# SelectByPolygon outputs <cr> on commandline

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/selectbypolygon-outputs-on-commandline.html

## 文章内容

By Philippe Leefsma
Q:
I have noticed that each time SelectByPolygon is used via VB AutoCAD gets a <CR> on the command line and things on the command line disappear off into the history buffer which is very odd to see happening.
A:
There isn’t a mean to stop this behavior at this time and this behavior is logged for a change request 511115.
LISP functions like the one below using SSGET do not exhibit this behavior.

(defun c:wbtest ()
(setq pt_list '((1 1)(40 1)(40 40)(1 40)))
(setq sset (ssget "_CP" pt_list))
  (setq ilast (sslength sset)) 
)

