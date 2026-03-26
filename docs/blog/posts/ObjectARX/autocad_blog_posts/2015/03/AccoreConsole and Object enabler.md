---
title: "AccoreConsole and Object enabler"
date: 2015-03-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "For AccoreConsole to recognize a custom entity in your drawing, it requires to load the object enabler just as AutoCAD does. If you already know th..."
author: Autodesk
---
# AccoreConsole and Object enabler

发布日期: 2015-03-01

原始链接: https://adndevblog.typepad.com/autocad/2015/03/accoreconsole-and-object-enabler.html

## 文章内容

By Balaji Ramamoorthy
For AccoreConsole to recognize a custom entity in your drawing, it requires to load the object enabler just as AutoCAD does. If you already know the full path of your object enabler (.dbx) you can have it configured for loading at startup by modifying the registry. Here is a sample registry file that would register the object enabler for AsdkPoly custom entity from the ObjectARX SDK :
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Autodesk\ObjectDBX\R20.0\Applications\AsdkPolyObj2.0]
"DESCRIPTION"="AsdkPolyObj2.0"
"LOADER"="D:\\Temp\\asdkpolyobj.dbx"
"LOADCTRLS"=dword:00000009
if you do not know the full path to the dbx, you can have the "LOADER" path set as simply "asdkpolyobj.dbx". In that case, AccoreConsole would try searching for it alongside the AccoreConsole exe path, the drawing path or one of the support paths. An easy way to have the support path configured for AccoreConsole is to launch AutoCAD and add the custom path to its "support file search path" using the Options command. AccoreConsole uses the same set of search paths that is already setup in AutoCAD.
It is important to have the right application name of your object enabler written to the registry. A simple way to determine this is to list the entities in the drawing. AccoreConsole will display the details of the proxy object and its Application name as shown here :

For some reason, if you do not want AccoreConsole to load the object enablers, start AutoCAD and set the DEMANDLOAD to 0 and close it. Further invocation of AccoreConsole will stop loading the object enablers even when the dbx is configured for loading at startup using the registry. Please do not use this unless you have a reason to do so. This may cause other issues as object enablers that AutoCAD requires for its working can also get ignored.

## 评论

**内容**: John.f said...
Hi,
Is there another way to load a dbx Under accoreconsole ?
Thanks.
Reply
04/28/2016 at 02:31 AM

---
