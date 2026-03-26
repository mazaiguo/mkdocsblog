---
title: "MFC: Problem with CAcModuleResourceOverride"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
description: "You might find that when you use the CAcModuleResourceOverride object to switch the default resource handle (AutoCAD resource handle) to your appli..."
author: Autodesk
---
# MFC: Problem with CAcModuleResourceOverride

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/mfc-problem-with-cacmoduleresourceoverride.html

## 文章内容

By Gopinath Taget
You might find that when you use the CAcModuleResourceOverride object to switch the default resource handle (AutoCAD resource handle) to your application resource file, you cannot call AutoCAD or ARX function such as acedGetFileD().
This is because you switched the default resource file (the AutoCAD resource file) to your application resource file using the CAcModuleResourceOverride object. Then, inside a function (where the resource handle still points to your application resource file), you call an AutoCAD function that needs to access the AutoCAD resources (not yours). As you switched it, the acedGetFileD() tries to find the dialog template it needs, and fails. To solve this problem, restore the AutoCAD resource handle as the default one. See the following sample code:
HINSTANCE hOld =AfxGetResourceHandle () ; // Optional
AfxSetResourceHandle (acedGetAcadResourceInstance ()) ;
acedGetFileD(...) ;
AfxSetResourceHandle (hOld) ; // Optional

