---
title: "Creating a gradient hatch using VLisp"
date: 2012-09-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Hatch
description: "Here is a Visual Lisp example that adds a circle to model space and fill it with a gradient hatch."
author: Autodesk
---
# Creating a gradient hatch using VLisp

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/creating-a-gradient-hatch-using-vlisp.html

## 文章内容

By Balaji Ramamoorthy
Here is a Visual Lisp example that adds a circle to model space and fill it with a gradient hatch.
(defun c:addGHat (/       acadObject  acaddocument
     mspace      mycircle   myloop      myhatch
     col1       col2
     )
   (vl-load-com)

   (setq acver (substr (getvar "acadver")1 2))

   (SetQ acadobject   (VLAX-Get-ACAD-Object)
  acaddocument (VLA-Get-ActiveDocument acadobject)
  mspace      (VLA-Get-ModelSpace acaddocument)
  )
   (SetQ mycircle (VLA-AddCircle
      mspace
      (VLAX-3D-Point '(50.0 50.0 0.0))
      150.0
      )
  )
   (SetQ myloop (VLAX-Make-SafeArray vlax-vbObject '(0 . 0)))
   (VLAX-SafeArray-Put-Element
     myloop
     0
     mycircle
     )
 
  (SetQ myhatch (VLA-AddHatch
     mspace
     acPreDefinedGradient
     "LINEAR"  
     :vlax-true
     acGradientObject
     )
  )
 
  (setq col1 (vla-GetInterfaceObject
         (vlax-get-acad-object)
         (strcat "AutoCAD.AcCmColor." acver)
         )
  )
 
  (setq col2 (vla-GetInterfaceObject
         (vlax-get-acad-object)
         (strcat "AutoCAD.AcCmColor." acver)
         )
  )
 
  (vla-SetRGB col1 255 0 0)
  (vla-setrgb col2 0 0 255)
 
  (vla-put-gradientcolor1 myhatch col1)
  (vla-put-gradientcolor2 myhatch col2)
 
  (VLA-AppendOuterLoop myhatch myloop)
  (VLA-Evaluate myhatch)
)
Update : Thanks to Oleg for suggesting the use of acadVer instead of using "AutoCAD.AcCmColor.19" to get the color object.

## 评论

**内容**: Oleg said...
Hi, Balaji
To get work your code in my Acad version (A2010)
I've added the line to get version, now it works
like a charm. Perhaps it would be useful for somebody else:
(defun c:addGHat (/ acadObject acaddocument
acver mspace mycircle myloop myhatch
col1 col2
)
(vl-load-com)
(setq acver (substr (getvar "acadver")1 2))
(SetQ acadobject (VLAX-Get-ACAD-Object)
acaddocument (VLA-Get-ActiveDocument acadobject)
mspace (VLA-Get-ModelSpace acaddocument)
)
(SetQ mycircle (VLA-AddCircle
mspace
(VLAX-3D-Point '(50.0 50.0 0.0))
150.0
)
)
(SetQ myloop (VLAX-Make-SafeArray vlax-vbObject '(0 . 0)))
(VLAX-SafeArray-Put-Element
myloop
0
mycircle
)

(SetQ myhatch (VLA-AddHatch
mspace
acPreDefinedGradient
"LINEAR"
:vlax-true
acGradientObject
)
)

(setq col1 (vla-GetInterfaceObject
(vlax-get-acad-object)
(strcat "AutoCAD.AcCmColor." acver)
)
)

(setq col2 (vla-GetInterfaceObject
(vlax-get-acad-object)
(strcat "AutoCAD.AcCmColor." acver)
)
)

(vla-SetRGB col1 255 0 0)
(vla-setrgb col2 0 0 255)

(vla-put-gradientcolor1 myhatch col1)
(vla-put-gradientcolor2 myhatch col2)

(VLA-AppendOuterLoop myhatch myloop)
(VLA-Evaluate myhatch)
)
(or (vl-load-com)(princ))
Regards,
Oleg
Reply
09/18/2012 at 02:20 AM

---
**内容**: Balaji said in reply to Oleg...
Thanks Oleg !
Nice change to keep the code independent of the AutoCAD version.
I will update the post based on your suggestion.
Reply
09/18/2012 at 02:38 AM

---
**内容**: Oleg said...
Thanks Balaji,
this is an old trick, perhaps,
I've stoled it from Michael Puckett :)
Regards,
Oleg
Reply
09/18/2012 at 08:54 AM

---
