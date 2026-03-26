---
title: "Call LISP function based on its name"
date: 2012-07-01
categories:
  - AutoLISP
tags:
  - AutoLISP
description: "I have a variable which contains the name of a LISP function, but I do not know how to use that in order to call the function."
author: Autodesk
---
# Call LISP function based on its name

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/call-lisp-function-based-on-its-name.html

## 文章内容

By Adam Nagy
I have a variable which contains the name of a LISP function, but I do not know how to use that in order to call the function.
Solution
You can use (read) to get the function from the name then (mapcar) or (apply) to invoke it. Here are two functions that we will be calling knowing their names. One has an input parameter, the other one does not.
(defun myfunc1 ( / )
  (alert "myfunc1 called")
)

(defun c:callmyfunc1 ( / funcname)
  (setq funcname "myfunc1")
  (apply
    (read funcname)
    nil
  )
)

(defun myfunc2 (param / )
  (alert (strcat "myfunc2 called with param=" param))
)

(defun c:callmyfunc2 ( / funcname)
 (setq funcname "myfunc2")
  (apply
    (read funcname)
    '("testparam")
  )
)

