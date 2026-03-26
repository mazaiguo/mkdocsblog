---
title: "Jigged entity's properties do not appear in the OPM (Property Palette)"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Palette
description: "My code follows very closely the "ObjectARX 2009 SDK\samples\editor\Palettes\BoltSolution" sample but still the properties of the jigged entity do ..."
author: Autodesk
---
# Jigged entity's properties do not appear in the OPM (Property Palette)

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/jigged-entitys-properties-do-not-appear-in-the-opm-property-palette.html

## 文章内容

By Adam Nagy
My code follows very closely the "ObjectARX 2009 SDK\samples\editor\Palettes\BoltSolution" sample but still the properties of the jigged entity do not appear in the OPM.
Solution
After looking through your code it seems that you forgot to add the ACRX_CMD_INTERRUPTIBLE flag to the command you start the jig from:
// Supports OPM display of command properties
#define ACRX_CMD_INTERRUPTIBLE      0x00400000

