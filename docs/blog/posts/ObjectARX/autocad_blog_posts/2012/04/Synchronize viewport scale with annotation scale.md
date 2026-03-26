---
title: "Synchronize viewport scale with annotation scale"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "When on a paper layout, if a viewport is selected or is active then the AutoCAD status bar contains a button that enables the user to synchronize t..."
author: Autodesk
---
# Synchronize viewport scale with annotation scale

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/synchronize-viewport-scale-with-annotation-scale.html

## 文章内容

By Adam Nagy
When on a paper layout, if a viewport is selected or is active then the AutoCAD status bar contains a button that enables the user to synchronize the viewport’s scale with the annotation scale.
You can achieve the same using the below code:
ads_name name;
ads_point pt;
acedEntSel(L"Pick viewport", name, pt);
  AcDbObjectId id;
acdbGetObjectId(id, name);
  AcDbObjectPointer<AcDbViewport> ptrVP(id, AcDb::kForWrite);
   AcDbAnnotationScale * pAnnoScale = ptrVP->annotationScale(); 
double scale;
pAnnoScale->getScale(scale);
delete pAnnoScale;
ptrVP->setCustomScale(scale);

## 评论

**内容**: Rafael said...
I have nerver used LISP, can you use this code in a normal script (notepad) and does it work in the student version of autocad?
Reply
11/26/2015 at 05:29 AM

---
**内容**: Balaji said...
Hi Rafael,
Sorry, i do not know if AutoCAD Student version can run Lisp code.
If you do have it installed, can you please give it a try ?
Here is the Lisp code that helps synchronize the viewport scale and the annoscale :
(vl-load-com)
(defun c:sync()
(command-s "_.pSPACE")
(print "Select a viewport")
(setq vpsel (ssget ":E:S" '((0 . "VIEWPORT"))))
(setq vplist (ssname vpsel 0))
(setq vport (vlax-ename->vla-object vplist))
(command-s ".mspace")
(setq scale (getvar 'cannoscalevalue))
(command-s "_.pSPACE")
(vla-put-CustomScale vport scale)
(vla-regen (vla-get-ActiveDocument (vlax-get-acad-object)) acAllViewports)
(setq vpsel nil)
)
Since you haven't used Lisp before, here are the steps to try it :
-Copy the above Lisp code to notepad and save it as a file with .lsp extension
-Run AppLoad command and choose the lsp file that you saved previously
-Start AutoCAD and switch to paperspace
-Type "(c:sync)" in AutoCAD's command prompt and hit enter
-Choose the paperspace viewport that you want to synch.
Regards,
Balaji
Reply
11/26/2015 at 10:03 PM

---
