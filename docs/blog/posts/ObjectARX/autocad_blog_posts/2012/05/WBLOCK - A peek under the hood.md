---
title: "WBLOCK - A peek under the hood"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Database
description: "WBLOCK honors hard references (as it always has). This means hard owner and hard pointer references would be cloned during the WBLOCK process. If a..."
author: Autodesk
---
# WBLOCK - A peek under the hood

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/wblock-a-peek-under-the-hood.html

## 文章内容

By Gopinath Taget
WBLOCK honors hard references (as it always has). This means hard owner and hard pointer references would be cloned during the WBLOCK process. If an object that has been chosen for WBLOCK has a hard reference to a second object, the second object is copied during the wblockClone operation (which is used by the WBLOCK command) as well. But this was a potential problem in early releases of AutoCAD (Pre-AutoCAD 2000). Why? The problem with the WBLOCK command was that it first wblockClone's objects into a temporary in-memory database, then calls save() to save the temporary database to disk. But save honors only the ownership references (hard owner and soft owner). This means one kind of hard reference called the hard pointer reference will not be honored by save and that means objects pointed to by hard pointer references would not be saved. Put another way, objects that have been cloned during wblockClone are not saved to the drawing file if their owners haven't been cloned during wblockClone.
To avoid this problem with wblockClone, dictionaries and custom objects (Inheriting from AcDbObject) now automatically file a hardpointer id of their owners. In this way, the complete ownership hierarchy is preserved, and save() can save them all.

