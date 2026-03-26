---
title: "Create multi-sheet DWF using DSD files"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - Unicode
description: "A DSD file is a text configuration file that the AutoCAD publisher functionality honors. You can create it programmatically or using the PUBLISH UI..."
author: Autodesk
---
# Create multi-sheet DWF using DSD files

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/create-multi-sheet-dwf-using-dsd-files.html

## 文章内容

By Gopinath Taget
A DSD file is a text configuration file that the AutoCAD publisher functionality honors. You can create it programmatically or using the PUBLISH UI. It typically looks something like this:
---------copy the following in a ASCII file with extension .dsd--------
[DWF6Version]
Ver=1
[DWF6Sheet:3D House-Model]
DWG=C:\Program Files\Autodesk\AutoCAD 2009\Sample\3D House.dwg
Layout=Model
Setup=
[DWF6Sheet:3D House-Layout1]
DWG=C:\Program Files\Autodesk\AutoCAD 2009\Sample\3D House.dwg
Layout=Layout1
Setup=
[DWF6Sheet:3D House-Layout2]
DWG=C:\Program Files\Autodesk\AutoCAD 2009\Sample\3D House.dwg
Layout=Layout2
Setup
[Target]
Type=1
DWF=c:\temp\multi.dwf
OUT=
PWD=
-----------------------------------------------------------------------------------------------------------
Assuming the above configuration is stored in "c:\temp\multi.dsd" - you can then drive the PUBLISH command using:
(command "_-PUBLISH" "C:/TEMP/multi.dsd")
It is recommended that you set FILEDIA to 0 if running this from LISP (you may need to do the equivalent from OARX or VBA):
(setq oldFD (getvar "FILEDIA"))
(setvar "FILEDIA" 0)
(command "_-PUBLISH" "C:/TEMP/multi.dsd")
(setvar "FILEDIA" oldFD)

