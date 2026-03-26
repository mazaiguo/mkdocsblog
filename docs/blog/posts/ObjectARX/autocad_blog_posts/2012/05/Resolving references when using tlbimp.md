---
title: "Resolving references when using tlbimp"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C++
  - COM
  - COM Interop
  - ObjectARX
description: "To use a COM component in a .Net project, you will need an inter-op assembly created from the type-library which can be referenced in your .Net pro..."
author: Autodesk
---
# Resolving references when using tlbimp

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/resolving-references-when-using-tlbimp-.html

## 文章内容

By Balaji Ramamoorthy
To use a COM component in a .Net project, you will need an inter-op assembly created from the type-library which can be referenced in your .Net project. This is done automatically when a reference is added in a .Net project using the “Add Reference” and selecting a component from the COM tab. But it sometimes becomes important to generate these assemblies by using specific versions of the type library.
Type Library importer (tlbimp.exe) is a tool that can create the inter-op assembly from a type-library. In its simplest form, you can use “tlbimp” as follow:
For example if you are creating an inter-op assembly for the E-Transmit type-libary (C:\ObjectARX 2012\inc-x64\AcETransmit18.tlb)
tlbimp "C:\ObjectARX 2012\inc-x64\AcETransmit18.tlb"
/out:AcETransmit18.Interop.dll
/namespace:AcETransmit
/machine:x64
  tlbimp "C:\ObjectARX 2012\inc-win32\AcETransmit18.tlb"
/out:AcETransmit18.Interop.dll
/namespace:AcETransmit
/machine:x86
If you are using tlbimp tool to create an inter-op assembly for one of your own COM components that imports other AutoCAD type-library such as “axdb18enu.tlb”, then you will additionally need to resolve the references. By default, if no additional reference paths are specified, the type-library importer will use the type libraries registered in the registry.
Here is an example usage to resolve the references explicitly:
tlbImp.exe "C:\Test\LineCOMWrapper\x64\MyLineCOMWrapper.arx"
/out:" MyLineCOMWrapper.dll"
/namespace:MyLine
/nologo
/reference:"C:\\ObjectARX 2012\\inc-x64\\Autodesk.AutoCAD.Interop.Common.dll"
/tlbreference:"C:\\ObjectARX 2012\\inc-x64\\axdb18enu.tlb"
/machine:x64 
tlbImp.exe "C:\Test\LineCOMWrapper\Win32\MyLineCOMWrapper.arx" /out:"MyLineCOMWrapper.dll"
/namespace:MyLine
/nologo
/reference:"C:\\ObjectARX 2012\\inc-win32\\Autodesk.AutoCAD.Interop.Common.dll"
/tlbreference:"C:\\ObjectARX 2012\\inc-win32\\axdb18enu.tlb"
/machine:x86
For a complete list of command line switches that can be used with tlbimp.exe, please refer to the MSDN documentation http://msdn.microsoft.com/en-us/library/tt0cf3sx(v=vs.80).aspx

