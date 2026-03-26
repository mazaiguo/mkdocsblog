---
title: "Localizing AutoCAD / AutoCAD OEM in other languages"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - OEM
description: "Can I localize AutoCAD / AutoCAD OEM in other languages?"
author: Autodesk
---
# Localizing AutoCAD / AutoCAD OEM in other languages

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/localizing-autocad-autocad-oem-in-other-languages.html

## 文章内容

By Philippe Leefsma
Q:
Can I localize AutoCAD / AutoCAD OEM in other languages?
A:
AutoCAD and AutoCAD OEM are built the same way with regards to localization. Localizable components in AutoCAD are:
- Menu
- MNL
- Lisp
- DCL
- PGP
- Pattern file .PAT
- Linetype file .LIN
- Shape/Font
- Help file (.hlp, .chm)
- Templates
- AutoCAD Core (Windows resource file + linked XMX file)
- Drivers (Windows resource file)
- Externsions (Windows resource file and/or XMX file)
- Others (.htm, .txt, .bmp, ...)
In each of these components there are localizable and non localizable strings. Forgetting to localize one string or localizing one non-localizable string would possibly break the component feature. So it must be done carefully.
All components can be localized by third party if they have an agreement with AutoCAD to do this, excepting few. All the components using a XMX file cannot be localized because the XMX format is a binary encrypted Autodesk file format and Autodesk does not expose any API or tools to work with XMX file.
One solution to this problem is to replace the XMX file by a localized version of the same XMX file from another AutoCAD version if it is made from the same build. It must be from the same build (or similar) to ensure the same number of localized messages contained in the XMX file.
However, this solution will work for all except in one case. The AutoCAD core component XMX file cannot be exchanged by another one, because it is linked to the EXE it was compiled for. For example a German XMX file will not work on a French AutoCAD release. Since you can replace the resource file, but not the XMX file, it means that the AutoCAD core will be partially localized. Most command prompts will remain in the original language unless autodesk provides the proper localized XMX file linked with that particular AutoCAD release.

