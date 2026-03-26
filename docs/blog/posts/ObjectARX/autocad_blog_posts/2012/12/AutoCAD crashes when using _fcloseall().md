---
title: "AutoCAD crashes when using _fcloseall()"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "AutoCAD is crashing when using fcloseall() function in an ARX application. The error message is: 'Internal error:SHLOAD SHSEEK 2'. If I use fclose(..."
author: Autodesk
---
# AutoCAD crashes when using _fcloseall()

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/autocad-crashes-when-using-_fcloseall.html

## 文章内容

by Fenton Webb
Issue
AutoCAD is crashing when using _fcloseall() function in an ARX application. The error message is: 'Internal error:SHLOAD SHSEEK 2'. If I use fclose() function instead of _fcloseall() function, then the problem does not occur.
Solution
First, you must make sure you link your ARX application using the C Runtime Library "Multithreaded DLL" , this is the recommended setting. AutoCAD is linked "Multithreaded DLL" so your ARX application uses the same instance of the C Runtime Library as AutoCAD.
This also means, both ACAD and your application share the same file pointers. If you call _fcloseall() in your application, you close all files that ACAD.EXE has opened.
The workaround is to *NOT* call _fcloseall(), or to compile & link your application "Multithreaded". In that case, your application will have its own C Runtime Library statically linked to your DLL

