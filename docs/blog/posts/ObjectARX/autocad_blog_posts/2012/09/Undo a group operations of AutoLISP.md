---
title: "Undo a group operations of AutoLISP"
date: 2012-09-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
description: "My menu item uses AutoLISP code to call two AutoCAD commands.  Why does the UNDO command only undo the last of the two commands?"
author: Autodesk
---
# Undo a group operations of AutoLISP

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/undo-a-group-operations-of-autolisp.html

## 文章内容

By Xiaodong Liang
Issue
My menu item uses AutoLISP code to call two AutoCAD commands.  Why does the UNDO command only undo the last of the two commands?
Solution
If all you are executing with a menu item is series of multiple commands as in:
[Draw Many]^c^cLINE 0,0,0 10,10,0 ;CIRCLE 5,5 5;
Then when you type U at the command line, both items will be undone.However, if you are doing the following via a menu item and AutoLISP code:

(defun testCmd ()
   (command "LINE" "0,0,0" "10,10,0" "")
   (command "CIRCLE" "5,5" 5)
   (princ)
) 
[Draw Many w/Lisp]^c^c(testCmd);
The U only erases the circle.
The solution is to code your AutoLISP function like so:
(defun testCmd ()
   (command "UNDO" "BE")
   (command "LINE" "0,0,0" "10,10,0" "")
   (command "CIRCLE" "5,5" 5)
   (command "UNDO" "END")
   (princ)
)

