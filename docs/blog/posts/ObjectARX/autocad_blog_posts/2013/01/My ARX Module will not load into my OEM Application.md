---
title: "My ARX Module will not load into my OEM Application"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - OEM
  - ObjectARX
description: "I have created my ARX module with the OEM libraries, added it to the list in the 'My Modules' tab in the OEM Make Wizard, but when I run the produc..."
author: Autodesk
---
# My ARX Module will not load into my OEM Application

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/my-arx-module-will-not-load-into-my-oem-application.html

## 文章内容

By Fenton Webb
Issue
I have created my ARX module with the OEM libraries, added it to the list in the 'My Modules' tab in the OEM Make Wizard, but when I run the product, this module can't be loaded.  What is wrong?
Solution
1)  Make certain the ARX is indeed built with the OEM version of ObjectARX SDK included in the Arx subfolder of the OEM installation on your hard drive, and after stamping, make sure it depends on your <prod>.exe file.  Use the dependency walker (Depends.exe) to check this.
2)  Again, make certain the module is added to the list in the 'My Modules' tab in the Make Wizard.  A rebuild of the 'resources' is required when changes are made to the modules list.
3) if you are still stuck, start your OEM product in the Visual Studio debugger – do you see any issues displayed in the Output window?
4) If item 3 gives no hits, download the Windows SDK and utilize GFlags.exe by “Running as Administrator”… Turn “Loader Snaps” on for acad.exe, then retry your debugging session as in (3)
5) Failing that, try loading your ARX application in AOEM.exe to see if that works, if it does, then there is something wrong with your binding process.

