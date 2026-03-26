---
title: "RealDWG and Civil3d Object Enabler"
date: 2017-10-01
categories:
  - Civil 3D
tags:
  - AutoCAD
  - Civil 3D
  - DWG
description: "If you are planning to extend your realDWG app to support C3D drawings, then it is must for your app to have access to Civil3D dbx modules to avoid..."
author: Autodesk
---
# RealDWG and Civil3d Object Enabler

发布日期: 2017-10-01

原始链接: https://adndevblog.typepad.com/autocad/2017/10/realdwg-and-civil3d-object-enabler.html

## 文章内容

By Madhukar Moogala
If you are planning to extend your realDWG app to support C3D drawings, then it is must for your app to have access to Civil3D dbx modules to avoid proxy objects.
The installer of Civil C3D OE 2018 was changed, it’s independent any other product now. Different with OE 2017.
From 2018 onwards OE installs files and registries to fixed location.
File: C:\Program Files\Autodesk\Autodesk AutoCAD Civil 3D 2018.1 Object Enabler 64 Bit
Registry: HKEY_LOCAL_MACHINE\SOFTWARE\Autodesk\ObjectDBX\R22.0
RealDWG  always loading .dbx from above registry key.
In theory, OE 2018 is available for all RealDWG application (with consistent version), We only verify the official target products (AutoCAD and family, InfraWorks, Navisworks Manager and simulation).
How to deploy Civil3d Object Enabler with our application ?
Civil3d Object Enabler is a free application, your free to redistribute along with your application.
How do I distribute the AutoCAD Civil 3D Object Enabler install?
The AutoCAD Civil 3D Object Enabler is free, and can be distributed to anyone who wants to view the civil objects in your drawings. However, the AutoCAD Civil 3D Object Enabler alone cannot display the objects in your drawings. You must have an installed copy of one of the Autodesk products listed in Using the AutoCAD Civil 3D Object Enabler.
One approach is to extract Civil3DOE.MSI from Civil3D_2018_OE_64Bit.EXE which you have downloaded from web. You can use ‘dark’ tool from Wix toolset for extraction. And wrap the extracted MSI in to your application.

C:\Program Files (x86)\WiX Toolset v3.11\bin>dark D:\Crap\Civil3D_2018_OE_64Bit.exe -x D:\Crap\Civil3D_2018_OE_64Bit

