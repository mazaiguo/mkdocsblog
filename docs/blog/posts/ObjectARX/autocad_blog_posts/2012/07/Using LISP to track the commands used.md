---
title: "Using LISP to track the commands used"
date: 2012-07-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
description: "I'm programming in LISP and now would like to track how many commands are being used within an AutoCAD session. How could I do it?"
author: Autodesk
---
# Using LISP to track the commands used

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/using-lisp-to-track-the-commands-used.html

## 文章内容

By Adam Nagy
I'm programming in LISP and now would like to track how many commands are being used within an AutoCAD session. How could I do it?
Solution
You can find samples about reactors in the LISP Help file, but here is the exact code you would need.
In this case we'll only track commands that actually ended, not including commands that got started and then cancelled - i.e. editor reactor’s commandEnded
When the document is closed we pop up a dialog showing how many commands were used in it since it got opened.
You would need to set up acaddoc.lsp so that it runs the following code for each opened document:
(defun editor-beginClose (reactor-object parameter-list /) 
  ; instead of an alert box write the data somewhere 
  (alert (strcat "Command count is " (itoa *command-count*))) 
) 

(defun editor-commandEnded (reactor-object parameter-list /) 
  (setq *command-count* (1+ *command-count*)) 
) 

(defun StartWatching (/) 
  ; we need the ActiveX system for this 
  (vl-load-com) 
  ; set the counter 
  (setq *command-count* 0) 
  ; start the event watcher 
  (vlr-editor-reactor nil '(
    (:vlr-beginClose . editor-beginClose)
    (:vlr-commandEnded . editor-commandEnded))
  ) 
  ; don't print anything to the screen 
  (princ) 
) 

; this should be started for each opened drawing 
(StartWatching)

