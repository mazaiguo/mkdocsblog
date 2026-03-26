---
title: "Renaming or copying an anonymous block using LISP or VBA"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Block
  - VBA
description: "How do I rename or copy an anonymous block to another name, such as TESTBLOCK?"
author: Autodesk
---
# Renaming or copying an anonymous block using LISP or VBA

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/renaming-or-copying-an-anonymous-block-using-lisp-or-vba.html

## 文章内容

By Fenton Webb
Issue
How do I rename or copy an anonymous block to another name, such as TESTBLOCK?
Solution
It is possible to rename an anonymous block. For example, you can rename a block named *T1 to TESTBLOCK. When listed, the available blocks in a drawing use commands such as BLOCK or INSERT. TESTBLOCK will not be listed because it is an
anonymous block (but it exists). Changing an anonymous block's name will not make it a named block. The group code 70 decides if the block is anonymous, and this group code cannot be edited.
For example, create an anonymous block "*T" using any_blk function, and then execute the ren_blk function to rename it to "TESTBLOCK".

(defun c:any_blk ()
 (vl-load-com)
 (setq a_app  (VLAX-GET-ACAD-OBJECT)
    a_doc  (vla-get-ActiveDocument a_app)
    a_blks (vla-get-blocks a_doc)
    blk    (vla-add a_blks (vlax-3d-point '(0 0 0)) "*T")
 )
 (vla-addcircle blk (vlax-3d-point '(0 0 0)) 3)
)

(defun c:ren_blk ()
 (vl-load-com)
 (setq a_app  (VLAX-GET-ACAD-OBJECT)
    a_doc  (vla-get-ActiveDocument a_app)
    a_blks (vla-get-blocks a_doc)
    blk    (vla-item a_blks "*T1")
)
 (vla-put-name blk "TESTBLOCK")
)
Now invoke command INSERT and you will find that TESTBLOCK is not listed, but you are allowed to type the blockname and then to insert it. The block TESTBLOCK is not listed as it is an anonymous block.
As a workaround, you could make a copy of the anonymous block instead of renaming it, as shown in the following sample code:

(defun c:cop_blk ()
 (vl-load-com)
 (setq a_app  (VLAX-GET-ACAD-OBJECT)
    a_doc  (vla-get-ActiveDocument a_app)
    a_blks (vla-get-blocks a_doc)
    i      0
 )
 (if (tblsearch "BLOCK" "*T1")
      (progn
     (setq blk (vla-item a_blks "*T1"))
     (setq inspt  (vla-get-origin blk)
           cnt    (- (vla-get-count blk) 1)
           newfil (vlax-make-safearray vlax-vbobject (cons 0 cnt))
     )
     (vlax-for ent    blk
         (vlax-safearray-put-element newfil i ent)
         (setq i (1+ i))
     )
     (if (null (tblsearch "BLOCK" "TESTBLOCK"))
          (setq newblk (vla-add a_blks inspt "TESTBLOCK"))
          (setq newblk (vla-add a_blks inspt "TESTBLOCKX"))
     )
     (vla-copyobjects a_doc newfil newblk nil)
      )
      (princ "\nBlock *T is not available. Unable to make a Copy.")
 )
 (princ)
)
Here is a sample VBA code to copy an anonymous block:

Sub copyblk()
   Dim objects() As Object
   Dim oldblk As AcadBlock
   Dim newblk As AcadBlock
   Dim inspt As Variant
   Dim obj As Object
   Dim i As Integer
   
   i = 0
   Set oldblk = ThisDrawing.Blocks.Item("*T1")  'Replace "*T1" with the
appropriate anonymous block name
   inspt = oldblk.Origin
   Cnt = oldblk.Count - 1
   ReDim objects(Cnt) As Object
   
   For Each obj In oldblk
    Set objects(i) = obj
    i = i + 1
   Next obj
   
   Set newblk = ThisDrawing.Blocks.Add(inspt, "NEWTEST")
   ThisDrawing.CopyObjects objects, newblk
End Sub

## 评论

**内容**: Aleksei Kulik aka kpblc said...
Did you test your code? It won't works.
First of all, *T-named blocks used to define TABLE objects (and 'cos of this it's not good idea to use this name template). Secondary, vla-put-name function won't rename anonymous block (it won't rename it at AutoCAD 2006, 2007, 2008 and up to 2014).
Reply
04/03/2013 at 11:57 AM

---
**内容**: hh hhh said in reply to Aleksei Kulik aka kpblc...
You're right!!!!
Reply
02/26/2015 at 08:25 PM

---
**内容**: Aleksei Kulik aka kpblc said...
Only code used CopeObjects method works correctly.
Reply
04/03/2013 at 12:10 PM

---
**内容**: giuseppe said...
Salve ho un blocco presumo che lo sia con un *davanti esempio *u977 provo a modificarlo ma non me lo fa modificare e nemmeno esplodere poiché mi compare la scritta " è inserito in una serie rettangolare"
come posso fare affinché lo possa modificare?
Reply
05/27/2024 at 03:10 AM

---
