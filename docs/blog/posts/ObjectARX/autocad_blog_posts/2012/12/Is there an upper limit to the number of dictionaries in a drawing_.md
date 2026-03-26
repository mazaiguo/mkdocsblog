---
title: "Is there an upper limit to the number of dictionaries in a drawing?"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Database
description: "There is no hard-coded limit to the number of dictionaries you can have in an AcDbDatabase, although it is recommended that they be nested. Inside ..."
author: Autodesk
---
# Is there an upper limit to the number of dictionaries in a drawing?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/is-there-an-upper-limit-to-the-number-of-dictionaries-in-a-drawing.html

## 文章内容

By Gopinath Taget
There is no hard-coded limit to the number of dictionaries you can have in an AcDbDatabase, although it is recommended that they be nested. Inside the named objects dictionary, you should have a top level dictionary using your company's developer ID (typically four characters) as a prefix in order to prevent conflicts with names. Underneath this top-level dictionary, it is recommended that application-specific dictionaries are maintained and that they be nested, if necessary.

