---
title: "Error "Problem in loading application" on 64 bit OS when using GetInterfaceObject"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - COM
  - Plugin
description: "I have an AutoCAD .NET AddIn which provides an ActiveX server that allows me to drive my AddIn from an external application. This works fine on a 3..."
author: Autodesk
---
# Error "Problem in loading application" on 64 bit OS when using GetInterfaceObject

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/error-problem-in-loading-application-on-64-bit-os-when-using-getinterfaceobject.html

## 文章内容

By Adam Nagy
I have an AutoCAD .NET AddIn which provides an ActiveX server that allows me to drive my AddIn from an external application. This works fine on a 32 bit OS, but on 64 bit I get a "Problem in loading application" error when using GetInterfaceObject() to access my ActiveX server. I checked and the AddIn is loaded, so I'm not sure what goes wrong.
Solution
When you are building your application on a 64 bit OS, then the ActiveX server inside your AddIn is registered by Visual Studio in the 32 bit hive of the registry since Visual Studio itself is 32 bit even on a 64 bit OS. So you have to register your component yourself using the 64 bit version of regasm.
The easiest solution is if you just add a Build Event to your project which runs after each successful build of your project:
"C:\Windows\Microsoft.NET\Framework64\v2.0.50727\regasm.exe" "$(TargetPath)" /tlb /codebase

## 评论

**内容**: Steven Reed said...
My problem is that I am getting this error while doing a GetInterfaceObject("AutoCAD.AcCmColor.18") in my VBA running on my 64-bit Vista machine with AutoCAD Map 3D 2011.
I don't find this is the Registry in either the 32 or 64 bit portions of HKCR.
Any ideas where this should be registered?
Reply
05/08/2013 at 03:30 PM

---
