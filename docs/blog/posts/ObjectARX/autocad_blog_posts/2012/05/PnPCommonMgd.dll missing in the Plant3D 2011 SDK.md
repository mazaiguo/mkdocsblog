---
title: "PnPCommonMgd.dll missing in the Plant3D 2011 SDK"
date: 2012-05-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - Plant 3D
description: "I am trying to use PnPXDbDatasource as in the "Data Objects Extensions" example from the Plant SDK 2011 Developer Guide.  I am getting errors about..."
author: Autodesk
---
# PnPCommonMgd.dll missing in the Plant3D 2011 SDK

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/pnpcommonmgddll-missing-in-the-plant3d-2011-sdk.html

## 文章内容

By Wayne Brill
Issue
I am trying to use PnPXDbDatasource as in the "Data Objects Extensions" example from the Plant SDK 2011 Developer Guide.  I am getting errors about a missing reference to an assembly named PnPCommonMgd for the type Autodesk.ProcessPower.Common.PnPCollectionItem. I am unable to find PnPCommonMgd.dll in the Plant3D SDK where the other assemblies are located. Is this assembly available?
Solution
PnPCommonMgd.dll is missing from the Plant3D SDK. It does however install with Plant3D P&ID product and can be referenced from the install directory:
C:\Program Files\Autodesk\AutoCAD Plant 3D 2011

