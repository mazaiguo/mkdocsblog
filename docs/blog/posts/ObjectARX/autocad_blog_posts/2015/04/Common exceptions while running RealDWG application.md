---
title: "Common exceptions while running RealDWG application"
date: 2015-04-01
categories:
  - AutoCAD C++
tags:
  - C++
  - DWG
  - ObjectARX
description: "In this blog post, we will look at a few common setup related issues that can cause problems in running your RealDWG application."
author: Autodesk
---
# Common exceptions while running RealDWG application

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/common-exceptions-while-running-realdwg-application.html

## 文章内容

By Balaji Ramamoorthy
In this blog post, we will look at a few common setup related issues that can cause problems in running your RealDWG application.
System.IO.FileNotFoundException : This exception get thrown usually because your RealDwg Application does not find the dependent dlls. To ensure your RealDwg application accesses the right DLLs is to create an installer for your application with all the dependencies and then installing your application in a clean test machine and test it. But, for testing purposes during development, you can place your RealDWG application in the RealDWG root folder and test it. It is easier to simply set the build output path in the Visual Studio solution to place the output in the RealDWG root folder.
Also, ensure that the [RealDWG root path], [RealDWG root path]\Fonts and [RealDWG root path]\Support folder paths are added to the system's PATH environment variable. You may need to restart Visual Studio if you made the environment variable change when Visual Studio was open.
System.InvalidProgramException : RealDWG SDK has two versions of acdbmgd.dll just as the ObjectARX SDK does. The dll in RealDWG 2016\Inc folder has its executable code removed and the one in the RealDWG root folder is the unmodified dll. When referencing the "acdbmgd.dll" in your VisualStudio project from the Inc folder, remember to set "Copy Local" property to false for the reference. This is to prevent Visual Studio from replacing the "acdbmgd.dll" in the RealDWG root folder with the one found in "Inc" folder. If this happens, your application can throw a System.InvalidProgramException and the only way to fix it would be to find the "acdbmgd.dll" from the RealDWG install CD and copy it to the RealDWG root folder.

## 评论

**内容**: gabriel sallum said...
Hi, Thanks for the blog. I've have been fighting with this for some time now.
The problem is that I cannot seem to get this going correctly.
As per your instructions, I seem to fall into the category of having to re-copy the Dll back into the ReadDWG dir. My issue is that on the RealDWG dir the "acdbmgd.dll" is already one that has 6.3 megs, on the install Distribution, it seems that there are a couple of versions but most fall under 2 categories, one with small (kb) size and another with a lager ~6mb size. As previously stated, I fall in the category of having the larger one in my DWG folder. So I guess I need to copy the smaller one (kb sized) into the RealDWG directory ?
thanks,
Its appreciated
Reply
06/09/2016 at 07:12 AM

---
