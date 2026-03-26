---
title: "Cloned viewport exists but is invisible in a newly created layout"
date: 2012-08-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - DWG
  - ObjectARX
description: "Starting from a layout "layout1" with a viewport "vp" in it, I wish to copy this viewport with ObjectARX (deepCloneObjects) into an existing but no..."
author: Autodesk
---
# Cloned viewport exists but is invisible in a newly created layout

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/cloned-viewport-exists-but-is-invisible-in-a-newly-created-layout.html

## 文章内容

By Philippe Leefsma
Q:
Starting from a layout "layout1" with a viewport "vp" in it, I wish to copy this viewport with ObjectARX (deepCloneObjects) into an existing but not yet opened layout "layout2" of the same dwg. But changing to layout2 the copied viewport is invisible and cannot be selected nor can it be found with the _list command or anything else.
If layout2 was already opened once before copying vp (without filling in the page setup dialog), everything works fine i.e. vp is perfectly visible after changing to layout2.
What is wrong?
A:
Because the paperspace viewport is not created until the first time a layout is activated, it’s very likely that there’s no paperspace viewport for the layout that the viewport is being copied into, or that the paperspace viewport ends up *NOT* being the first AcDbViewport object in the layout’s BlockTableRecord. It is not supposed to matter whether the paperspace viewport is the first viewport or not, but a lot of the layout handling code (and other code as well) assumes that the paperspace viewport is the first viewport in the BlockTableRecord. So, if the paperspace viewport is not first, problems can occur.
The solution is to switch to the Layout first (making it active) before cloning the viewport.

