---
title: "How to force an insert to be refreshed?"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "Lets say you are looking for a way to force an update of the AcDbBlockReferences after modifying its AcDbBlockTableRecord without having to call RE..."
author: Autodesk
---
# How to force an insert to be refreshed?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-force-an-insert-to-be-refreshed.html

## 文章内容

By Gopinath Taget
Lets say you are looking for a way to force an update of the AcDbBlockReferences after modifying its AcDbBlockTableRecord without having to call REGEN?
The simplest and fastest way to do this is to iterate the current space, open all the AcDbBlockReference entities for write and call the assertWriteEnabled() method. Because your block definition could be nested in another block definition, you should call assertWriteEnabled() on all AcDbBlockReferences that are present.
As an alternative method (which may decrease the time spent on the process) and to avoid unnecessary 'Undo' information recording, you can temporarily turn off the Undo recording and restore it after the process. To do this, use the 'AcDbDatabase::disableUndoRecording()' method.

## 评论

**内容**: Tony Tanzillo said...
"The simplest and fastest way to do this is to iterate the current space, open all the AcDbBlockReference entities for write and call the assertWriteEnabled() method."
I'm not sure that's the 'fastest' way. :d
You can open the AcDbBlockTableRecord for the block whose insertions you want to refresh, and call getBlockReferenceIds( false, true ) to get an array of the ids of all insertions of the block, and all insertions of all dependent blocks, then open each of them for write and call assertWriteEnabled().
You should also call acdbForceOpenObjectOnLockedLayer() before opening each insertion if it's on a locked layer.
Reply
01/21/2013 at 01:03 AM

---
