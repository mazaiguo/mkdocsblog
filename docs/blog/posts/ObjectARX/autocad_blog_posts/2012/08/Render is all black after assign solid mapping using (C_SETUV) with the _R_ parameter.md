---
title: "Render is all black after assign solid mapping using (C:SETUV) with the "R" parameter"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Solid
description: "I am trying to make a solid mapping using c:setuv with the "R" parameter. When the entity is rendered it is completely black."
author: Autodesk
---
# Render is all black after assign solid mapping using (C:SETUV) with the "R" parameter

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/render-is-all-black-after-assign-solid-mapping-using-csetuv-with-the-r-parameter.html

## 文章内容

By Philippe Leefsma
Q:
I am trying to make a solid mapping using c:setuv with the "R" parameter. When the entity is rendered it is completely black.
A:
A change request is pending against this behavior. One work around to consider would be to use the "P" option as illustrated below:
-
(defun 3DPOINT (pt cx cy cz /)
   (if cx (setq pt (list (+ (car pt) cx) (cadr pt) (caddr pt))))
   (if cy (setq pt (list (car pt) (+ (cadr pt) cy) (caddr pt))))
   (if cz (setq pt (list (car pt) (cadr pt) (+ (caddr pt) cz))))
)
(defun c:test ()
  (setq ss_obj (ssget) 
           p0 (list 0.0 0.0 0.0)
           current_mapsize 5 
  ) ;setq
  (C:MATLIB "I" "APE" (findfile "RENDER.MLI")) 
  (C:RMAT "A" "APE" ss_obj)
  (c:setuv "A" ss_obj "P" p0 (polar p0 0 current_mapsize)(polar p0 (/ pi 2.0) current_mapsize)(3dpoint p0 nil nil current_mapsize))
  (c:rpref "TOGGLE" "SKIPRDLG" "ON")
  (c:rpref "STYPE" "ASCAN")
  (c:render)
)

