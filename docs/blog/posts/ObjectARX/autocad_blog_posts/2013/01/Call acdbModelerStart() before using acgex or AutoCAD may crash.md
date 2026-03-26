---
title: "Call acdbModelerStart() before using acgex or AutoCAD may crash"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Solid
description: "You might find that sometimes, when creating 3D Solids such as an AcGeCylinder instance, AutoCAD crashes (at the constructor of these classes)."
author: Autodesk
---
# Call acdbModelerStart() before using acgex or AutoCAD may crash

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/call-acdbmodelerstart-before-using-acgex-or-autocad-may-crash.html

## 文章内容

By Gopinath Taget
You might find that sometimes, when creating 3D Solids such as an AcGeCylinder instance, AutoCAD crashes (at the constructor of these classes).
This problem can be resolved if the modeler dlls are loaded. When an application uses anything in acgex (set of math classes for solid modeling and computations), it must first call acdbModelerStart() to ensure that the modeler dlls are available. It must then call acdbModelerEnd() when it is finished with all calls to acgex.

