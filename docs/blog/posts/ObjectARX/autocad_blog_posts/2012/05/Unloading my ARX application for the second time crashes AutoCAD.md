---
title: "Unloading my ARX application for the second time crashes AutoCAD"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "1. appload command and load TestDll.ARX"
author: Autodesk
---
# Unloading my ARX application for the second time crashes AutoCAD

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/unloading-my-arx-application-for-the-second-time-crashes-autocad.html

## 文章内容

By Adam Nagy
1. appload command and load TestDll.ARX
2. close appload dialog
3. appload command and unload TestDll.ARX
4. close appload dialog
5. appload command and load TestDll.ARX
6. close appload dialog
7. appload command and unload TestDll.ARX -> AutoCAD crashes
Solution
I can see in your project's settings that you are using CLR (i.e. Common Language Runtime Support (/clr)).
This makes your project managed, which means that its extension should be *.dll and it should be loaded using NETLOAD, not APPLOAD.
Note that managed AddIns cannot be unloaded/reloaded in the same AutoCAD session.

