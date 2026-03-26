---
title: "Select vertices of a polyline"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - Polyline
  - Selection
description: "The vertices of the AcDbPolyline are not separate entities, that is why acedNentSelP() no longer works. The vertex information is now stored direct..."
author: Autodesk
---
# Select vertices of a polyline

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/how-to-select-vertices-of-a-new-style-polyline.html

## 文章内容

By Augusto Goncalves
The vertices of the AcDbPolyline are not separate entities, that is why acedNentSelP() no longer works. The vertex information is now stored directly in the polyline entity. The AcDbPolyline supports GS Markers (Graphic System Markers), which means you can find out which vertex the user selected by a combination of ssget and ssnamex:
(setq s (ssget))
(setq marker (caddr (car (setq e (ssnamex s 0)))))
(setq e (entget (cadr (car e))))
(setq l 0)
(foreach i e
   (if (= 10 (car i))
      (progn
         (if (= l marker)
            (progn
               (princ (cdr i))
               (terpri)
            )
         )
         (setq l (1+ l))
      )
   )
)

## 评论

**内容**: Account Deleted said...
Hi, Augusto!
"The vertices of the AcDbPolyline are not separate entities, that is why acedNentSelP() no longer works."
Reply
09/04/2012 at 03:42 AM

---
**内容**: Augusto Goncalves said in reply to Account Deleted...
Thanks Alexander, I have fixed this type.
Regards,
Augusto Goncalves
Reply
09/05/2012 at 05:41 AM

---
**内容**: Account Deleted said in reply to Augusto Goncalves...
And now you can delete my comment. :-)
Reply
09/05/2012 at 02:05 PM

---
**内容**: Augusto Goncalves said in reply to Account Deleted...
I like the comments :) keep them coming.
Reply
09/05/2012 at 02:08 PM

---
