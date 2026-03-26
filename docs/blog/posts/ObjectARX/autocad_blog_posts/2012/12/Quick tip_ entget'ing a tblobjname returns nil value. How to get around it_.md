---
title: "Quick tip: entget'ing a tblobjname returns nil value. How to get around it?"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Block
  - Dimension
  - Plot
description: "Why is the return value of the (entget) function nil after updating dimension entities?"
author: Autodesk
---
# Quick tip: entget'ing a tblobjname returns nil value. How to get around it?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/quick-tip-entgeting-a-tblobjname-returns-nil-value-how-to-get-around-it.html

## 文章内容

By Gopinath Taget
Why is the return value of the (entget) function nil after updating dimension entities?
This happens because of a known problem with tlbobjname lisp function. Consider the following code:
(setq ent (entget (tblobjname "block" "*D1"))
        det (entget (cdr (assoc -2 ent)))
)
(print det)
At the command prompt type the following:
Command: Dim
Dim: upd
Select objects: all
Select objects:
Now execute the above lisp code again and you will notice a nil return value.  This is due to the known problem with 'tblobjname' function.  The workaround is to use 'tblsearch' instead:
(setq ent (tblsearch "block"  "*D1")
        det (entget (cdr (assoc -2 ent)))
)
(print det)

