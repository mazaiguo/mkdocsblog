---
title: "Creating a Layout using Visual LISP in AutoCAD"
date: 2012-06-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Plot
description: "Here’s a nice example that shows how to add a Layout using Visual LISP. It also shows how to set a Plot Style configuration and the Paper Size, and..."
author: Autodesk
---
# Creating a Layout using Visual LISP in AutoCAD

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/creating-a-layout-using-visual-lisp-in-autocad.html

## 文章内容

by Fenton Webb
Here’s a nice example that shows how to add a Layout using Visual LISP. It also shows how to set a Plot Style configuration and the Paper Size, and then make the new Layout active…
(defun c:addMyLayout ()
  (vl-load-com)
  (setq acadApp (vlax-get-Acad-object))
  (setq acadDoc (vla-get-ActiveDocument acadApp))
  (setq layouts (vla-get-Layouts acadDoc))
    ;; Delete the layout named "Test" if it exists
  (vlax-for objLayout layouts
    (if (= (vla-get-name objLayout) "Test")
      (progn
        (princ
          (strcat "\nDeleted Layout named "
              (vla-get-name objLayout) "..."
          )
        )
        (vla-delete objLayout) ;delete the Layout
        (vlax-release-object objLayout) ; release the Layout Object
      );progn
    );if
  ) ;vlax-for
    (setq layoutObj (vla-add layouts "Test"))
    ;; Assign Grayscale.CTB to the Layout
  (vla-put-StyleSheet layoutObj "Grayscale.ctb")
    ;; Assign DWF configuration to the Layout
  (if (= (substr (vlax-variant-value (vla-getvariable acadDoc "ACADVER")) 1 2) "15")
    (vla-put-configname layoutObj "PublishToWeb DWF.pc3")
    (vla-put-configname layoutObj "DWF6 ePlot.pc3")
  ) ;if
    ;; Assign Paper Size B to the Layout  
  (vla-put-canonicalmedianame
    layoutObj
    "ANSI_expand_B_(11.00_x_17.00_Inches)"
  )
    ;; Make the new Layout Active
  (vla-put-activelayout acadDoc layoutObj)
    ;; Example getting StyleSheet and Configname, not doing anything
  ;; with them here however
  (setq currPStyle (vla-Get-StyleSheet layoutObj))
  (setq currConfig (vla-Get-configname layoutObj))
  (princ)
)

## 评论

**内容**: Irné Barnard said...
Much more elegant and efficient version here:
http://www.theswamp.org/index.php?topic=42101.0
Reply
06/26/2012 at 02:28 AM

---
**内容**: Hasan said...
Thanks for this great example
I am wondering if there an exampl to import layout from existing drawing?
Thanks
Reply
02/07/2013 at 01:56 AM

---
**内容**: Salama said...
Thnks,
could this be a more detailed lisp routine by creating /drawing custom paper sizes layouts.
We hope from you to write a lisp that could initiate a Template layout for the most common paper sizes like A4,A3,A2,A1, A0 by drawing a rectangle frame with the Exact size of paper.
Reply
01/05/2021 at 04:48 AM

---
