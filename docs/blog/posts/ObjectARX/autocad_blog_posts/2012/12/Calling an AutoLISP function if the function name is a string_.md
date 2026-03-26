---
title: "Calling an AutoLISP function if the function name is a string?"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoLISP
description: "This can be achieved by using (eval (list (read "string"))). Here is some sample code:"
author: Autodesk
---
# Calling an AutoLISP function if the function name is a string?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/calling-an-autolisp-function-if-the-function-name-is-a-string.html

## 文章内容

By Gopinath Taget
This can be achieved by using (eval (list (read "string"))). Here is some sample code:
(defun adts_function ()
   (princ "\nDeveloper Technical Services")
   (princ)
)
(defun c:test ()
   (setq fname "adts_function")
   (eval (list (read fname)))
  
)
(prompt "\nCommand c:test defined")
(princ)

