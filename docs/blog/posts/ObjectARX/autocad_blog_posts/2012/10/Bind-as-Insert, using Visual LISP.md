---
title: "Bind-as-Insert, using Visual LISP"
date: 2012-10-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Block
  - XREF
description: "To perform a bind-as-insert of an Xref, using Visual LISP, here is a sample code."
author: Autodesk
---
# Bind-as-Insert, using Visual LISP

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/bind-as-insert-using-visual-lisp.html

## 文章内容

By Balaji Ramamoorthy
To perform a bind-as-insert of an Xref, using Visual LISP, here is a sample code.
By setting the BINDTYPE system variable to 1, a bind-as-insert is performed:
(setvar "BINDTYPE" 1)
(command "_-xref" "_bind" "MYBLOCK")
(setvar "BINDTYPE" 0)
Using Visual Lisp, the following code will accomplish the same task.
(defun c:BindInsert ( / appAcad docActive colBlocks objBlk)
   (vl-load-com) ;load ActiveX
   (setq appAcad (vlax-get-acad-object)
         docActive (vla-get-ActiveDocument appAcad)
   ) ;setq
   ;;get the blocks collection
   (setq colBlocks (vla-get-blocks docActive))
   (vlax-for objBlk colBlocks
      ;;Is the block an xref?
      (if (= (vlax-get-property objBlk 'IsXref) :vlax-true)
         ;;if True, then bind it as an insert
         (vlax-invoke-method objBlk "bind" :vlax-true)
      ) ;if
      (vlax-release-object objBlk)
   ) ;vlax-for
   ;;release objects from memory
   (vlax-release-object colBlocks)
   (vlax-release-object docActive)
)

## 评论

**内容**: Alvaro Leon said...
Excelent!
Reply
11/01/2012 at 06:54 AM

---
**内容**: Marcelo said...
Hi!
This routine is very good! Could you modify a little to have the BINDTYPE set to 0 instead to 1?
Thanks!
Marcelo
Reply
03/04/2015 at 11:03 AM

---
