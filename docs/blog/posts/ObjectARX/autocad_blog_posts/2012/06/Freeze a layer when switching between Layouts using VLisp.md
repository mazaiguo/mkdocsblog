---
title: "Freeze a layer when switching between Layouts using VLisp"
date: 2012-06-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - DWG
  - Layer
description: "Below is a Visual LISP example that uses :VLR-commandEnded to freeze and thaw a layer named Test when switching between layouts. "LAYOUTCONTROL" is..."
author: Autodesk
---
# Freeze a layer when switching between Layouts using VLisp

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/freeze-a-layer-when-switching-between-layouts-using-vlisp.html

## 文章内容

By Balaji Ramamoorthy
Below is a Visual LISP example that uses :VLR-commandEnded to freeze and thaw a layer named Test when switching between layouts. "LAYOUT_CONTROL" is the name of the command that switches between layouts (the function only runs if this was the command that just ended).
To test this function use a default DWG file and create a layer named "Test".
Note: A different layer needs to be current or the example will fail.  Error checking would need to be added for this issue (no error checking here for simplicity).
(vl-load-com)
(defun com_end (reactorObject callbackdata)
   (setq acadDoc (vla-get-ActiveDocument (VLAX-GET-ACAD-OBJECT)))
   (setq test (nth 0 callbackdata))
   (if (= test "LAYOUT_CONTROL")
      (progn
         (setq testSpace (vla-get-activespace acadDoc))
         (if (= testSpace 0)
            (progn
               ;;get paperspace.
               (setq paperSpace (vla-get-paperspace acadDoc))
               ;; paper space viewport
               ;; using this to get the viewport had problems unless
               ;; the Paper space viewport was previously activated
               ;; using get-activepviewport instead
               ;; (setq pvPort(vla-item paperSpace 1))
               (setq pvPort (vla-get-activepviewport acadDoc))
               ;; make a viewport active and displayed
               (vla-put-activepviewport acadDoc pvPort)
               (vla-display pvPort :vlax-true)
               (vla-put-viewporton pvPort :vlax-true)
               (vla-update pvPort)
               (vla-put-mspace acadDoc :vlax-true)
               ;; get and freeze the layer
               (setq Layers (vla-get-layers acadDoc))
               (setq LayObj (vla-item Layers "Test"))
               (vla-put-freeze LayObj :vlax-true)
            ) ; progn
            (progn
               ;; Thaw the layer - in Model Space
               (setq Layers (vla-get-layers acadDoc))
               (setq LayObj (vla-item Layers "Test"))
               (vla-put-freeze LayObj :vlax-false)
               (vla-regen acadDoc acAllViewports)
            ) ; progn
         ) ; if
      )
   )
)
  ;;; run stuff
(mapcar 'vlr-remove-all '(:VLR-COMMAND-Reactor))
(VLR-command-Reactor
   nil
   '((:VLR-commandEnded . com_end))
)

## 评论

**内容**: samsul said...
this is using for what??
Reply
08/15/2012 at 08:58 PM

---
