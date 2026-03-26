---
title: "Display not updated properly when using acedDragGen()"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Selection
description: "Consider this scenario: You created some AutoCAD entities and would like to drag them. So you get their object IDs, change them to adsname using ac..."
author: Autodesk
---
# Display not updated properly when using acedDragGen()

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/display-not-updated-properly-when-using-aceddraggen.html

## 文章内容

By Gopinath Taget
Consider this scenario: You created some AutoCAD entities and would like to drag them. So you get their object IDs, change them to ads_name using acdbGetAdsName, then add them to a selection set one by one. However, when you try to drag them using acedDragGen, the entities remain in their original location. Why does this happen? Is there anyway to solve it?
Unfortunately, this behavior is as designed. AutoCAD uses a very sophisticated graphics cache to store all the entities in current view. For the sake of performance, this cache is only updated/flushed if changes/user interaction occur in the drawing. Because there are no drawing interactions yet (although the graphic has been dragged), AutoCAD does not update its onscreen display until the action is finished.
The solution is to force AutoCAD to flush its graphic and update its display screen. There are at least two ways to do so. Please add one of the code blocks below before calling acedDragGen() function.
Block 1:
actrTransactionManager->flushGraphics() ;
acedUpdateDisplay();
Block 2:
ads_prompt(_T(""));

