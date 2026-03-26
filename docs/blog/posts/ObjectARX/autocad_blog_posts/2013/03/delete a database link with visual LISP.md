---
title: "delete a database link with visual LISP"
date: 2013-03-01
categories:
  - AutoLISP
tags:
  - API
  - AutoLISP
  - Database
description: "How do I delete a database link from an entity using the CAO API and Visual LISP?"
author: Autodesk
---
# delete a database link with visual LISP

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/delete-a-database-link-with-visual-lisp.html

## 文章内容

By Xiaodong Liang
Issue
How do I delete a database link from an entity using the CAO API and Visual LISP?
Solution
The following is a short Visual LISP example that prompts the user to select an object. It then deletes any links that are associated with that object.
;;; This function deletes a link from a selected object

(defun c:DLink ()
(vl-load-com)


;;; Get the object and get the object ID    
(setq ent1 (car (entsel "\nSelect entity to erase links")))
(setq Obj (vlax-ename->vla-object ent1))
(setq ob_ID (vla-get-objectid Obj))


;;; Instantiate the DBConnect object
(setq dbConnect (vlax-create-object "CAO.DbConnect.16"))


;;; Get the linkTemplates    
(setq LTs (vlax-invoke-method dbConnect "GetLinkTemplates"))


;;; Get a linkTemplate named "EmployeeLink1", This linkTemplate
;;; can be created from the Employee table in the DB sample that ships with
;;; AutoCAD
(setq LT (vlax-invoke-method LTs "Item" "EmployeeLink1"))


;;; Get the links using The linkTemplate
(setq linkSel (vlax-invoke-method dbConnect "GetLinks" LT nil nil nil))


;;; Iterate through the links and delete the link
;;; if it has the same ObjectID as the link
(vlax-for thisLink linkSel
   
   (setq l_Obj_ID (vlax-get-property thisLink "ObjectID"))


   (if (= l_Obj_ID ob_ID)
    
    (vla-delete thislink)
   
   )
)


)

