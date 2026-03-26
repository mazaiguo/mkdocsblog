---
title: "Understanding group code 68 of AcDbViewport"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Group code 68 represents the viewport status field, and the value is an integer with the following meaning:"
author: Autodesk
---
# Understanding group code 68 of AcDbViewport

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/understanding-group-code-68-of-acdbviewport.html

## 文章内容

By Gopinath Taget
Group code 68 represents the viewport status field, and the value is an integer with the following meaning:
0: the viewport is off so that the view within it is not displayed on screen.
Non-zero value: The viewport is on so that the view within it is displayed on screen as long as this viewport is active (only certain number of viewports can be active at any time. This number is reported by the MAXACTVP system variable). And the value indicates the order of stacking for the viewports, where 1 is the active viewport, 2 is the next, etc..

