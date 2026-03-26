---
title: "About Visual Studio 2010, Visual Studio Express, Platform Toolset and AutoCAD 2010-2012"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
description: "Here are some answers to the most frequently asked questions about Visual Studio, Platform Toolset and AutoCAD:"
author: Autodesk
---
# About Visual Studio 2010, Visual Studio Express, Platform Toolset and AutoCAD 2010-2012

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/about-visual-studio-2010-visual-studio-express-platform-toolset-and-autocad-2010-2012.html

## 文章内容

By Philippe Leefsma
  Here are some answers to the most frequently asked questions about Visual Studio, Platform Toolset and AutoCAD:
1/ Can we use VS2010 with Platform Toolset set to V90 to compile R18 (ObjectARX 2010/2011/2012) applications?
AutoCAD 2012 is built using VS 2010 with Platform Toolset set to v90, and is binary compatible with AutoCAD 2011. Therefore, you should be able to use this configuration without problem to create your ObjectARX 2010 and 2011 applications.
2/ To compile in VS2010 with Platform Toolset, it is needed to have VS2008?
Unfortunately yes, you need to have VS2008 installed on the same machine if you want to compile an application using Platform Toolset.
Here is an extract form Microsoft's website:
In addition to targeting the correct platform toolset, you must also have the associated version of Visual Studio installed. For example, to target the .NET Framework 2.0, 3.0, and 3.5, and the v90 platform toolset, you must have Visual Studio 2008 installed. However, you can use Visual C++ 2010 to do your development work, provided that you target the correct Framework version and platform toolset.
Extracted from here: http://msdn.microsoft.com/en-us/library/ff770576.aspx
3/ To compile ObjectARX/.Net applications, is the Visual Studio Express version enough?
VS Express can compile valid ObjectARX/.Net applications, however it is not a supported compiler (Visual Studio 2008 SP1 is the minimal supported compiler for AutoCAD 2010 - 2012).
Also apart from the IDE limitations, such as no support for debugging and 64-bit, VS Express doesn’t ship with the MFC Framework, which is not free, so you are likely to get very limited at some point if you plan to do C++ development.

## 评论

**内容**: petcon said...
vs2010可通吃vc6 vc7 vc7.1 vc8 vc9 毫无压力
Reply
05/10/2012 at 10:47 PM

---
**内容**: petcon said...
use this magic tool!!
http://daffodil.codeplex.com/
Reply
05/17/2012 at 10:08 PM

---
