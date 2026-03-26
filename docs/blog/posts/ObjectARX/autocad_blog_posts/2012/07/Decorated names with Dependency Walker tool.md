---
title: "Decorated names with Dependency Walker tool"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - COM
description: "The Dependency Walker tool, available at www.dependencywalker.com, is “is a free utility that (…) lists all the functions that are exported by that..."
author: Autodesk
---
# Decorated names with Dependency Walker tool

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/decorated-names-with-dependency-walker-tool.html

## 文章内容

By Augusto Goncalves
The Dependency Walker tool, available at www.dependencywalker.com, is “is a free utility that (…) lists all the functions that are exported by that module, and which of those functions are actually being called by other modules”.
This is particularly interesting on AutoCAD programing environment as several functions are not API exposed or document, but still exported on the C++ code. That way, it is possible use DllImport to call them.
On a previous post, we explain how use this DllImport to call our custom C++ methods, but in some cases the method name changes when compiled. This different name is called decorated names. When that happens, the Dependency Walker show us the decorated name required on the EntryPoint attribute parameter.
Important: the decorated name may change between AutoCAD major versions, for instance between 2012 (R18) and 2013 (R19), and between platforms (e.g. 32 and 64 bit). That way, it is usually required to create more than one DllImport, one for each variation.
To get the decorated name, start the tool, open the DLL or EXE, find the method and right-click to uncheck ‘Undecorate C++ Function’, as shown below.
Then right-click again to ‘Copy Function Name’, as shown below. Now we can use this name at the EntryPoint parameter.

