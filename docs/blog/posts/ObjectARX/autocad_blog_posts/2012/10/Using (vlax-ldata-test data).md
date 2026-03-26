---
title: "Using (vlax-ldata-test data)"
date: 2012-10-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Unicode
description: "How to use the (vlax-ldata-test data) Visual LISP function? The documentation refers to a "session boundary", what does it mean?"
author: Autodesk
---
# Using (vlax-ldata-test data)

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/using-vlax-ldata-test-data.html

## 文章内容

By Balaji Ramamoorthy
Issue
How to use the (vlax-ldata-test data) Visual LISP function? The documentation refers to a "session boundary", what does it mean?
Solution
The following sample shows how to use the session boundary, which means you can store and retrieve any kind of LISP data into and out of a dictionary or an object. It does not mean that it is possible to transfer among different AutoCAD instances using
vlax-ldata-xxxxx family functions.
In the following code, foo is a function and it is expressed as a list in LISP, so 'foo as the parameter will return True, otherwise, foo will return false. For fnm, a file descriptor that can be used by other I/O functions, it will change every time you open the same file and you can use it in a certain context. If you store it somewhere and want to use it in a different running context, it will fail. That is a clear image of session boundary.
(vl-load-com)

(setq lin (entmake '((0 . "LINE") (10 1 1 1) (11 20 20 20))))
(setq fnm (open "mmm.out" "W"))

(defun foo () (list 1 2 3))

;; True (T) for:
(vlax-ldata-test 1)
(vlax-ldata-test 'foo)
(vlax-ldata-test "A")
(vlax-ldata-test lin)
(vlax-ldata-test (list 1 "a" 'foo lin))

;; False (NIL) for:
(vlax-ldata-test foo)
(vlax-ldata-test fnm)
(vlax-ldata-test (list 1 "a" foo lin))
(vlax-ldata-test (cons 1 fnm))

