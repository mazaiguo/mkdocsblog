---
title: "SDI mode deprecated in AutoCAD"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - COM Interop
  - ObjectARX
description: "I've just run into the topic Support MDI Operations under ObjectARX Application Interoperability Guidelines > ObjectARX Programming Practices in th..."
author: Autodesk
---
# SDI mode deprecated in AutoCAD

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/sdi-mode-deprecated-in-autocad.html

## 文章内容

By Adam Nagy
I've just run into the topic Support MDI Operations under ObjectARX Application Interoperability Guidelines > ObjectARX Programming Practices in the ObjectARX Reference, which says:
ObjectARX applications must support MDI mode. SDI mode has been deprecated and will be removed in a future release.
How long can I still use SDI mode?
Solution
SDI mode has been deprecated for quite a few releases now and might get removed in any of the future versions. We cannot tell for sure which exact version that might be.
Therefore, we would encourage you to update your code so that it supports and runs in MDI mode.

