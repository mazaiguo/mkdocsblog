---
title: "AutoLISP example - create a Table (using ActiveX)"
date: 2012-04-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
description: "Here is a Visual Lisp example that uses the ActiveX interface to create a table:"
author: Autodesk
---
# AutoLISP example - create a Table (using ActiveX)

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/autolisp-example-create-a-table-using-activex.html

## 文章内容

Here is a Visual Lisp example that uses the ActiveX interface to create a table:
By Wayne Brill
  (defun c:addMyTable ( / ActiveDocument mSpace pt
              myTable nRows nCols row cell )
  (vl-load-com)
  (setq ActiveDocument (vla-get-activedocument
             (vlax-get-acad-object)))
  (setq mSpace(vla-get-modelspace ActiveDocument))
  (setq pt (vlax-make-safearray vlax-vbDouble
                                   '(0 . 2)))
  ;insertion point for the table
  (vlax-safearray-fill pt '(2.0 2.0 0.0))
  (setq myTable
     (vla-addtable mSpace pt 5 5 10 30))
  (vla-setcelltextheight myTable 0 0 5)
  (vla-settext myTable 0 0 "myTable")
 
  ;rows and columns zero based
  (setq nRows(- (vla-get-rows myTable) 1))
  (setq nCols(- (vla-get-columns myTable) 1))
 
  ; rows and columns after row 0, column 0
  (setq row 1)
  (setQ cell 0)
 
  ; loop through cells
  (while (<= row nRows)
    (while (<= cell nCols)
   (vla-setCelltextHeight myTable row cell 5.0)
        (vla-settext myTable row cell "test")
        ; make cell alignment middle center
        (vla-setCellAlignment myTable row cell 5)     
   (setq cell (1+ cell))
   );while
  (setq row (1+ row))
  (setq cell 0) 
);while
(princ)
);defun

## 评论

**内容**: Kahn said...
Hi Sir,
Thanks for you post. I'm learning how to create a table in AutoCAD by Autolip.
Could I ask you a question? How do I set the first row of the table without merge cell.
Thank you.
Reply
11/19/2014 at 04:38 PM

---
