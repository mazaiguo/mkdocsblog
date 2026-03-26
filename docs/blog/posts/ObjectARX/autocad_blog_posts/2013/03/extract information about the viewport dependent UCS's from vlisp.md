---
title: "extract information about the viewport dependent UCS's from vlisp"
date: 2013-03-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - UCS
description: "When I use the following code in a drawing that has several model space  viewports where each viewport has a different UCS, the name of the UCS tha..."
author: Autodesk
---
# extract information about the viewport dependent UCS's from vlisp

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/extract-information-about-the-viewport-dependent-ucss-from-vlisp.html

## 文章内容

By Xiaodong Liang
Issue
When I use the following code in a drawing that has several model space  viewports where each viewport has a different UCS, the name of the UCS that was set in the active viewport at the time the function was invoked always displays. How can I get information about the viewport-dependent UCS's using Visual LISP?
(defun c:vp_ucs (/)
 (foreach elem (vports)
   (setvar "cvport" (car elem))
   (princ "\n")
   (princ (getvar "UCSNAME"))
 )
)
Solution
This is a known problem.You can work around this by using the following ActiveX functions in Visual LISP as shown in the following sample code. To run it, make sure the drawing have some named UCS and the view ports apply the UCS.
(defun c:Test ()
 (vl-load-com) ;Enable ActiveX functions
 (setq a_app (VLAX-GET-ACAD-OBJECT) ;Pointer to Acad Application
    a_doc (VLA-GET-ACTIVEDOCUMENT a_app) ;Pointer to ActiveDocument
    oldvar (getvar "cmdecho")
 )
(setvar "cmdecho" 0)
;Iterate through the various viewports by setting them active and then extracting the UCS name.
 (foreach itm (vports)
   (setvar "CVPORT" (car itm))
   (command ".redraw") ;Force a command interaction with acad application to obtain the UCSNAME
   (setq oUCS (vla-get-activeucs a_doc))
   (print (vla-get-name oUCS))
 )
(setvar "cmdecho" oldvar) ;reset cmdecho setvar back to its original state
(princ)
)

