---
title: "What are the ‘Load Controls’ in AutoCAD OEM"
date: 2013-07-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - OEM
  - ObjectARX
description: "The Load Controls section of the AutoCAD OEMMakeWizard define the demand loading required for your module."
author: Autodesk
---
# What are the ‘Load Controls’ in AutoCAD OEM

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/what-are-the-load-controls-in-autocad-oem.html

## 文章内容

by Fenton Webb
The Load Controls section of the AutoCAD OEMMakeWizard define the demand loading required for your module.
It relates directly to the ObjectARX AcadApp::LoadReasons enum, e.g.
struct AcadApp {
  enum LoadReasons {
    kOnProxyDetection = 0x01,
    kOnAutoCADStartup = 0x02,
    kOnCommandInvocation = 0x04,
    kOnLoadRequest = 0x08,
    kLoadDisabled = 0x10,
    kTransparentlyLoadable = 0x20,
    kOnIdleLoad = 0x40
  };
The Load Controls are used for all ObjectARX, ObjectDBX, .NET and Mixed Mode DLLs.

