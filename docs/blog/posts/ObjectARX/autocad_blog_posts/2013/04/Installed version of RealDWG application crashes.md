---
title: "Installed version of RealDWG application crashes"
date: 2013-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
description: "My application runs fine on the development machine but the installed version crashes on a clean test machine."
author: Autodesk
---
# Installed version of RealDWG application crashes

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/installed-version-of-realdwg-application-crashes.html

## 文章内容

By Adam Nagy
Issue
My application runs fine on the development machine but the installed version crashes on a clean test machine.
If I only reference my version of HostApplicationServices inside a try-catch (Autodesk.AutoCAD.Runtime.Exception), then the installed version pops up this error:
So it seems that some components are missing. When I checked the sample that comes with the Introduction to RealDWG Programming DevTV presentation, that had the same problem. 
Solution
The sample is written in VS 2005. When you migrate it to VS 2008, then for some reason Visual Studio does not automatically pull in the policy merge modules that come with the included merge modules (*.msm)
As you'll find in many articles on the net, most Visual Studio merge modules require the corresponding policy merge modules.
So just make sure that those are also added to your merge module or installer project:

