---
title: "Visual LISP example for Controlling Drawing Properties with vla-SetCustomByIndex and similar methods"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoLISP
description: "I need a Visual Lisp example for SetCustomByIndex, SetCustomByKey, GetCustomByIndex and GetCustomByKey."
author: Autodesk
---
# Visual LISP example for Controlling Drawing Properties with vla-SetCustomByIndex and similar methods

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/visual-lisp-example-for-controlling-drawing-properties-with-vla-setcustombyindex-and-similar-methods.html

## 文章内容

By Philippe Leefsma
Q:
I need a Visual Lisp example for SetCustomByIndex, SetCustomByKey, GetCustomByIndex and GetCustomByKey.
A:
Here is an example that adds a custom drawing property. It then changes and gets the values:
(defun c:dProps2 (/ dProps dProp)
   (vl-load-com)
   (setq acadObject (vlax-get-acad-object))
   (setq acadDocument (vla-get-ActiveDocument acadObject))
   ;;Get the SummaryInfo
   (setq dProps (vlax-get-Property acadDocument 'SummaryInfo))
   ; comment this vla-addCustomInfo if the entries already exist in
   ; the drawing properties, (which they will after running this one time)
  (vla-AddCustomInfo dProps "wbKey" "wbValue")
  
  (vla-SetCustomByIndex dProps 0 "wbKey" "wbValue2")
  (vla-setCustomByKey dProps "wbKey" "wbValue3")
  (vla-getCustomByKey dProps "wbKey" 'myValue)
  (vla-getCustomByIndex dProps 0 'myValue1 'myValue2)
  (princ (strcat "wbKey value = " myValue "\n"))
  (princ (strcat "Name = " myValue1 "\n"))
  (princ (strcat "Value = " myValue2 "\n"))
  (princ) 
)

