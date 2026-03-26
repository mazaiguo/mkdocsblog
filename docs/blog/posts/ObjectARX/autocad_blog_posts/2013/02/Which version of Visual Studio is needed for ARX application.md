---
title: "Which version of Visual Studio is needed for ARX application"
date: 2013-02-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "Depending on the version of AutoCAD you are writing your ARX application for you may need to use a different version of Visual Studio - the same ve..."
author: Autodesk
---
# Which version of Visual Studio is needed for ARX application

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/which-version-of-visual-studio-is-needed-for-arx-application.html

## 文章内容

By Adam Nagy
Depending on the version of AutoCAD you are writing your ARX application for you may need to use a different version of Visual Studio - the same version that the specific AutoCAD version was compiled with too.
You can simply check the Release Notes section of the readarx.chm file inside the specific version of ObjectARX SDK that corresponds to the version of AutoCAD you are writing your ARX application for (in case of AutoCAD 2013 check the ObjectARX SDK 2013)
E.g. in case of AutoCAD 2013 you would need to use Visual Studio 2010 with Service Pack 1
You may use a different version of Visual Studio for creating your project, but the actual compilation needs to be done using the compiler of the Visual Studio version that is pointed out in the readarx file. This blog post shows how: http://adndevblog.typepad.com/autocad/2012/05/about-visual-studio-2010-visual-studio-express-platform-toolset-and-autocad-2010-2012.html

