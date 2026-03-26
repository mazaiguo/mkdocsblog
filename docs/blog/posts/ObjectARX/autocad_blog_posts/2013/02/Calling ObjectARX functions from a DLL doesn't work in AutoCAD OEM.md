---
title: "Calling ObjectARX functions from a DLL doesn't work in AutoCAD OEM"
date: 2013-02-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - OEM
  - ObjectARX
description: "When I try to use an ObjectARX function from a DLL, it doesn't seem to execute. This works fine in AutoCAD but not OEM, why?"
author: Autodesk
---
# Calling ObjectARX functions from a DLL doesn't work in AutoCAD OEM

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/calling-objectarx-functions-from-a-dll-doesnt-work-in-autocad-oem.html

## 文章内容

by Fenton Webb
Issue
When I try to use an ObjectARX function from a DLL, it doesn't seem to execute. This works fine in AutoCAD but not OEM, why?
Solution
This is the intended behavior. ObjectARX API functions can only be called from ARX modules which have been properly bound to the OEM product. A simple workaround for this is to turn the DLL into an ARX. This can be done by implementing a basic acrxEntryPoint function and linking the DLL with the RXAPI.LIB library. Now you can rename the file to have an ARX extension and it can be bound to the OEM product, allowing the ARX functions to work properly.

