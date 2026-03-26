---
title: "Object enabler's interop assembly references the latest AutoCAD interop dll instead of the version the COM wrapper was built with"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - COM
  - COM Interop
  - Plugin
description: "I created a custom entity and made sure that its COM wrapper is using the AutoCAD 2010 tlb's, but when I'm trying to use it from a .NET AddIn I run..."
author: Autodesk
---
# Object enabler's interop assembly references the latest AutoCAD interop dll instead of the version the COM wrapper was built with

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/object-enablers-interop-assembly-references-the-latest-autocad-interop-dll-instead-of-the-version-the-com-wrapper-was-built.html

## 文章内容

By Adam Nagy
I created a custom entity and made sure that its COM wrapper is using the AutoCAD 2010 tlb's, but when I'm trying to use it from a .NET AddIn I run into problems for the interop dll created for it automatically by Visual Studio is referencing the AutoCAD 2011 interop dll's and so I get an error when compiling my project:
"error BC32206: The project currently contains references to more than one version of Autodesk.AutoCAD.Interop.Common, a direct reference to version 18.0.0.0 and an indirect reference (through 'AEN1MyLineOE3Lib.MyLineCom') to version 18.1.0.0. Change the direct reference to use version 18.1.0.0 (or higher) of Autodesk.AutoCAD.Interop.Common."
If I uninstall AutoCAD 2011, then of course everything is fine, but I'd prefer a different solution.
Solution
When you reference a tlb from Visual Studio then it's using tlbimp in the background to create an interop dll for it. If we do it ourselves then we can check what's going on during the interop making process using the /verbose option of tlbimp.exe.

As you can see the primary interop assembly is being used - which is from AutoCAD 2011.
However with the /reference option you can set which interop assembly to use:

Now that the interop assembly used the AutoCAD 2010 interop assembly, everything was fine when I referenced my interop assembly in the .NET AddIn.

