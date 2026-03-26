---
title: "Command line version of my command"
date: 2012-07-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Plot
  - Unicode
description: "I have a command written in LISP that gets some information from the user through a dialog and now I would like to create a command line version of..."
author: Autodesk
---
# Command line version of my command

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/command-line-version-of-my-command.html

## 文章内容

By Adam Nagy
I have a command written in LISP that gets some information from the user through a dialog and now I would like to create a command line version of it that could also be called from a script. So I have MYCOMMAND and I would like to create -MYCOMMAND. How can I do it?
Solution
You just have to prefix your command name with a dash '-' and only use command line input methods like getstring, etc.
; the function itself
(defun myprint_func (mytext / )
  (print mytext)
)

; the user interface version of the command
(defun c:myprint ( / mytext)
  ; use user interface (e.g. DCL dialog) to set mytext
  ; ...
  (myprint_func mytext)
  (princ)
)

; the command line version of the command
(defun c:-myprint ( / mytext)
  ; use command line input functions to set mytext
  (setq mytext (getstring "\nProvide text: "))

  (myprint_func mytext)

  (princ)
)

