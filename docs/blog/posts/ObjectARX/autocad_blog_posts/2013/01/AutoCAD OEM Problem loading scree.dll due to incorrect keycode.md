---
title: "AutoCAD OEM Problem loading scree.dll due to incorrect keycode"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
description: "Using the AutoCAD OEM make wizard I have created a new project following the steps in the tutorial. When I try to launch the exe an error message s..."
author: Autodesk
---
# AutoCAD OEM Problem loading scree.dll due to incorrect keycode

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/autocad-oem-problem-loading-screedll-due-to-incorrect-keycode.html

## 文章内容

By Fenton Webb
Issue
Using the AutoCAD OEM make wizard I have created a new project following the steps in the tutorial. When I try to launch the exe an error message saying "Problem loading SCREE.DLL resource file" occurs.
Solution
This error is normally due to an incorrect Keycode entered in the Project Information tab of the Make Wizard. As per the “Oem Developers Guide” documentation found in oemdev.chm, verify that you have entered the correct code. The format should be:
MMCCCCCDD
…where MM is the current month, CCCCC is the the last 5 digits of your Serial Number, and DD is the current day. So if your S/N was 112-98712345, and today was June 7th you would enter your code as: 061234507.
If it’s still not working, for single digit months, like June = 06, try cutting the 0 e.g. 61234507.
Note: In one case a corrupt aoem.exe caused a similar error. In that case, all projects created on that system would fail with an error regarding scree.dll. Also AutoCAD OEM would not run and a UAV would occur. The solution for this was to reinstall.

