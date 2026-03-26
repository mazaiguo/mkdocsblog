---
title: "AutoLISP Example - set the model or paperspace background color"
date: 2012-05-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
description: "Here is a function that shows how to change the background colors using the ActiveX interface from VisualLISP."
author: Autodesk
---
# AutoLISP Example - set the model or paperspace background color

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/autolisp-example-set-then-model-or-paperspace-background-color.html

## 文章内容

Here is a function that shows how to change the background colors using the ActiveX interface from VisualLISP.
By Wayne Brill
(defun SetBkColor ()
  (setq acad (vlax-get-acad-object)
    pref (vla-get-Preferences acad)
    disp (vla-get-Display pref)
    newColr (vlax-make-variant 255 19)
  );setq
  (if (= (getvar "tilemode") 1)
   ;;change the modelspace background color
    (progn
      (setq oldColr (vla-get-GraphicsWinModelBackgrndColor disp)
         ;;convert unsupported variant type 19 to vlax-vbLong
        oldColrLong (vlax-variant-change-type
        (vla-get-GraphicsWinModelBackgrndColor disp)
          vlax-vbLong)
      );setq
      (vla-put-GraphicsWinModelBackgrndColor disp newColr)
      (alert (strcat "Restore previous background color: "
         (itoa (vlax-variant-value oldColrLong))))
          ;;restore previous model background color
      (vla-put-GraphicsWinModelBackgrndColor disp oldColr)
   );progn
    ;;change the paperspace (layout) background color
   (progn
     (setq oldColr (vla-get-GraphicsWinLayoutBackgrndColor disp)
         ;;convert unsupported variant type 19 to vlax-vbLong
        oldColrLong (vlax-variant-change-type
        (vla-get-GraphicsWinLayoutBackgrndColor disp)
          vlax-vbLong)
     );setq
     (vla-put-GraphicsWinLayoutBackgrndColor disp newColr)
     (alert (strcat "Restore previous background color: "
         (itoa (vlax-variant-value oldColrLong))))
    
    ;;restore previous paper space background color
    (vla-put-GraphicsWinLayoutbackgrndColor disp oldColr)
   );progn
);if
)

## 评论

**内容**: dba said...
Hello Wayne,
as I can see, this method changes the Backgroundcolor for the 2d-Wireframe view. Is there a similar approach to change the bg-col for "3d projected view"?
AutoCAD Architecture 2012 x64 / Win7
Thanks in advance!
Best Regards,
Daniel
Reply
09/04/2013 at 06:46 AM

---
**内容**: dba said...
[edit] 3d parallel projected view
Reply
09/04/2013 at 06:47 AM

---
