---
title: "How to detect if a toolbar has been loaded using VLISP?"
date: 2012-07-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
  - VBA
description: "Using VLisp, to detect if a toolbar has been loaded, we can use ActiveX methods to do the work, just like VBA does. The following code can achieve ..."
author: Autodesk
---
# How to detect if a toolbar has been loaded using VLISP?

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/how-to-detect-if-a-toolbar-has-been-loaded-using-vlisp.html

## 文章内容

By Balaji Ramamoorthy
Using VLisp, to detect if a toolbar has been loaded, we can use ActiveX methods to do the work, just like VBA does. The following code can achieve the task:
;;; Detect if the "Web" toolbar is loaded
(defun c:detectToolbar (/ acadapp menuGroups menuGroup0 toolbars)
   ;; Load COM support
   (if (car (atoms-family 1 '("vl-load-com")))
      (vl-load-com)
   )

   ;; Get AutoCAD application, the ACAD menuGroup and toolbars
   (setq acadapp    (vlax-get-acad-object)
           menuGroups (vla-get-menugroups acadapp)
           menuGroup0 (vla-item menuGroups "ACAD")
           toolbars   (vla-get-toolbars menuGroup0)
   )

   (vlax-for eachTB toolbars
      (setq nameTB (vla-get-name eachTB))
      (if (= nameTB "Web")
         (princ "\n Web toolbar has been loaded.")
      )
   )

   (princ)
)
This example determines if a menugroup named "BatchPublish" has been loaded:
(defun c:chkmenu (/ menuGroups eachMG nameMG)
(if (car (atoms-family 1 '("vl-load-com")))
      (vl-load-com)
   )

   ;; Get AutoCAD application, and menuGroups
   (setq acadapp    (vlax-get-acad-object)
           menuGroups (vla-get-menugroups acadapp)
   )

   (vlax-for eachMG menuGroups
      (setq nameMG (vla-get-name eachMG))
      (if (= nameMG "BATCHPUBLISH") ;Change this to the name of your menu
         (princ "\n BATCHPUBLISH menu has been loaded.")
      )
   )
   (princ)
  )

