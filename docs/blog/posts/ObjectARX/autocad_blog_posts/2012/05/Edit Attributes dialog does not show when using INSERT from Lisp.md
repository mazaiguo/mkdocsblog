---
title: "Edit Attributes dialog does not show when using INSERT from Lisp"
date: 2012-05-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Block
description: "I have the following Lisp code and it used to work fine - i.e. it showed the Edit Attributes dialog when a block with attributes was being inserted."
author: Autodesk
---
# Edit Attributes dialog does not show when using INSERT from Lisp

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/edit-attributes-dialog-does-not-show-when-using-insert-from-lisp.html

## 文章内容

By Wayne Brill
Issue
I have the following Lisp code and it used to work fine - i.e. it showed the Edit Attributes dialog when a block with attributes was being inserted.
(defun c:myinsert ( / )
  (setvar "ATTREQ" 1)
  (setvar "ATTDIA" 1)
  (initdia)
  (command "-insert" "MyBlock" "0,0" 1 1 0.0)  
)
However, in AutoCAD 2012 the functionality seems broken as only the command line version of Edit Attributes is available.
How could I make the Edit Attributes dialog appear?
Solution
This behavior has been reported and hopefully the fix will be available in the first service pack of AutoCAD 2012.
You may find the following workaround acceptable in the meantime:
(defun c:myinsert ( / attreq  )
  (setq attreq  (getvar "ATTREQ"))
  (setvar "ATTREQ" 0)
  (command "_.-insert" "myblock" "0,0" 1 1 0)
  (setvar "ATTREQ" attreq)
  (if (= attreq 1)
      (command "_ddatte" (entlast))
  )
)

