---
title: "Removing an embedded VBA macro programmatically using Lisp"
date: 2012-06-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - DWG
  - VBA
description: "You can embed VBA macros in a DWG file and in some situations, you might feel the need to get rid of the embedded macros."
author: Autodesk
---
# Removing an embedded VBA macro programmatically using Lisp

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/removing-an-embedded-vba-macro-programmatically-using-lisp.html

## 文章内容

By Gopinath Taget
You can embed VBA macros in a DWG file and in some situations, you might feel the need to get rid of the embedded macros.
If so, the following lisp routine will help you remove the embedded macro:
(defun removeEmbedMacro()
  (entdel (cdr(car (dictsearch (namedobjdict) "ACAD_VBA"))))
  )
In this lisp routine, we remove the dictionary item “ACAD_VBA” in the Named Object Dictionary. This is because embedded macros live under the ACAD_VBA dictionary item.

