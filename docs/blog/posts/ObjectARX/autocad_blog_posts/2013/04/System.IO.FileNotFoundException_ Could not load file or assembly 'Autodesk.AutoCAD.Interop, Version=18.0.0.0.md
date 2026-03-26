---
title: "System.IO.FileNotFoundException: Could not load file or assembly 'Autodesk.AutoCAD.Interop, Version=18.0.0.0"
date: 2013-04-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - COM Interop
  - ObjectARX
  - Plugin
description: "My AddIn is referencing the Autodesk.AutoCAD.Interop version 18.0.0.0 assembly from the ObjectARX 2010 SDK, so that it works with AutoCAD 2010, 201..."
author: Autodesk
---
# System.IO.FileNotFoundException: Could not load file or assembly 'Autodesk.AutoCAD.Interop, Version=18.0.0.0

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/systemiofilenotfoundexception-could-not-load-file-or-assembly-autodeskautocadinterop-version18000.html

## 文章内容

By Adam Nagy
Issue
My AddIn is referencing the Autodesk.AutoCAD.Interop version 18.0.0.0 assembly from the ObjectARX 2010 SDK, so that it works with AutoCAD 2010, 2011 and 2012. Unfortunately, if my application is run on a computer where only AutoCAD 2011 is installed I get a FileNotFoundException:
System.IO.FileNotFoundException: Could not load file or assembly 'Autodesk.AutoCAD.Interop, Version=18.0.0.0, Culture=neutral, PublicKeyToken=eed84259d7cbf30b' or one of its dependencies. The system cannot find the file specified.
File name: 'Autodesk.AutoCAD.Interop, Version=18.0.0.0, Culture=neutral, PublicKeyToken=eed84259d7cbf30b'
Solution
Unfortunately, the AutoCAD 2011 installer does not install the AutoCAD 2010 version (18.0.0.0) of the Autodesk.AutoCAD.Interop.dll. This issue is supposed to be remedied in Update 1.1 for AutoCAD 2011.
You could also work around the issue by creating your own version of the interop assembly using tlbimp, reference that in your application and distribute this interop assembly with your application. It's recommended to use a different name for it, e.g. My.Autodesk.AutoCAD.Interop.dll
In the Visual Studio Command Prompt navigate to the appropriate ARX SDK include folder and type tlbimp acax18enu.tlb /out:My.Autodesk.AutoCAD.Interop.dll
We have the same issue on x64 OS's as well, that the 64 bit interop dll's are not installed - this would require the same workaround as described above. This issue is supposed to be fixed in AutoCAD 2012.
Note: you can simply start explorer and type %WINDIR%\assembly in the Address field to see which assemblies are installed on your system.

