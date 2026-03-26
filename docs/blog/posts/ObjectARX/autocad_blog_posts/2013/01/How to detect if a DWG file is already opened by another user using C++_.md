---
title: "How to detect if a DWG file is already opened by another user using C++?"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - DWG
  - Plot
description: "You can check if a DWG file is already opened or not, using a file mode for "append." For example, the following code demonstrates the usage:"
author: Autodesk
---
# How to detect if a DWG file is already opened by another user using C++?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-detect-if-a-dwg-file-is-already-opened-by-another-user-using-c.html

## 文章内容

By Gopinath Taget
You can check if a DWG file is already opened or not, using a file mode for "append." For example, the following code demonstrates the usage:
ACHAR fileName[] = L"myDrawing.dwg";
void fileInUse()
{
ofstream fp(fileName, ios::app) ;
 if(!fp) {
  acutPrintf(L"%s is IN USE.\n", fileName);
}
 else {
  acutPrintf(L"%s is NOT in use.\n", fileName);
  fp.close();
}
}

