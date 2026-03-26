---
title: "Loading 3rd party ARXs into an OEM product"
date: 2013-02-01
categories:
  - AutoCAD C++
tags:
  - C++
  - OEM
  - ObjectARX
description: "Can I load a third party ARX module into my OEM product? For instance, an ARX that checks a hardware lock."
author: Autodesk
---
# Loading 3rd party ARXs into an OEM product

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/loading-3rd-party-arxs-into-an-oem-product.html

## 文章内容

by Fenton Webb
Issue
Can I load a third party ARX module into my OEM product? For instance, an ARX that checks a hardware lock.
Solution
No you can't. All ARX modules that are loaded into an OEM product MUST be bound specifically to that product. This means that they must be compiled and linked with the OEM version of ObjectARX.
The only exceptions to this are DBX modules, or Object Enablers. As an OEM developer, you have the option to allow unsecured DBX modules to be loaded into your product. If this is enabled (it is enabled by default), then your product can load third party DBX modules that will enable your product to display custom entities in the drawing instead of leaving them as proxy entities. However, if you do not want to allow object enablers to be used in your product, you can disable this feature in the OEM Make Wizard.

