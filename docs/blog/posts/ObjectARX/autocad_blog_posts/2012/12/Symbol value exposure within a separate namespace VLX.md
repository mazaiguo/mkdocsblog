---
title: "Symbol value exposure within a separate namespace VLX"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Plot
description: "I compiled the following AutoLISP code as a separate namespace VLX, and the value of symbol 'hugo' (setq hugo 12345), in my current drawing is not ..."
author: Autodesk
---
# Symbol value exposure within a separate namespace VLX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/symbol-value-exposure-within-a-separate-namespace-vlx.html

## 文章内容

By Xiaodong Liang
Issue
I compiled the following AutoLISP code as a separate namespace VLX, and the value of symbol 'hugo' (setq hugo 12345), in my current drawing is not available to my VLX. Why ?
(defun C:DUMMY ( / )    
   (print "\n DUMMY:")
   (print hugo)
   (print "\n DUMMY.")    
)
Solution
The VLX namespace is not contained in the document namespace. For a thorough discussion of namespaces, refer to the following sections in the Visual LISP Developer's Guide:
Creating a New Application
Designing for a Multiple Document Environment
Referencing Variables in Document Namespaces
VLX Namespace Functions
Visual LISP contains two functions that allow a separate namespace to VLX to access, and sets values for AutoLISP symbols that are defined in the current document:
(vl-doc-set), (vl-doc-ref)
So if you code your lisp as follows:

(defun C:SMART ( / hugo vlxhugo)    
   (princ "\n Smart: \n")
   (setq vlxhugo (vl-doc-ref 'hugo))
   (if hugo 
      (progn (princ "\nVariable hugo = ") (princ hugo))
      (princ "\nVariable hugo is not defined in VLX!\n")
   )
   (if vlxhugo 
      (progn (princ "\nVariable VLXhugo = ") (princ vlxhugo))
      (princ "\nVariable VLXhugo is not defined in VLX!\n")
   )
   (princ "\n Smart. \n")
   (vl-doc-set 'hugo "A New Value")
   (princ)  
)
Then compile it as a separate namespace VLX, then (setq hugo 12345) in your current document, and run the SMART function. The function will report the current vale of 'hugo', and reset it from within the separate namespace VLX.

