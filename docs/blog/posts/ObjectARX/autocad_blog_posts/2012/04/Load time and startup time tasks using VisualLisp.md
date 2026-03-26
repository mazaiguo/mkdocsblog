---
title: "Load time and startup time tasks using VisualLisp"
date: 2012-04-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
description: "There is an easy way to setup your Lisp functions to run when any drawing is opened in AutoCAD."
author: Autodesk
---
# Load time and startup time tasks using VisualLisp

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/load-time-and-startup-time-tasks-using-visuallisp.html

## 文章内容

By Balaji Ramamoorthy
There is an easy way to setup your Lisp functions to run when any drawing is opened in AutoCAD.
Before we get to the details, lets me explain what I will be referring to as the "load time" and "startup time" in this post.
When a drawing is opened in AutoCAD, while it is still being loaded you may be interested in running your lisp function. I refer to this as the "load time".
Just after the drawing is fully opened, you may be interested in running your lisp function. I refer to this as the "startup time"
AutoCAD loads the "acaddoc.lsp" when a drawing is opened. If this file does not exist, then just create it and ensure that it is in one of the support paths configured in AutoCAD. This lsp file will be automatically loaded by AutoCAD for each drawing that is opened.
Here is a sample code that you can copy and paste at the end of your "acaddoc.lsp" :
(defun load-time-operations ()
(princ "\nThis executes at load time. Before s::startup.")
(princ "\nMy load time tasks...")
)
  ; Ensure that load-time-operations gets a call
(load-time-operations)
  (defun s::startup ()
(princ "\nDocument is opened and AutoCAD is now ready.")
(princ "\nMy Startup tasks...")
)
Save the acaddoc.lsp and start AutoCAD and open a drawing. You can find the load time and startup messages displayed.
If your Lisp code is big and you do not want to add all the code to the acaddoc.lsp, you may also load your lsp file using the "(load "C:\\Test\\MyFuncs.lsp")"
Thanks to Owen Wengerd for highlighting this important point.
AutoCAD provides the acadXXXXdoc.lsp (For ex : acad2012doc.lsp) that gets loaded even before the acaddoc.lsp for every drawing that is opened. Inserting your lisp code in this file will also work but is definitely not recommended because this file is reserved for use by AutoCAD. Instead you will need to create the acaddoc.lsp file if it does not already exist.

## 评论

**内容**: Owen Wengerd said...
Please don't tell developers or end users to modify the acadXXXXdoc.lsp file, as that file belongs to AutoCAD. End users should create and use acaddoc.lsp for this purpose, and developers should use the registry demand load mechanism to load their applications.
Reply
04/18/2012 at 05:40 PM

---
**内容**: Balaji said...
Thanks Owen,
I have updated the blog post.
Reply
04/18/2012 at 10:50 PM

---
