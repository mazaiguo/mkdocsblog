---
title: "How to access the truecolor property via AutoLISP?"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - DXF
description: "True color property of an entity is stored under the DXF code of 420.  It is a 32-bit integer value. When used with True Color, the 32-bit integer ..."
author: Autodesk
---
# How to access the truecolor property via AutoLISP?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-access-the-truecolor-property-via-autolisp.html

## 文章内容

By Gopinath Taget
True color property of an entity is stored under the DXF code of 420.  It is a 32-bit integer value. When used with True Color, the 32-bit integer represents a 24-bit color value. The high-order byte (8 bits) is 0, the low-order byte an unsigned char holds the Blue value (0-255), then comes the Green value, and the next-to-high order byte is the Red Value. Converting this integer value to hexadecimal yields the following bit mask: 0x00RRGGBB. For example, a true color with Red = 200, Green = 100 and Blue = 50 is 0x00C86432, and in DXF, in decimal, 13132850. 
The following code demonstrates how to convert a list of rgb to a true color and vice versa, and shows how to retreive/set a true color property to an entity, using AutoLISP. 
;; Convert TrueColor into a list of RGB
(defun trueColorToRGB (tcol)
 (setq r (lsh tcol -16))
 (setq g (lsh (lsh tcol 16) -24))
 (setq b (lsh (lsh tcol 24) -24))
 (list r g b)
)
;; Convert a list of RGB to TrueColor
(defun RGBToTrueColor (rgb)
 (setq r (lsh (car rgb) 16))
 (setq g (lsh (cadr rgb) 8))
 (setq b (caddr rgb))
 (setq tcol (+ (+ r g) b))
)
(defun C:getColor(/)
 (setq ename (car (entsel "\nPick an object with true color:")))
 (setq edata (entget ename)) 
;; we have a true color.
 (setq tcol (cdr (assoc 420 edata)))
 (princ "\n true color = ")(princ tcol)
;; convert it to a list of RGB. 
(setq rgb (trueColorToRGB tcol))
 (princ "\n rgb = ")(princ rgb)
 (princ)
)
(defun C:setColor(/)
 (setq ename (car (entsel "\nPick an object to set a true color:")))
 (setq edata (entget ename))
;; set a true color from a list of rgb values.(R=10 G=100 B=200)
(setq rgb (list 10 100 200))
 (setq tcol (RGBToTrueColor rgb))
;; and set it.
 (setq edata (subst (cons 420 tcol) (assoc 420 edata) edata))
 (entmod edata)
 (princ "\n rgb = ")(princ rgb)
 (princ "\n true color = ")(princ tcol)
 (princ)
)

## 评论

**内容**: Alexander Rivlis said...
Hi, Gopinath!
Are you sure that code is right?
(setq g (lsh (lsh tcol 16) -24))
Maybe
(setq g (lsh (lsh tcol 16) -16))
?
Reply
01/16/2013 at 07:17 AM

---
**内容**: Gopinath Taget said in reply to Alexander Rivlis...
Hi Alexander,
I tested the code as is and it works:
(setq g (lsh (lsh tcol 16) -24))
This code left shifts a 32 bit value (where the high byte is the color method). so we do need to right shift 24 bits.
Cheers
Gopinath
Reply
01/16/2013 at 08:33 PM

---
**内容**: Alexander Rivlis said in reply to Gopinath Taget...
Oh! It's my fault. Excuse me, please!
Reply
01/17/2013 at 03:04 AM

---
**内容**: Alexander Rivlis said...
Other variants:
(defun GetRGB ( truecolor )
(list
(logand (lsh truecolor -16) 255) ;; R
(logand (lsh truecolor -8) 255) ;; G
(logand truecolor 255) ;; B
)
)
(defun GetTrueColor ( r g b )
(+ (lsh r 16) (lsh g 8) b)
)
Reply
01/16/2013 at 07:25 AM

---
**内容**: Owen Wengerd said...
None of those conversions appear to honor the "color method" high byte (i.e. they all assume it will be "byColor").
Reply
01/16/2013 at 07:56 AM

---
