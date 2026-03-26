---
title: "Using BRep API in AutoCAD OEM"
date: 2013-10-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - OEM
description: "Recently a developer reported this error message when a custom .arx module that made BRep calls was being loaded at startup : "'xxx.arx cannot find..."
author: Autodesk
---
# Using BRep API in AutoCAD OEM

发布日期: 2013-10-01

原始链接: https://adndevblog.typepad.com/autocad/2013/10/using-brep-api-in-autocad-oem.html

## 文章内容

By Balaji Ramamoorthy
Recently a developer reported this error message when a custom .arx module that made BRep calls was being loaded at startup : "'xxx.arx cannot find a procedure that it needs.”
A way to narrow down the procedure that is not being found is to use gflags.exe that is part the debugging tools for Windows from the Windows SDK. Here are the steps :
1) Run the gflags.exe and specify the OEM product name.
2) Hit the Tab key and turn on the loader snaps 
                      3) Run the OEM product under the Visual Studio debugger until the error message appears in the command prompt.
4) Look at the messages in the Visual Studio output window to identify the procedure name that is not being found similar to the one shown here :
LdrpSnapThunk - ERROR: Procedure "?isSelfIntersecting@AcGeImpCurve3d@@UEBAHPEAVAcGeSelfIntersectTestCallback@@AEBVAcGeTol@@@Z" could not be located in DLL "AcGe19.dll" First-chance exception at 0x77350108 in TTGCAD.exe: 0xC0000139: Entry Point Not Found.
In this case a method in the "AcGe19.dll" was not being found. Copying "AcGe19.dll" from the OEM installer folder under "\x64\aoem\Program Files\Root\acge19.dll" to the OEM 2013 folder and rebuilding the product resolved the issue.

## 评论

**内容**: damien s said...
I am suggesting to try "Long Path Tool" program that solves long file names issues with simplicity.
Reply
07/26/2017 at 06:25 AM

---
