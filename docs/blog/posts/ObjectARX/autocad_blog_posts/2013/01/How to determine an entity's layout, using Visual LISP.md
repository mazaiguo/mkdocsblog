---
title: "How to determine an entity's layout, using Visual LISP"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Block
description: "Any entity you select has an owner.  If it is a sub-entity of a block reference, the block reference is the owner.  If it is not a sub-entity, then..."
author: Autodesk
---
# How to determine an entity's layout, using Visual LISP

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-determine-an-entitys-layout-using-visual-lisp.html

## 文章内容

By Gopinath Taget
Any entity you select has an owner.  If it is a sub-entity of a block reference, the block reference is the owner.  If it is not a sub-entity, then either Paper Space or Model Space would be the owner.  From the owner's Object ID we can get the object, its Layout property, and finally the Layout's name property, to identify the layout.  The Visual LISP example below shows how to get this property.
  (defun c:GetLayout ( / oApp oDoc obj lOwnerID
            ownerObj bIsLayout sLoName)
   (vl-load-com)
   (setq oApp    (vlax-get-acad-object)
           oDoc    (vla-get-activedocument oApp)
           obj    (vlax-ename->vla-object (car (entsel)))
           lOwnerID  (vla-get-ownerid obj)
           ownerObj  (vla-objectidtoobject oDoc lOwnerID)
           bIsLayout (vlax-get-property ownerObj "IsLayout")
   ) ;setq
     (if (= bIsLayout :vlax-true)
      (progn
         (setq sLoName (vla-get-name (vla-get-layout ownerObj)))
         (alert (strcat "Layout Name is " sLoName))
      ) ;progn
   ) ;if
   (princ)
)

