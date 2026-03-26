---
title: "Append fails with multiple defined s:startup functions"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - CUI
  - Migration
description: "I have followed the documentation in the Migration Assistance and the Customization Guide. My code also works in previous versions of AutoCAD. Why ..."
author: Autodesk
---
# Append fails with multiple defined s:startup functions

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/append-fails-with-multiple-defined-sstartup-functions.html

## 文章内容

By Xiaodong Liang
Issue
I have followed the documentation in the Migration Assistance and the Customization Guide. My code also works in previous versions of AutoCAD. Why does the following code fail?
(defun MYSTARTUP ()
  (if (not (equal (menugroup "MYGROUP") "MYGROUP")) (command "MENULOAD"
"MYMENU") )
)
(setq S::STARTUP (append S::STARTUP MYSTARTUP))
With this error:
; error: Invalid attempt to access a compiled function definition.  You may 
want to define it using defun-q: #
Solution
As the error indicates, you most likely have a S::STARTUP function already defined using defun in another file. If you have third party programs installed on your system, there can easily be more than one instance of the S:STARTUP function definitions. If this is the case, you will need to either find all instances of startup functions and ensure that they are defined with defun-q in order to use the append function with them, or you can use the AutoLISP code that follows: If you do not know how S::STARTUP is defun'd, then this additional code placed in your ACADDOC.LSP file (along with your MYSTARTUP function) will work for either type of S::STARTUP function, such as SUBR or LIST:
(defun new-startup-func (afoo-arg)

 (eval
   (list 'defun 's::startup '()
;; If S::STARTUP exists call S::STARTUP by SUBR ID
     (if s::startup               
      (list (list 'quote s::startup))
     )                     
;; if user SUBR, add it here to new S::STARTUP defun
     (if afoo-arg             
      (list (list 'quote (eval afoo-arg)))
     )
   )
 )
)

(new-startup-func 'MYSTARTUP)

