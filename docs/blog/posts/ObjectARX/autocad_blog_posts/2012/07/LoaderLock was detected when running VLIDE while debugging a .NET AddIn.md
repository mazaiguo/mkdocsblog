---
title: "LoaderLock was detected when running VLIDE while debugging a .NET AddIn"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Plugin
description: "I get a "LoderLock was detected" with the below information when I run command VLIDE while debugging my .NET AddIn: "Attempting managed execution i..."
author: Autodesk
---
# LoaderLock was detected when running VLIDE while debugging a .NET AddIn

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/loaderlock-was-detected-when-running-vlide-while-debugging-a-net-addin.html

## 文章内容

By Adam Nagy
I get a "LoderLock was detected" with the below information when I run command VLIDE while debugging my .NET AddIn: "Attempting managed execution inside OS Loader lock. Do not attempt to run managed code inside a DllMain or image initialization function since doing so can cause the application to hang." What could I do?
Solution
You can simply disable the Loader Lock detection in this case in Visual Studio:
Go to Debug > Exceptions... > Managed Debugging Assistants > LoaderLock and untick it.

## 评论

**内容**: mississauga seo agency said...
You can simply disable the Loader Lock detection in this case in Visual Studio:
Reply
05/11/2023 at 07:52 AM

---
