---
title: "Get the per-viewport frozen layers for paper space viewports in Lisp"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Block
  - Layer
description: "The frozen layers of current viewport are stored in the XDATA of the paperspace viewport object. The registered application name is "ACAD"."
author: Autodesk
---
# Get the per-viewport frozen layers for paper space viewports in Lisp

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/get-the-per-viewport-frozen-layers-for-paper-space-viewports-in-lisp.html

## 文章内容

The frozen layers of current viewport are stored in the XDATA of the paperspace viewport object. The registered application name is "ACAD".
In the XDATA, group code 1003 is used to store the layer name. The following code shows how to retrieve this information:
(defun c:ListVPFreezeLayers ()
   (setq psEnt (tblobjname "block" "*PAPER_SPACE"))
   (setq ent (entnext psEnt))
   (setq ent (entnext ent))
   (setq lst (entget ent '("*")))
   (setq ename (cdr (assoc 0 lst)))
   (setq i 0)
   (while (/= ent nil)
      (setq lst (entget ent '("*")))
      (setq ename (cdr (assoc 0 lst)))
      (if (= ename "VIEWPORT")
         (progn
            (setq i (+ i 1))
            (print)
            (princ "Frozen layers of No. ")
            (princ i)
            (princ " viewport are:")
            (setq lst (cdadr (assoc -3 lst)))
            (foreach memb lst
               (if (= 1003 (car memb))
                  (print (cdr memb))
               )
            )
            (print)
         )
      )
      (setq ent (entnext ent))
   )
   (print)
)

