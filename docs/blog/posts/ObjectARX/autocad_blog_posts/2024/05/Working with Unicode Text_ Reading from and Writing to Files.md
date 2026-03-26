---
title: "Working with Unicode Text: Reading from and Writing to Files"
date: 2024-05-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Unicode
description: "Before AutoCAD 2021, AutoLisp/VLisp was not fully Unicode compliant."
author: Autodesk
---
# Working with Unicode Text: Reading from and Writing to Files

发布日期: 2024-05-01

原始链接: https://adndevblog.typepad.com/autocad/2024/05/working-with-unicode-text-reading-from-and-writing-to-files.html

## 文章内容

By Madhukar Moogala
Before AutoCAD 2021, AutoLisp/VLisp was not fully Unicode compliant.
AutoCAD 2021 introduced a new system variable, LISPSYS, which fully supports AutoLisp functions with Unicode characters.
Here's how to read a text file with Unicode characters and create an MTEXT entity with the parsed contents:
Sample text file with Unicode characters:
    こんにちは、良い一日を

The following AutoLisp code reads the text file and creates an MTEXT entity

```lisp
  (defun c:drawtext()
   (setq f (open "d:/temp/r.txt" "r" "utf8"))
   (setq mytext (read-line f))
   (setq mypoint (list 1.0 1.0 0.0)
         myotherpoint (list -0.5 2.0 0.0)
         mycolor "2" ; red
         myrot 90.0
         currcolor (getvar "CECOLOR")
   )
   (setvar "CECOLOR" mycolor)
   (command "mtext" mypoint "R" myrot "@" mytext "")
   (setvar "CECOLOR" currcolor)
   (close f)
  )
```
Note:We use utf8encoding, which tells AutoLISP to open a Unicode stream for reading and writing.
Now, similarly, we can write the Unicode contents of an MTEXT entity to a file:
```lisp
  (defun c:writetext()
  (setq f (open "d:/temp/w.txt" "w" "utf8"))
  (setq txt (vla-get-textstring (vlax-ename->vla-object (car (entsel "Pick mtext")))))
  (write-line txt f)
  (close f)
  )

```

Here's the result:

