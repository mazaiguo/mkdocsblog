---
title: "AutoCAD Lisp: Why does (rtos 8.6375 2 3) return 8.637 instead of 8.638 as expected?"
date: 2012-08-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
description: "Why does (rtos 8.6375 2 3) return 8.637 instead of 8.638 as expected? How can I correct it?"
author: Autodesk
---
# AutoCAD Lisp: Why does (rtos 8.6375 2 3) return 8.637 instead of 8.638 as expected?

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/autocad-lisp-why-does-rtos-86375-2-3-return-8637-instead-of-8638-as-expected.html

## 文章内容

By Philippe Leefsma
Q:
Why does (rtos 8.6375 2 3) return 8.637 instead of 8.638 as expected? How can I correct it?
A:
This is a known issue in AutoCAD and AutoLISP. However, it is more of a precision issue of computers than a bug of AutoCAD.
There is always a certain degree of inaccuracy when calculating values. This is the case in other programming languages as well. To demonstrate this, we will compare the numbers 8.6375 and 7.6375. Observe the following output in the AutoCAD command window:
Command: (rtos 7.6375 2 3)
"7.638"
Command: (rtos 7.6375 2 16)
"7.6375"
Command: (rtos 8.6375 2 3)
"8.637"
Command: (rtos 8.6375 2 16)
"8.637499999999999"
It may be surprising that the number 8.6375 is represented as 8.637499999999999 above.  The computer represents this value as a binary number (a series of 0s and 1s).  It must perform transformations or calculations for all other numbers (especially for decimals), thus causing the precision issue.
This is taken into account by the workaround below, which substitutes (bzh_rtos ) for the original (rtos ) function.  The comments help to explain the process:

(defun Bzh_rtos
   (num mod pre / A B len dec1 dec2 dec22 small_value real_num)
   (setq A (rtos num mod pre))  ;A contains the value (rtos) returns
   (setq B (rtos num mod (+ 1 pre))) 
   (setq real_num num)
   (setq len   (strlen A)  ;Length of A string
           dec1  (substr A len 1);The last decimal of A
           dec2  (substr B len 1);The next to the last decimal of B
           dec22 (substr B (+ len 1) 1);The last decimal of B
   )
   ;;Set a fuzz factor. We can change it to other value as we like.
   (setq small_value (expt 0.1 (+ 1 14)))
   ;;Check if dec1 equals to dec2
   (if (= dec1 dec2)
      (if (= dec22 "5")
         (setq real_num (+ real_num small_value))
      )
   )
   ;;Recaculate the adjusted number and return
   (rtos real_num mod pre)
)

