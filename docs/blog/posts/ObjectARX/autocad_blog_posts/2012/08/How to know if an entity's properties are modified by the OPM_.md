---
title: "How to know if an entity's properties are modified by the OPM?"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "How would one know if an entity's properties are modified by the OPM?"
author: Autodesk
---
# How to know if an entity's properties are modified by the OPM?

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/how-to-know-if-an-entitys-properties-are-modified-by-the-opm.html

## 文章内容

By Philippe Leefsma
Q:
How would one know if an entity's properties are modified by the OPM?
A:
OPM brackets the property modification calls with modeless operation start/end notifications using the string "OPM_CHGPROP".
Applications should receive these notifications through the AcEditorReactor::modelessOperationWillStart() and AcEditoReactor::modelessOperationEnded()

