---
title: "Delete LayerFilters using LISP (non-ActiveX)"
date: 2012-09-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
  - Layer
  - Unicode
description: "So maybe you want to write an AutoLISP function (not ActiveX) to delete layerFilters."
author: Autodesk
---
# Delete LayerFilters using LISP (non-ActiveX)

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/delete-layerfilters-using-lisp-non-activex.html

## 文章内容

by Fenton Webb
So maybe you want to write an AutoLISP function (not ActiveX) to delete layerFilters.
With ActiveX (vla-xxx) functions, you can obtain the ACADLAYERS_DICTIONARY dictionary by calling
(vla-getextensiondictionary <layerscollection>)
but how can we access ACAD_LAYERFILTERS and delete the layerfilters, using just plain old AutoLISP?
Here’s how…
(defun C:DelLyrFlt ( / tbl lyr xlist xrec filt)
   (setq tbl (tblnext "LAYER" T)
            lyr (tblobjname "LAYER" (cdr(assoc 2 tbl)))
   ) ;setq
   ;;Find the"ACAD_LAYERFILTERS" xrecord in the extension dictionary of the layer
   (setq xlist (dictsearch
                     (cdr (assoc 360 (entget (cdr (assoc 330 (entget lyr))))))
                     "ACAD_LAYERFILTERS")
   ) ;setq
   (if xlist
      (progn
         ;;Get the first layer_filter
         (setq xrec (cdr (assoc -1 xlist))
                 filt (dictnext xrec t)
         ) ;setq
         ;;Remove each layer_filter
         (while filt
            (dictremove xrec (cdr (assoc 1 filt)))
            (setq filt (dictnext xrec t))
         ) ;while
         ;;Find the"ACAD_LAYERFILTERS" xrecord
         (dictremove
            (cdr (assoc 360 (entget (cdr (assoc 330 (entget lyr))))))
            "ACAD_LAYERFILTERS"
         )
      ) ;progn
   ) ;if
   (princ)
)

## 评论

**内容**: Greg said...
Thanks for posting LISP on the blog. We use lisp quite a lot at work because of its ease of use and we do not need to tweak the code with every new release of AutoCAD that comes through our office.
~Greg
Reply
09/15/2012 at 09:12 AM

---
**内容**: Fenton Webb said...
Hey Greg
I personally believe that LISP is a great tool for doing work in AutoCAD. if it gets the job done, I'm 100% behind it... That includes VBA too.
Reply
09/17/2012 at 10:23 AM

---
