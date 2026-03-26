---
title: "Setup Requirements For AutoCAD OEM 2017"
date: 2016-05-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - OEM
description: "We have been receiving queries on OEM 2017 makewizard, to reach large audience I posting the necessary Visual studio 2015 set up requirements neede..."
author: Autodesk
---
# Setup Requirements For AutoCAD OEM 2017

发布日期: 2016-05-01

原始链接: https://adndevblog.typepad.com/autocad/2016/05/setup-requirements-for-autocad-oem-2017.html

## 文章内容

By Madhukar Moogala 
We have been receiving queries on OEM 2017 makewizard, to reach large audience I posting the necessary Visual studio 2015 set up requirements needed for successful build of OEM application.
Problem: ‘Next’ button is greyed out in OEM makewizard 2017?
Developing Environment for AutoCAD \OEM 2017 is Visual Studio 2015.
If OEM application doesn’t find VC++ or MFC tools, application disables ‘NEXT’ control.
In Visual Studio 2015, Visual C++ is not installed by default. When installing, be sure to choose Custom installation and then choose the C++ components you require. Or, if Visual Studio is already installed, choose File | New | Project | C++ and you will be prompted to install the necessary components.
You have to install MFC and VC++ tools, please follow this blog.
http://blogs.msdn.com/b/vcblog/archive/2015/07/24/setup-changes-in-visual-studio-2015-affecting-c-developers.aspx
Essentially, the three tools that the OemMakeWizard is looking for are: rc.exe, nmake.exe and sn.exe. 
Nmake.exe gets installed in VC\tools.   
It actually searches for all three of these on the search path. But it runs vcvars32.bat to  setup that search path.

## 评论

**内容**: Alexander Rivilis said...
>>>Developing Environment for AutoCAD \OEM 2017 is Visual Studio 2017.<<<
I think this is a typo and AutoCAD OEM 2017 require Visual Studio 2015.
Reply
05/23/2016 at 08:10 AM

---
**内容**: Madhukar Moogala said...
Thanks Alexander, I corrected post now.. :)
Reply
05/23/2016 at 09:03 PM

---
