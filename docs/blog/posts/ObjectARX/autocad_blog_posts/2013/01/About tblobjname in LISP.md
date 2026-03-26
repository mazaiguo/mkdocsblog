---
title: "About tblobjname in LISP"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoLISP
  - Block
  - C++
  - COM
  - ObjectARX
description: "Different handles are returned by (tblobjname "block" "") and (vlas-invoke-method blocks "item" ""), which is rooted in their history."
author: Autodesk
---
# About tblobjname in LISP

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/about-tblobjname-in-lisp.html

## 文章内容

By Augusto Goncalves
Different handles are returned by (tblobjname "block" "") and (vlas-invoke-method blocks "item" ""), which is rooted in their history.
 
(tblobjname) returns the block's "BLOCK" entity, also known as the AcDbBlockBegin object, which rooted in history (i.e. something only existing LISP code could rationalize). This is what (tblsearch "block" ")) used to return elements of.
 
(vlax-invoke-method blocks "item" "") returns the object Id of the actual Block Table Record, which is generally of greater interest to "modern code". ObjectARX and ActiveX applications should have no (or little) use for AcDbBlockBegin and AcDbBlockEnd entities, they exist only for compatibility reasons.
This code can be used to get to the block object:
(defun c:getToBlock (/ acadApp acadDoc acadBlocks myBlock myBlockHandle)
  (if (and (setq e1 (entsel "\nSelect Block Reference: "))
    (= (cdr (assoc 0 (entget (car e1)))) "INSERT"))
    (progn
      (vl-load-com)
      (Setq acadApp (vlax-get-acad-object)
        acadDoc (vla-get-ActiveDocument acadApp) 
        acadBlocks  (vlax-get-property acadDoc "blocks")
        myBlock (vlax-invoke-method acadBlocks "item" 
           (cdr (assoc 2 (entget (car e1)))))
        myBlockHandle (vlax-get-property myBlock "handle"))
      (print myBlock)
    )
  )
  (princ)
)

