---
title: "Drive AutoCAD and ARX from C++ app"
date: 2015-12-01
categories:
  - AutoCAD .NET
tags:
  - AutoCAD
  - C++
description: "Just like in case of a .NET application, in a C++ application as well you'll need to handle certain COM messages like 0x80010001 (RPCECALLREJECTED)..."
author: Autodesk
---
# Drive AutoCAD and ARX from C++ app

发布日期: 2015-12-01

原始链接: https://adndevblog.typepad.com/autocad/2015/12/drive-autocad-and-arx-from-c-app.html

## 文章内容

By Adam Nagy
Just like in case of a .NET application, in a C++ application as well you'll need to handle certain COM messages like 0x80010001 (RPC_E_CALL_REJECTED) in order to keep things running:
Handling COM calls rejected by AutoCAD from an external .NET application
You also need to take care of making sure your add-in will be allowed to load otherwise a security dialog will pop up:
AutoCAD 2016: Trusted paths and AutoLoader
For testing purposes, the easiest thing might be to add the path of your arx/dll to the trusted paths in the Options dialog: Options >> Files >> Trusted Locations
The rest should be relatively straight-forward.
Here is a sample app that demonstrates this. It includes and exe and an ARX project. In the exe you just have to modify the path of the arx and dwg files which are being used by the sample:
https://github.com/adamenagy/AutoCAD-CppExeAndARX

