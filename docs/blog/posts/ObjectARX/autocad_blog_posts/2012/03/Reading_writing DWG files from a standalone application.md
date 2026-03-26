---
title: "Reading/writing DWG files from a standalone application"
date: 2012-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - DWG
description: "A commonly asked question via ADN support and on our public forums is how to read or write DWG files from a standalone executable without having to..."
author: Autodesk
---
# Reading/writing DWG files from a standalone application

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/readingwriting-dwg-files-from-a-standalone-application.html

## 文章内容

By Stephen Preston
A commonly asked question via ADN support and on our public forums is how to read or write DWG files from a standalone executable without having to install AutoCAD on the same machine.
This can be done by licensing the Autodesk RealDWG SDK. This SDK allows you to build DWG capability into your own application without having to install AutoCAD on the same machine and automate it from your executable. RealDWG is essentially the DatabaseServices part of the AutoCAD .NET API (or AcDb part of ObjectARX), along with supporting namespaces.
RealDWG doesn’t include AutoCAD ‘editor’ APIs, and so you can’t easily use it for viewing and plotting DWG files (unless you do a lot of work implementing your own graphics/plotting engine). If your customer won’t buy AutoCAD for that, but they need viewing and plotting with the same fidelity that AutoCAD provides, then consider AutoCAD OEM. AutoCAD OEM is a customizable AutoCAD that you can ‘brand’ as your own application, and from which you can expose a subset of the full AutoCAD functionality, and also add your own additional functionality.  AutoCAD LT and DWG TrueView are examples of Autodesk products built using AutoCAD OEM.
Both RealDWG and AutoCAD OEM are licensed technologies. You can find out more from the Tech Soft 3D website. (Tech Soft 3D are  our global distributor for RealDWG and AutoCAD OEM).
Here’s a video on RealDWG programming basics, recorded by DevTech’s Adam Nagy.

## 评论

**内容**: Fenton Webb said...
Extra Notes:
1) Since RealDWG 2012 the security attributes are not needed
2) Visual Studio versions have changed to Visual Studio 2010
Reply
07/02/2012 at 07:12 PM

---
**内容**: Carl said...
Hi there! I'm trying to build an in-house batch plotter utility - I would like it to run outside of Autocad, but I CAN have Autocad installed - I don't need a full RealDWG solution. Is this possible or does external access have to be RealDWG?
Reply
12/18/2013 at 02:21 PM

---
**内容**: Peter said...
RealDWG is NOT an option. The pricing is absolutely ridiculous!
AutoCAD is now affordable but without a DWG manipulator (independently of AutoCAD), managing a large number of files is impractical.
We need an affordable DWG solution!
Reply
05/22/2016 at 01:48 PM

---
**内容**: Madhukar Moogala said in reply to Peter...
Hi Peter,
I'm not going to argue with your opinion on the price. Either your business model gives you an ROI from licensing RealDWG or it doesn't.
However, this is now a very old article. RealDWG is still alive and well, but we have recently introduced another option - AutoCAD I/O. AutoCAD I/O is AcCoreConsole (think headless AutoCAD) running on a server - to which you can submit batch jobs. AutoCAD I/O has an advantage over RealDWG, because it can also plot. The service is currently in Beta and is therefore free. Eventually, possibly as early as next month, Autodesk will announce a pricing model, which will be usage based so you only pay for what you expect to use. See https://developer.autodesk.com/api/autocadio/ for more info.
Cheers,
Stephen
Reply
05/23/2016 at 04:48 PM

---
