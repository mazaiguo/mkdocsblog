---
title: "Using DIMPOST in a Lisp routine"
date: 2014-03-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Dimension
description: "I'm trying to change DIMPOST to \X in a lisp routine. The program will not accept \X in a lsp program. I'm want to change Dimstyle using the set up..."
author: Autodesk
---
# Using DIMPOST in a Lisp routine

发布日期: 2014-03-01

原始链接: https://adndevblog.typepad.com/autocad/2014/03/using-dimpost-in-a-lisp-routine.html

## 文章内容

By Xiaodong Liang
Question
I'm trying to change DIMPOST to \X in a lisp routine. The program will not accept \X in a lsp program. I'm want to change Dimstyle using the set up; Method set to NONE for both primary(Metric) and alternate units(English) and alternate unit placement under the primary units. I can do this manually but not in the lisp.
Solution
With these Lisp statements, the dimension formatting were as requested by the developer :
<<<
; To reset the alternative dimension prefix and suffix
(command-s "DIMAPOST" ".")
; To reset the primary dimension prefix and suffix
(command-s "DIMPOST" ".")
; To set the orientation of the alternative dimension over the primary dimension
(setvar "DIMPOST" "\\X")
>>>

