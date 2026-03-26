---
title: "How to add a group in a selection set from an AutoLISP function?"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Selection
description: "The following code selects all the entities contained in a group."
author: Autodesk
---
# How to add a group in a selection set from an AutoLISP function?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-add-a-group-in-a-selection-set-from-an-autolisp-function.html

## 文章内容

By Gopinath Taget
The following code selects all the entities contained in a group.
(defun selgrp (grpname)
   ;; grpname is the group name, it accepts
   ;; unnamed groupnames, such as *A1
   (setq grp (dictsearch (namedobjdict) "ACAD_GROUP"))
   (setq a1 (dictsearch (cdr (assoc -1 grp)) grpname))
   (setq ss (ssadd))
   (while (/= (assoc 340 a1) nil)
      (setq ent (assoc 340 a1))
      (setq ss (ssadd (cdr ent) ss))
      (setq a1 (subst (cons 0 "") ent a1))
   )
   ss
)

## 评论

**内容**: Rainbow Friends said...
Ok, thanks for the information and have a good day
Reply
08/03/2023 at 02:27 AM

---
