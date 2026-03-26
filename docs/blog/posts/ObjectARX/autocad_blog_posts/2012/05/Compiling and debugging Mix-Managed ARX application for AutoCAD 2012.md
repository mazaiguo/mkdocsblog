---
title: "Compiling and debugging Mix-Managed ARX application for AutoCAD 2012"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
description: "AutoCAD 2012 targets .NET Framework 4.0. This means you have to use VS2010 to debug your .NET application. ObjectARX still requires VS2008 SP1 comp..."
author: Autodesk
---
# Compiling and debugging Mix-Managed ARX application for AutoCAD 2012

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/compiling-and-debugging-mix-managed-arx-application-for-autocad-2012.html

## 文章内容

By Philippe Leefsma
  AutoCAD 2012 targets .NET Framework 4.0. This means you have to use VS2010 to debug your .NET application. ObjectARX still requires VS2008 SP1 compiler.
So can you clarify how is it possible to compile and debug a mix-managed application for AutoCAD 2012 ?
Solution
Concerning compiling and running a .Net or mix-managed application for AutoCAD 2012, you can still use VS2008 SP1, but as it doesn't support .Net Framework 4.0, you won't be able to run your application under the debugger.
A mixed-mode arx that can be debugged needs to be compiled with VS2010, platform toolset set to V90 and Framework 3.5 Targeted.
Once this is done, you can run AutoCAD form the debugger and break in managed or unmanaged code.
However, targeting Framework 3.5 in VS2010 is however not so straightforward.
Here are several techniques that expose how to achieve that:
Managed C++ projects will target the Framework 4.0 by default. The reason behind this design is that the VS2010 compiler cannot target Framework 2.0, 3.0 or 3.5. The VS2008 compiler must be used to target 2.0, 3.0 or 3.5. To make the converted C++ application build out of box, Microsoft decided to move the TargetFrameWorkVersion to 4.0 by default for C++ applications.
The Managed C++ applications can be retargeted to other frameworks by one of the following methods:
• Edit the vcxproj file and in the first property group ( <PropertyGroup Label="Globals">) add the following:
<TargetFrameworkVersion>v3.5</TargetFrameworkVersion>
• Open the VS2010 command line, set TargetFrameworkVersion=v3.5, and then start devenv.exe from the commandline. This will target all your C++ applications to v3.5 framework.
• Pass /p:TargetFrameworkVersion=v3.5 to MSBuild when building applications: MSBuild my.vcxproj /p:TargetFrameworkVersion=v3.5
Note that VS2008 has to be installed on the machine for the application to target 2.0, 3.0 or 3.5.

For C#/VB.Net applications, conversion does not change the target Framework version if the targeted Framework is installed on the machine. If the targeted Framework is not installed, you will have the choice of either downloading the required Framework or upgrading the target Framework to 4.0
Please refer to this post for other information about VS2010 and Platform Toolset.

