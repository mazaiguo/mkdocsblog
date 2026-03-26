---
title: "Preventing the display of the proxy information dialog"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - DXF
  - ObjectARX
description: "Users do not like the message that is displayed when a custom object does not have its owning DBX/ARX application present. Is there any way to crea..."
author: Autodesk
---
# Preventing the display of the proxy information dialog

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/preventing-the-display-of-the-proxy-information-dialog.html

## 文章内容

By Philippe Leefsma
Users do not like the message that is displayed when a custom object does not have its owning DBX/ARX application present. Is there any way to create an object such that this message is never displayed when our application is not loaded?
Solution
It is possible since AutoCAD 2004 and later versions. There is a proxy entity flag introduced for this purpose: AcDbProxyEntity::kDisableProxyWarning = 0x400. You can use this flag in conjunction with other proxy flags within the ACRX_DXF_DEFINE_MEMBERS macro. Please see the online doc for the description: ObjectARX Reference --> Macros --> AcRx --> ACRX_DXF_DEFINE_MEMBERS.

