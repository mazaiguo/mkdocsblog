---
title: "How can you show AModeler hidden line as a dashed line"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - HLR
  - Polyline
description: "Basically, you'll need to add a class that is derived from OutputPolylineCallback and override outputPolyline(). Next, instantiate a callback objec..."
author: Autodesk
---
# How can you show AModeler hidden line as a dashed line

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/how-can-you-show-amodeler-hidden-line-as-a-dashed-line.html

## 文章内容

By Gopinath Taget
Basically, you'll need to add a class that is derived from OutputPolylineCallback and override outputPolyline(). Next, instantiate a callback object in the subViewportDraw() of the custom entity class so it is called when it is HIDE, SHADE or RENDER. Since the callback will give you the hidden edges of a body, if you figure out the correct projection plane, it is just a matter of loading a dashed linetype and displaying the hidden edges in an appropriate LTSCALE.
There is also a trick to force AutoCAD to display the hidden edges. All of the above is fully demonstrated in this sample. Pay special attention to AsdkBody.cpp and .h files, and please be sure to load the sample drawing to test.

