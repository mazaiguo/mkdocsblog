---
title: "Index color versus true color and how to use AcCmEntityColor::colorMethod"
date: 2012-09-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - Layer
  - ObjectARX
description: "Is there a document that better explains how the true color works?"
author: Autodesk
---
# Index color versus true color and how to use AcCmEntityColor::colorMethod

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/index-color-versus-true-color-and-how-to-use-accmentitycolorcolormethod.html

## 文章内容

By Philippe Leefsma
Q:
Is there a document that better explains how the true color works?
What format is the AcCmEntityColor? How is it made up? How does the colorMethod() property work?
A:
AutoCAD actually stores either ACI or RGB values depending on what color is specified. For example, if a circle is assigned an index color, it will be stored as an index color. If it is assigned an RGB value, it will be stored as RGB value. There is a reason for this kind of implementation. One is that ACI color scheme is the legacy that we have to maintain. More importantly, there are some differences of using ACI and RGB. For example, plot style and render material for an entity that is assigned byColor can only use index colors not RGB values.
Another key point is that there are 256 index colors with a set of matching RGB values and we do provide API features to convert them back and forth. ACI to RGB - acedGetRGB(), RGB to ACI - accmGetColorFromRGBName() and AcCmColor::getColorIndex(). But keep in mind that from RGB to ACI will be the closest match unless it is the exact 256 index mapped values. This means if you convert an ACI color to an RGB color, you can expect getting back the exact index color number by converting the RGB value. The reverse is not always true. If you have an RGB color, if it falls into an exact match with an ACI color, there it no problem. If not, there is no round trip guarantee that the original RGB values can be obtained through the conversion process.
In regards to AcCmEntityColor::colorMethod(), it is true that it is not recommended for external developers' to use and it is risky to use it, especially it is prohibitive to use kByPen, kLayerOff, kLayerFrozen and kNone as documented in ObjectARX reference. However, if you have to do it, just keep in mind that every time you use kByColor, make sure you use RGB values. If you use kByACI, make sure entity colors are set by index colors. This basically means that all the ground work needs to be performed every time you change to a difference color method to ensure all properties are set properly. Otherwise, certain values can be garbage so they are useless.

