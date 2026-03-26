---
title: "LISP﻿: (ssadd) returns nil if it encounters an error"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Selection
description: "In older versions of AutoCAD (prior to 2004), (ssadd) did not return nil upon error (i.e. if SEQEND was added to the selection set, (ssadd) still r..."
author: Autodesk
---
# LISP﻿: (ssadd) returns nil if it encounters an error

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/lisp-ssadd-returns-nil-if-it-encounters-an-error.html

## 文章内容

By Gopinath Taget
In older versions of AutoCAD (prior to 2004), (ssadd) did not return nil upon error (i.e. if SEQEND was added to the selection set, (ssadd) still returned the selection set).  Since AutoCAD 2004, (ssadd) returns nil for error (i.e. if SEQEND is added to the selection set, (ssadd) now returns nil):
(setq ss (ssadd na ss)) ; fails because (ssadd) returns nil for error.
Just doing (ssadd na ss) ; works because ss may be modified but is never set to nil. The 'nil' error return can be ignored.
You can code the routine without SETQing the return and it will work just fine:
(command "_.plinetype" 0)
(command "_.pline" "0,0" "5,5" "5,4" "12,5" "")
  (defun foo()
   (setq na (entlast))
   (setq ss (ssadd))
   (while na
      (ssadd na ss)
      (setq na (entnext na))
   )
   (princ "\n(sslength ss): ") (princ (sslength ss))(princ)
)
  This changed behavior resulted from fixing a known issue.  (ssadd) is a LISP "Special Form".  It modifies the second argument and returns a value.  It modifies the selection set passed as the second argument, and returns the modified selection set or nil as error.  Lisp users should develop the habit of using the side-effect of (ssadd) to check for success or failure, but *not* to redefine the selection set.

## 评论

**内容**: Andreas said...
Hi Gopinath,
we use AutoCAD 2013 64 Bit.
(ssadd (entlast) container)
worked fine in AutoCAD 2011 / 32 Bit
but fails in
AutoCAD 2013 64 Bit.
Do you know what is wrong or do you know an other way to collect selection sets.
Greetings
Andreas
Reply
06/04/2014 at 06:25 AM

---
