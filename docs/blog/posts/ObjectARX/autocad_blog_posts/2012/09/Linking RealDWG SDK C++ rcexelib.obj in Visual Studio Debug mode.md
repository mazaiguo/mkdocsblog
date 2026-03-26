---
title: "Linking RealDWG SDK C++ rcexelib.obj in Visual Studio Debug mode"
date: 2012-09-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
  - DWG
description: "If you are building a RealDWG application using the C++ API then you will have to link your application with the RealDWG SDK rcexelib.obj so that y..."
author: Autodesk
---
# Linking RealDWG SDK C++ rcexelib.obj in Visual Studio Debug mode

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/linking-realdwg-sdk-c-rcexelibobj-in-visual-studio-debug-mode.html

## 文章内容

by Fenton Webb
If you are building a RealDWG application using the C++ API then you will have to link your application with the RealDWG SDK rcexelib.obj so that your application will run.
The thing is with all Autodesk products, we give them to you compiled in Visual Studio ‘Release’ mode, not in ‘Debug’ mode therefore you have to be careful when trying to run in Debug mode.
The reason you have to be careful is because the default Visual Studio project setup for a Debug project is that it:
Defines _DEBUG preprocessor
Sets the Runtime Library as Multithreaded Debug DLL
If you try and build your RealDWG application in Debug mode with these settings, the linker will have some issues because the RealDWG SDK that you are linking to is built with the NDEBUG preprocessor symbol and Multithreaded DLL. This conflict will either give errors/warnings when building and ultimately crash your application when run.
Therefore, to get your RealDWG to build properly in debug mode, you need to make sure you have _DEBUG not set and also make sure you have Multithreaded DLL set as the Runtime Library…

## 评论

**内容**: Alan Anderson said...
Fenton, this really doesn't work either, because if you have an application with many libs/dlls, then the removal of debug from this one project requires removal of debug from all projects or you will have the same problem with the mismatch of the _ITERATOR_DEBUG_LEVEL for example:
vpcacad.obj : error LNK2038: mismatch detected for '_ITERATOR_DEBUG_LEVEL': value '2' doesn't match value '0' in rcexelib.obj
This worked in the past without having the issue, something has changed, and frankly I haven't got it to work as of yet.
Alan Anderson
Manager Engineering Systems
BlueScope Buildings NA
Reply
09/19/2012 at 02:19 PM

---
**内容**: Fenton Webb said...
Hey Alan
Best thing is to load the RealDWG C++ sample 'DumpDWG' and copy the Visual Studio projects settings from that to your own project settings.
Reply
09/19/2012 at 02:24 PM

---
**内容**: Alan Anderson said...
DumpDWG is failing in acdbValidateSetup(lcid), so now I'm back to a setup problem with RealDWG 2013.
Ideas?
Reply
09/19/2012 at 02:37 PM

---
**内容**: dougal.harris@gmail.com said in reply to Alan Anderson...
Hi Alan,
Did you ever get this to the bottom of this? I am running into exactly the same problem, ie my application has many libs/dlls, the removal of debug from this one project requires removal of debug from all projects in the solution otherwise I get the same problem with the mismatch of the _ITERATOR_DEBUG_LEVEL.
Any help is solving this would be greatly appreciated.
Cheers,
Dougal
Reply
04/11/2013 at 09:37 PM

---
**内容**: hernyo said...
Hi Dougal,
did you manage to sort this out? I'm struggling with the same problem.
Thanks - Laszlo.
Reply
05/25/2013 at 07:22 AM

---
**内容**: Fenton Webb said...
Hey guys
The setup issue is most likely due to the fact that the RealDWG app is not deployed correctly. You need to follow the Redistributable Requirements detailed in readdbx.chm. Failing that, the easiest way to make it work is to output your RealDWG exe to the RealDWG base SDK folder where all of the dependency dlls reside.
Reply
05/25/2013 at 10:49 AM

---
**内容**: Sander said...
The newest visual studios introduce the _ITERATOR_DEBUG_LEVEL problems. That is mixing debug and release libs are detected by the compiler and flatly refused.
Removing _DEBUG from a projects requires the removal of _DEBUG from all the projects.
In an application with many libs/dlls you will see these problems.
I have some other third party libs and they require _DEBUG for debugging purposes. (Also getting into Microsoft libs requires _DEBUG.) Removing this is not really an option.
The best option would be for autodesk to also distribute the debug libs with RealDWG.
Otherwise I hope there is someone who knows how to deal with this?


Reply
11/15/2013 at 12:31 AM

---
**内容**: Fenton Webb said...
Hi guys
The RealDWG is compiled in release mode, therefore, compiling in Debug mode means that you have to link with Multithreaded DLL not Debug Multithreaded DLL.
Also, you should wrap your stdafx.h in this #ifdef (below) because simply including the afx headers with pragma import the debug libs which you don't want
We don't build an externally available Debug build of RealDWG, sorry about that.
#ifdef _DEBUG
#ifndef FULL_DEBUG
#define MY_WAS_DEBUG
#undef _DEBUG
#endif
#endif
// now include all MFC, CRT, STL headers
#ifdef MY_WAS_DEBUG
#define _DEBUG
#endif
Reply
11/15/2013 at 10:04 AM

---
