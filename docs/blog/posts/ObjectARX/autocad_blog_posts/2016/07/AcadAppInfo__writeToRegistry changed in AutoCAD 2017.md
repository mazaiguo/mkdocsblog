---
title: "AcadAppInfo::writeToRegistry changed in AutoCAD 2017"
date: 2016-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
description: "In AcadAppInfo::writeToRegistry, the Boolean parameters are removed in AutoCAD 2017. This is because AutoCAD is not guaranteed to run with elevated..."
author: Autodesk
---
# AcadAppInfo::writeToRegistry changed in AutoCAD 2017

发布日期: 2016-07-01

原始链接: https://adndevblog.typepad.com/autocad/2016/07/acadappinfowritetoregistry-changed-in-autocad-2017.html

## 文章内容

By Virupaksha Aithal
In AcadAppInfo::writeToRegistry, the Boolean parameters are removed in AutoCAD 2017. This is because AutoCAD is not guaranteed to run with elevated permissions always and hence writing to current machine is always problematic through API. Now writeToRegistry works like writeToRegistry(false, true) of AutoCAD 2016. (Write to current user only and in AutoCAD section).

