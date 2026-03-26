---
title: "Background color of the aerial view window"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - COM
  - ObjectARX
  - Palette
description: "The acedSetCurrentColors() function just sets the colors for the AutoCAD drawing window. With this function, it's possible to change the RGB value ..."
author: Autodesk
---
# Background color of the aerial view window

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/background-color-of-the-aerial-view-window.html

## 文章内容

By Augusto Goncalves
The acedSetCurrentColors() function just sets the colors for the AutoCAD drawing window. With this function, it's possible to change the RGB value of some colors. But this function is not intended to change the color of other windows than the drawing window.
There is no other function in the ObjectARX SDK that changes the AutoCAD colors.
As a workaround, use the AutoCAD ActiveX interface. You can access the AutoCAD preferences object via ActiveX. The preferences object has the property 'GraphicsWinBackgrndColor' where you can specify a color index (0-255). You cannot specify a new RGB value for the background color with this function; you can only select a color from the standard AutoCAD color palette. If you use this property, the AutoCAD drawing window and the AerialView window gets a new background color.

