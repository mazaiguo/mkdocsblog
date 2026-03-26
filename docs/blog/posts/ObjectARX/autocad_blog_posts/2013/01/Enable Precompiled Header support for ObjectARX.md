---
title: "Enable Precompiled Header support for ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "You need to create the Precompiled header through stdafx.cpp first before you can use it."
author: Autodesk
---
# Enable Precompiled Header support for ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/enable-precompiled-header-support-for-objectarx.html

## 文章内容

By Augusto Goncalves
You need to create the Precompiled header through stdafx.cpp first before you can use it.
First turn on Precompiled Header support for the whole project, Right click and goto the Project properties, select "C/C++ -> Precompiled headers"
Set to "Use Precompiled Header" through "Stdafx.h"
Next you need to tell the compiler the source file from which it should create the Precompiled header from, simply navigate to Stdafx.cpp and go to the Project properties, select "C/C++ -> Precompiled headers"
Set "Create Precompiled Header"
Compile

