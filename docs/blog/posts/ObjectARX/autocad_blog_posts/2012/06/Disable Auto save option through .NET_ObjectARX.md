---
title: "Disable Auto save option through .NET/ObjectARX"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
description: "Set the system variable “SAVETIME” to 0 to disable the Auto save option in AutoCAD as shown below."
author: Autodesk
---
# Disable Auto save option through .NET/ObjectARX

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/disable-auto-save-option-through-netobjectarx.html

## 文章内容

By Virupaksha Aithal
Set the system variable “SAVETIME” to 0 to disable the Auto save option in AutoCAD as shown below.
.NET
Application.SetSystemVariable("SAVETIME", 0);
ObjectARX
struct resbuf res;
res.restype=RTSHORT;
res.resval.rint=0;
acedSetVar(L"SAVETIME",&res);

