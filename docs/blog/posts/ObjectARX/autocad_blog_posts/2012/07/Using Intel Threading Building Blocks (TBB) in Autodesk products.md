---
title: "Using Intel Threading Building Blocks (TBB) in Autodesk products"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Plugin
description: "My AddIn is using Intel Threading Building Blocks (version 2.1.2009.201). It seems to load fine but later on crashes the application."
author: Autodesk
---
# Using Intel Threading Building Blocks (TBB) in Autodesk products

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/using-intel-threading-building-blocks-tbb-in-autodesk-products.html

## 文章内容

By Adam Nagy
My AddIn is using Intel Threading Building Blocks (version 2.1.2009.201). It seems to load fine but later on crashes the application.
Solution
More and more Autodesk products are using the same graphics system, One Graphics System (OGS), which takes advantage of Intel Threading Building Blocks that are available through tbb.dll and tbbmalloc.dll.
Revit has been using the above dll's since at least release 2010. AutoCAD and so its verticals have been using it since version 2011. Inventor starts using it in release 2012. Etc.
If your AddIn is not using the same version of the above dll's as the Autodesk product it is loaded into, then it can cause unexpected results, including crashing the application.
So, please make sure that you are using the appropriate version of these dll's. You can just look in the application folder of the specific product and check the version number of tbb.dll. E.g. in case of AutoCAD 2011 it's 2.1.2009.325

