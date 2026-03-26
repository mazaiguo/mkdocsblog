---
title: "Using acutPrintf in a Regular MFC DLL"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Plot
description: "If you are using an MFC Regular DLL, you have to manage module state switching when calling acutPrintf(). You need to do something like this:"
author: Autodesk
---
# Using acutPrintf in a Regular MFC DLL

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/using-acutprintf-in-a-regular-mfc-dll.html

## 文章内容

By Augusto Goncalves
If you are using an MFC Regular DLL, you have to manage module state switching when calling acutPrintf(). You need to do something like this:
void arx_func() {
  // Put AFX_MANAGE_STATE in its own scope
  {
    AFX_MANAGE_STATE(AfxGetAppModuleState());
    acutPrintf(L"\nHi!");
  } // End of scope
    // More of your code
}

