---
title: "Performance Issues When Copying/Arraying Text Entities in a Stamped OEM Application"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Block
  - OEM
  - Unicode
description: "You might find that when you create an array of a block reference with some preset attributes your Stamped OEM Application takes more time to array..."
author: Autodesk
---
# Performance Issues When Copying/Arraying Text Entities in a Stamped OEM Application

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/performance-issues-when-copyingarraying-text-entities-in-a-stamped-oem-application.html

## 文章内容

By Gopinath Taget
You might find that when you create an array of a block reference with some preset attributes your Stamped OEM Application takes more time to array the objects than AutoCAD or AOEM.EXE.
The most common reason for the difference in performance is the missing font file that the ATTDEF's text style is currently using. AutoCAD tries to search for the missing fonts (in the defined search paths) whenever Attribute Reference or TEXT entities are created, so that it can display them with the specified font. By default your Stamped OEM Application does not have the font files installed with it. So, the solution is to place the required font files in the font directory (or in the support directory) and modify the product's search path to include the font directory. This can be done while creating the Stamped OEM Application using the Make Wizard.
To test the effect of this on the performance of your application, try the following:
1) Add the following LISP code in aoem.lsp and compile the aoem.lsp.
2) Add the command "_arraytest" in the Make Wizard while creating your stamped application.
3) Invoke the Stamped OEM Application and open a drawing that has a block with a preset Attribute that references a font that is not installed.
4) Type the command "arraytest" and select the newly created block reference
(defun c:arraytest( / secEnd secStart)
(prompt "\nSelect a entity to array 100 X 100")
   (princ)
       (setq pss(ssget))
       (setq s (getvar "DATE"))
       (setq secStart(* 86400.0 (- s (fix s))))
       (setenv "MaxArray" (itoa (* 100 100)))
       (command "-array" pss "" "r" 100 100 100 100)
       (setq s (getvar "DATE"))
       (setq secEnd (* 86400.0 (- s (fix s))))
       (princ "\nTime taken :")
       (princ (- secEnd secStart))
       (princ)
)

