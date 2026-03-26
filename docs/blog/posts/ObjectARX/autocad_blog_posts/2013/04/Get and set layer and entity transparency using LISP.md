---
title: "Get and set layer and entity transparency using LISP"
date: 2013-04-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
  - Layer
description: "Why doesn't the following code work? vla-get-transparency highlights as blue in the VLIDE, but I get this error:"
author: Autodesk
---
# Get and set layer and entity transparency using LISP

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/get-and-set-layer-and-entity-transparency-using-lisp.html

## 文章内容

By Adam Nagy
Why doesn't the following code work? vla-get-transparency highlights as blue in the VLIDE, but I get this error:
"Error: ActiveX Server returned the error: unknown name: Transparency"
(setq ENT (entsel))
(if ENT
  (progn
    (setq VLA_OBJ_NAME (vlax-ename->vla-object (car ENT))
    VLA_OBJ_LAYER (vla-get-layer VLA_OBJ_NAME)
    VLA_ACT_DOC (vla-get-ActiveDocument (vlax-get-Acad-Object))
    LAYERNAME (vla-Item (vla-get-Layers VLA_ACT_DOC) VLA_OBJ_LAYER)
    )
    (if (>= (atof (substr (getvar "acadver") 1 4)) 18.1)
      (setq PROPTRAN (vla-get-transparency LAYERNAME))
    )
  )
)
Solution
The properties that you access when using the COM helpers of LISP are based on the ActiveX API.
If you look for the Transparency property in the ActiveX API, then you’ll find that it is only available for AcadRasterImage and AcadWipeout entities.
The Transparency for entities (which is only available in AutoCAD 2011) is provided by new interfaces like IAcadEntity2 and they are called EntityTransparency.
In case of layers however, there is no property like that.
That transparency value can be calculated from the layer’s XData. If it’s not there, then it’s the default 0%
; gets transparency in percentage 
(defun getLayerTransparency (layerName / layer transparency) 
  (setq layer (tblobjname "LAYER" layerName)) 
  ; get the XData of AcCmTransparency    
  (setq transparency (cdr (assoc 1071 (cdar (cdr (assoc -3 
    (entget layer '("AcCmTransparency")))))))) 
  (if (= transparency nil) 
    ; if we did not get a value it must be the default 0% 
    (setq transparency 0) 
    ; if we got a value then calculate from it 
    (progn 
      ; get the lower byte of the value 0..255 
      ; (100%..0% in the AutoCAD user interface) 
      (setq transparency (lsh (lsh transparency 24) -24)) 
      ; convert the value to a percentage 
      (setq transparency (fix (- 100 (/ transparency 2.55))))    
    ) ; (progn 
  ) ; (if  
)

(defun c:testGet (/ ent layerName transparency) 
  (setq ent (car (entsel))) 
  (setq layerName (cdr (assoc 8 (entget ent))))
  (setq transparency (getLayerTransparency layerName)) 
  (princ transparency) 
  (princ) 
)
It does not seem possible to set the value the same way - by adjusting the XData value -, but you can use the _LAYER command for that:
(defun c:testSet (/ ent layerName transparency) 
  (setq ent (car (entsel))) 
  (setq transparency (getint "Transparency value")) 
  (setq layerName (cdr (assoc 8 (entget ent))))
  (command "_LAYER" "_TR" transparency layerName "") 
  (princ) 
)
Code has been updated based on BlackBox's comments. Now it is not using unnecessary ActiveX function calls.

## 评论

**内容**: Paulo said...
Thanks so much. This tip is GOLD. =)
Reply
04/28/2013 at 12:06 PM

---
**内容**: BlackBox said...
Adam,
I think you're making this far more complicated than it needs to be.
Why are you twice (once in your test command, and another in your sub-function), converting to/from respectively vla-Object, to eName, when you can instead work with eName alone?
As I'm sure you're already aware....
In the case of the test function, instead of converting the eName to vla-Object, extracting the Layer Property string, you could instead simply extract (cdr (assoc 8 (entget eName))).
As for the sub-function, instead of getting the Layer Object from the Layers Collection via layerName string parameter, then converting that with vlax-Vla-Object->Ename, one can instead simply use TblObjName function on the Layers table directly.
Cheers
Reply
04/29/2013 at 01:10 PM

---
**内容**: Adam Nagy said in reply to BlackBox...
Hi BlackBox,
Thank you for the comments. Yes, it seems I'm a bit prone to use ActiveX in LISP :) - especially when the code in the question is using it already.
I updated the code accordingly.
Thanks again,
Adam
PS: What's even more important of course is that now I added colours to the code :-D
Reply
04/30/2013 at 03:18 AM

---
**内容**: Tony Tanzillo said in reply to Adam Nagy...
At this thread you can find a set of helper functions that make using ActiveX from LISP much easier and intuitive (almost as intuitive as VBA).
http://www.theswamp.org/index.php?topic=44212.msg494692#msg494692
Reply
04/30/2013 at 07:10 PM

---
**内容**: BlackBox said...
Adam,
For your consideration:
http://www.theswamp.org/index.php?topic=44517.0
Reply
05/02/2013 at 06:04 PM

---
**内容**: Anthony Isaac said...
An endowment fund displaced for the theme and augment of the citizens. The paths of the ai video generator are inclined for the terms. The rule is played for the hooting for the true aloe for the suggested element for the times by all issues.
Reply
06/17/2023 at 03:16 PM

---
