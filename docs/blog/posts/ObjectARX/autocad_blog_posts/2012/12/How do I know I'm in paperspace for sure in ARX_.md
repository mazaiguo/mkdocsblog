---
title: "How do I know I'm in paperspace for sure in ARX?"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
description: "The following code snippet would do the job."
author: Autodesk
---
# How do I know I'm in paperspace for sure in ARX?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-do-i-know-im-in-paperspace-for-sure-in-arx.html

## 文章内容

By Gopinath Taget
The following code snippet would do the job.
BOOL purePaperSpace () {
 struct resbuf res ;
acedGetVar (L"tilemode", &res) ;
 int tilemode =res.resval.rint ;
acedGetVar (L"cvport", &res) ;
 int cvport =res.resval.rint ;
 return (tilemode == 0 && cvport == 1) ;
}

