---
title: "Silent install of AutoCAD OEM"
date: 2013-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
description: "If you are trying to silently install your AutoCAD OEM maybe because it’s a prerequisite of another installer, then here’s how to do it…"
author: Autodesk
---
# Silent install of AutoCAD OEM

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/silent-install-of-autocad-oem.html

## 文章内容

by Fenton Webb
If you are trying to silently install your AutoCAD OEM maybe because it’s a prerequisite of another installer, then here’s how to do it…
setup.exe /t /q /c AOEM: INSTALLDIR="C:\Program Files\MyApp" InstallLevel=5 
In fact, that line can also be used to install any Autodesk product silently… Just substitute AOEM for the main section in the setup.ini file… e.g. AutoCAD=ACAD

