---
title: "Length of dictionary key names"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - C++
description: "The same rules apply to dictionary keys as to symbol table names: 255 characters or fewer, may be alphanumeric, may contain a dollar symbol ($), un..."
author: Autodesk
---
# Length of dictionary key names

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/length-of-dictionary-key-names.html

## 文章内容

By Gopinath Taget
The same rules apply to dictionary keys as to symbol table names: 255 characters or fewer, may be alphanumeric, may contain a dollar symbol ($), underscore (_) or hyphen (-). You can use the ARX function acdbSNValid() to check the validity of a symbol table name.
The allowable length is also dependent on the value of the sysvar "EXTNAMES". For more details, please refer to the online documentation.

