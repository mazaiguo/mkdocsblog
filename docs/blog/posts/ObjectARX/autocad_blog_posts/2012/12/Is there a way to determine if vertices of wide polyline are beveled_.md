---
title: "Is there a way to determine if vertices of wide polyline are beveled?"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Polyline
description: "If a polyline has multiple segments with different widths, the polyline maybe beveled at the point where the segments meet. Is there a way to deter..."
author: Autodesk
---
# Is there a way to determine if vertices of wide polyline are beveled?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/is-there-a-way-to-determine-if-vertices-of-wide-polyline-are-beveled.html

## 文章内容

By Philippe Leefsma
Q:
If a polyline has multiple segments with different widths, the polyline maybe beveled at the point where the segments meet. Is there a way to determine programmatically which vertices of a polyline are beveled?  
A:
There is not a property that will provide this information directly. One suggestion would be to calculate the angles between the polyline segments. The angles that determine if the bevel is drawn can be estimated from this comment in the regen code:
/* Polyline bevelling criteria: allow bevelling if two edges meet at (roughly) 15 to 179.5 degrees. */
#define MINBEVEL .25 /* About sin(15 deg) */
#define MAXBEVEL .009 /* About sin(.5 d) (= sin(179.5 d)) */

