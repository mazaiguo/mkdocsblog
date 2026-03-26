---
title: "ObjectARX 2021: Link Errors With VS 2019"
date: 2020-04-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Database
  - ObjectARX
  - Solid
description: "Q: We are getting link error compiling code for AutoCAD 2021 with Visual Studio 2019 and ObjectARX SDK 2021."
author: Autodesk
---
# ObjectARX 2021: Link Errors With VS 2019

发布日期: 2020-04-01

原始链接: https://adndevblog.typepad.com/autocad/2020/04/objectarx-2021-link-errors-with-vs-2019.html

## 文章内容

By Madhukar Moogala

Q: We are getting link error compiling code for AutoCAD 2021 with Visual Studio 2019 and ObjectARX SDK 2021.
A. The AutoCAD code for 3D modelling entities namely AcDbSubDMesh, AcDb3dSolid, AcDbRegion, AcDbAsmBody, AcDbShape etc are now ported to new library AcGeomEnt.lib
The declaration for almost all 3D entities are moved AcGeomEnt.lib, you need to link your source code with AcGeomEnt.lib which is present in <SDK>\lib-x64\
And, you may also need to appload  the AcGeomentObj.dbx in case if you are reading a drawing with 3D entities in side databases.

## 评论

**内容**: kim ji young said...
a
Reply
07/02/2020 at 12:28 AM

---
**内容**: Erphan Wadood said...
a
Reply
08/26/2020 at 12:43 AM

---
