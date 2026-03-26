---
title: "ObjectARX Wizard does not install on Windows Vista / Windows 7"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
  - ObjectARX
description: "Windows Vista / Windows 7 includes a much tighter security mechanism for controlling script modules that are run from it. Because the ObjectARX Wiz..."
author: Autodesk
---
# ObjectARX Wizard does not install on Windows Vista / Windows 7

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/objectarx-wizard-does-not-install-on-windows-vista-windows-7.html

## 文章内容

By Virupaksha Aithal
Windows Vista / Windows 7 includes a much tighter security mechanism for controlling script modules that are run from it. Because the ObjectARX Wizard runs a VBScript to initialise some of its components, Windows Vista or Windows 7 immediately disables the VBScript routines from running and thus aborts the installation.
To solve the problem, you must temporarily disable Windows Vista or Windows 7 UAC (User Account Control).
Once installed, you must re-enable UAC.

## 评论

**内容**: Kapil said...
You can also try troubleshoot compatibility... it worked for me.
Reply
08/07/2012 at 05:21 AM

---
