---
title: "Call to CoCreateInstance (in C++) loads AcVBA.arx"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - COM
  - VBA
description: "This is as designed. COM DLLs made in VB query for the IMSOComponentManager service on the STA message filter and this query is satisfied by loadin..."
author: Autodesk
---
# Call to CoCreateInstance (in C++) loads AcVBA.arx

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/call-to-cocreateinstance-in-c-loads-acvbaarx.html

## 文章内容

By Augusto Goncalves
This is as designed. COM DLLs made in VB query for the IMSOComponentManager service on the STA message filter and this query is satisfied by loading VBA.
For instance: an ARX module that calls CoCreateInstance to instantiate VB-based COM class, when the code was executed, AutoCAD will try to initialize its VBA sub system. On this scenario, AutoCAD fails to initalize its VBA sub-system and the exception it thrown killing the CoCreateInstance function call. In fact, the system is trying to locate "acvba.arx" and eventually threw an ole error if it was not found.
So currently, the only work around available is *not* to use VB to build components if we do not want this dependency.

