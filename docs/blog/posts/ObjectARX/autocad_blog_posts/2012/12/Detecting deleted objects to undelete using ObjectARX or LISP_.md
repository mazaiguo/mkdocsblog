---
title: "Detecting deleted objects to undelete using ObjectARX or LISP?"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - AutoLISP
  - C++
  - ObjectARX
  - Selection
description: "You might wonder, with an entity name, or a selection set of entities, if there is a way in to determine if any entities have been deleted so that ..."
author: Autodesk
---
# Detecting deleted objects to undelete using ObjectARX or LISP?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/detecting-deleted-objects-to-undelete-using-objectarx-or-lisp.html

## 文章内容

By Gopinath Taget
You might wonder, with an entity name, or a selection set of entities, if there is a way in to determine if any entities have been deleted so that they can be undeleted.
In AutoLISP, call entget on each entity name in the selection set. If the entity has been erased since the creation of the set, it will not return any entity data. Then call entdel to undelete the entity.
In ObjectARX, the AcDbObject::erase() method allows you to set or unset the erase bit of an object. You may also call acdbEntDel to undelete the entity.

