---
title: "How to Deploy OEM with SCCM"
date: 2017-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
description: "Large corporations prefer to deploy custom AutoCAD OEM suites using SCCM, here is preferred way to do, in the configuration manager tool"
author: Autodesk
---
# How to Deploy OEM with SCCM

发布日期: 2017-02-01

原始链接: https://adndevblog.typepad.com/autocad/2017/02/how-to-deploy-oem-with-sccm.html

## 文章内容

By Madhukar Moogala
Large corporations prefer to deploy custom AutoCAD OEM suites using SCCM, here is preferred way to do, in the configuration manager tool
you need to enter
setup.exe /t /q /c AOEM: INSTALLDIR="C:\Program Files\MyApp" InstallLevel=5
Where MyApp is OEM program name.
From AutoCAD OEM 2023-
We have changed the installer technology, we moved to ODIS which is a On Demand Installer Service, its purpose is to create an installation, deployment, and update experience that's fast, easy, predictable, and painless for customers.
For Silent Install -
setup.exe --silent --pf abc --sn defghijk
Note abc-defghijk is the serial number assigned to your account
The silent mode won’t allow you to change the INSTALLDIR.

## 评论

**内容**: A said...
How do you suppress reboot on AutoCAD OEM 2022?
Reply
07/01/2022 at 04:55 AM

---
**内容**: Gaetano Perbellini said...
A couple of questions (2023 version):
1) How to know when the silent install finished? When the Icon to start is presente on the desktop?
2) To make a silent installation I must provide my OEM Serial number to the customer. Could be this a problem? I noted that is not possibile to have this SN form the AutoCAD OEM GUI... so it seems non a good practice to give my personal SN to the customer...
Reply
12/13/2022 at 02:12 AM

---
**内容**: Gaetano Perbellini said in reply to Gaetano Perbellini...
About point 2) I found this: https://github.com/MadhukarMoogala/OEMScripts
where is written:
To install silently, the current setup.exe is not configured to silent install, so this is a workaround for now, use fake serial and prefix numbers.
...use fake serial and prefix numbers... is the solution!
Reply
12/14/2022 at 06:43 AM

---
