---
title: "Using NOMUTT variable to stop "Command: " Prompt between vla-getXXX methods"
date: 2012-07-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
description: "You may want to suppress the echo of the "Command: " prompt after subsequent calls to any of the 'Getxxxxxx' methods using ActiveX. For this the NO..."
author: Autodesk
---
# Using NOMUTT variable to stop "Command: " Prompt between vla-getXXX methods

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/using-nomutt-variable-to-stop-command-prompt-between-vla-getxxx-methods.html

## 文章内容

By Balaji Ramamoorthy
You may want to suppress the echo of the "Command: " prompt after subsequent calls to any of the 'Getxxxxxx' methods using ActiveX. For this the NOMUTT system variable along with extra Prompts as shown in the following sample lisp code can be used to stop the Command prompt from appearing after each vla-getXXX method.
(defun c:test (/ doc p1 p2 uo)
  (vl-load-com)
  (setq doc (vla-get-ActiveDocument (vlax-get-acad-object))
          msp (vla-get-modelspace doc)
            uo  (vla-get-utility doc)
  )

  (prompt "\nStart point:")
  (setvar "nomutt" 1)
  (vla-InitializeUserInput uo 9)
  (setq p1 (vla-getPoint uo nil))

  (setvar "nomutt" 0)
  (prompt "\nEnd point:")
  (setvar "nomutt" 1)
  (vla-InitializeUserInput uo 9)
  (setq p2 (vla-getPoint uo p1))

  (vla-addLine msp p1 p2)
  (setvar "nomutt" 0)
  (princ)
)

