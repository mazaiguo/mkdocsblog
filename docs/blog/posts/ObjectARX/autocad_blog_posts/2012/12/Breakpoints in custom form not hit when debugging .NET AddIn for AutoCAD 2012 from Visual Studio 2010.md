---
title: "Breakpoints in custom form not hit when debugging .NET AddIn for AutoCAD 2012 from Visual Studio 2010"
date: 2012-12-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Plugin
description: "I am trying to create .net add-in based on AutoCAD 2012 with Visual Studio 2010. The breakpoints in common classed can be hit, but those in custom ..."
author: Autodesk
---
# Breakpoints in custom form not hit when debugging .NET AddIn for AutoCAD 2012 from Visual Studio 2010

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/breakpoints-in-custom-form-not-hit-when-debugging-net-addin-for-autocad-2012-from-visual-studio-2010.html

## 文章内容

By Daniel Du
Issue
I am trying to create .net add-in based on AutoCAD 2012 with Visual Studio 2010. The breakpoints in common classed can be hit, but those in custom forms cannot be hit. I looked into this post http://through-the-interface.typepad.com/through_the_interface/2010/04/hitting-breakpoints-in-net-class-libraries-while-debugging-with-visual-studio-2010.html.But it does not help. I tried “Autodesk.Autodesk.ApplicationServices.Application.ShowModalDialog(oForm)” and “oForm.ShowDialog()”, same result. Is there anything else I can do?
Solution
VS2010 debugger does not work well with fiber; the solution is to turn off fiber in AutoCAD .
If you do not know yet, fibers are being deprecated, as Microsoft is dropping Windows support for fibers. For more information of fibers, please refer to http://msdn.microsoft.com/en-us/library/ms682661(v=vs.85).aspx
To turn it off, you can set NEXTFIBERWORLD to 0, close all documents, and AutoCAD will run fiberless in subsequent documents.  The system environment variable FIBERWORLD can show the current status of fiber.
Another thing should mention is: using NEXTFIBERWORLD = 0 the Ribbon might stop working – when you click on a button on ribbon, nothing happens. You can use command line as a workaround.
It applies to other AutoCAD vertical products like Civil 3D, ACA, AME, etc. as well.

## 评论

**内容**: Matus Brlit said...
When is Autodesk planning to get rid of fibers? Because with FIBERWORLD=0 there are issues that are hard to counter.
Reply
12/19/2012 at 03:55 AM

---
**内容**: Madhukar Moogala said in reply to Matus Brlit...
Sorry Matus - we can't comment on future plans for our products in a public forum. If you're an ADN member, then you can ask such questions in private using DevHelp Online, or maybe you've already asked them at one of our Developer Day conferences.
Obviously, we're working on this, otherwise we wouldn't have created the FIBERWORLD and related sysvars. If/when we do ship AutoCAD without fibers, we'd obviously be fixing those fiberless operation issues we know about.
Reply
12/19/2012 at 11:25 AM

---
**内容**: Jeff Evans said...
No fiber in future? does it mean that there are multithreads in Autocad?
Reply
01/08/2014 at 07:45 AM

---
