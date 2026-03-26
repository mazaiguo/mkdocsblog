---
title: "Using AcDbRasterImageDefFileAccessReactor"
date: 2012-10-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "I want to use an AcDbRasterImageDefFileAccessReactor to receive notifications when images are attached, detached, reloaded etc. using the Image Com..."
author: Autodesk
---
# Using AcDbRasterImageDefFileAccessReactor

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/using-acdbrasterimagedeffileaccessreactor.html

## 文章内容

By Philippe Leefsma
Q:
I want to use an AcDbRasterImageDefFileAccessReactor to receive notifications when images are attached, detached, reloaded etc. using the Image Command. Is there an example that shows how to implement and use the AcDbRasterImageDefFileAccessReactor class?
A:
The attached ObjectARX example shows how to implement Image dictionary notifications using the AcDbRasterImageDefFileAccessReactor class. The reactor is attached when the ARX application is loaded, and removed when the application is unloaded.
ArxRasterDefReactor.zip

