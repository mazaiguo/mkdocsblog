---
title: "AcDb::ePermanentlyErased when open cloned object during wblock-entire DWG"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - Block
  - DWG
  - Database
description: "Is it possible to open cloned objects in AcEditorReactor::beginDeepCloneXlation() or"
author: Autodesk
---
# AcDb::ePermanentlyErased when open cloned object during wblock-entire DWG

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/acdbepermanentlyerased-when-open-cloned-object-during-wblock-entire-dwg.html

## 文章内容

By Xiaodong Liang
Issue
Is it possible to open cloned objects in AcEditorReactor::beginDeepCloneXlation() or
AcEditorReactor::endDeepClone()
callbacks when WBLOCK - entire database is performed?
Trying to open them in
AcEditorReactor::beginDeepCloneXlation() or endDeepClone(),
results in getting "ePermanentlyErased" return code. We need to access them in kForWrite mode to make some processing.
  Solution
The problem is that in the context of doing a wblock on the entire database, AutoCAD does a fast wblock operation, which means that AutoCAD does not really clone the objects but simulates doing it because the goal is to save the 'clones' to a file. In order to prevent other users from modifying the clone objects (since the clone and original object are the same object in memory),
AutoCAD returns "ePermanentlyErased" error code when an application tries to open and modify a clone.
  You have two options for opening the clone object:
The first one is to open the original object instead of the clone, and to read information from it. But if you want to modify the object, be aware that both the original and the clone will be affected.
The second option is to disable the fast wblock mechanism by calling AcDbDatabase::forceWblockDatabaseCopy(). Doing this will force AutoCAD to create real clones of the objects. You will then be able to open and modify the clone objects and only them. See the ObjectARX online help for forceWblockDatabaseCopy() usage instructions.

