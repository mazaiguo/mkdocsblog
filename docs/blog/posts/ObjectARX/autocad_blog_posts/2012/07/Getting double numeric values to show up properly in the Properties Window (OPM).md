---
title: "Getting double numeric values to show up properly in the Properties Window (OPM)"
date: 2012-07-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - COM
description: "I've created a COM Wrapper for a Custom Object I've made. It seems that any/all double values that are added to the com wrapper automatically get d..."
author: Autodesk
---
# Getting double numeric values to show up properly in the Properties Window (OPM)

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/getting-double-numeric-values-to-show-up-properly-in-the-properties-window-opm.html

## 文章内容

By Philippe Leefsma
Q:
I've created a COM Wrapper for a Custom Object I've made. It seems that any/all double values that are added to the com wrapper automatically get displayed in the properties window as units of the type specified in the "Drawing Units" dialog. So if the double value is 14.500, it is automatically displayed by the Properties box as 1'-2½" in the AutoCAD properties window.
Is there any way to override this feature of the properties window and just allow the double entered to not be changed and shown as is???
A:
By default the OPM interprets double values as distance values.
Rather than returning a double variable type return one of the following (in your IDL and in your property functions) :
ACAD_DISTANCE - distance value
ACAD_ANGLE - angle value
ACAD_NOUNITS - simple double/ads_real value

