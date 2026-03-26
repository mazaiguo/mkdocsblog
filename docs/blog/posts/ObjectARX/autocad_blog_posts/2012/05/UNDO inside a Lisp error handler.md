---
title: "UNDO inside a Lisp error handler"
date: 2012-05-01
categories:
  - AutoLISP
tags:
  - AutoLISP
description: "If you want to call the UNDO command from an error handler then instead of using (command) you need to use (vla-SendCommand)"
author: Autodesk
---
# UNDO inside a Lisp error handler

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/undo-inside-a-lisp-error-handler.html

## 文章内容

By Adam Nagy
If you want to call the UNDO command from an error handler then instead of using (command) you need to use (vla-SendCommand)
(defun C:test ()
   (setq olderr *error*
     *error* myerr)
   (command "_undo" "_m")
   (command "_line" '(0 0 0) '(10 10 0) "")
   ; If you press esc when line is asking for the second point
   ; then myerr will be called by the system
   (command "_line" '(0 0 0) "\\" "")
   (setq *error* olderr)
)

(defun myerr (msg)
   (vl-load-com)
   (setq *error* olderr)

   ; Instead of using (command) ...
   ; (command "_undo" "b")
   ; use vla-SendCommand:
   (vla-SendCommand
     (vla-get-ActiveDocument
       (vlax-get-acad-object))
         (strcat (chr 27)(chr 27)"_.undo _b "))

   (princ)
)

## 评论

**内容**: GT said...
I'm assuming the reason is that there might be a command active?
I was using the following to get around that issue:
(if (= 0 (getvar "cmdactive")) (command "undo" "1" "regen"))
With my method the command line is clean when CMDECHO is 0. With vla-SendCommand I'm not sure if there is a way to suppress all the command line echoing.
Reply
05/18/2012 at 03:53 PM

---
