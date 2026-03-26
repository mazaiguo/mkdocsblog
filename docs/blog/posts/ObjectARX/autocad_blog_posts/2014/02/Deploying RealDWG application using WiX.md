---
title: "Deploying RealDWG application using WiX"
date: 2014-02-01
categories:
  - AutoCAD C++
tags:
  - C++
  - DWG
description: "Here is a sample project from RealDWG DevTV that has been modified to use WiX to deploy the application."
author: Autodesk
---
# Deploying RealDWG application using WiX

发布日期: 2014-02-01

原始链接: https://adndevblog.typepad.com/autocad/2014/02/deploying-realdwg-application-using-wix.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample project from RealDWG DevTV that has been modified to use WiX to deploy the application.
To try this, please download and install the WiX Toolset.
There are two batch files included in the sample project folder. These batch files run as "Pre-build event" when the project is built. Please ensure that the path of the VC++ re-distributables, Fonts and other RealDWG merge modules are correctly specified in the batch files.
The purpose of the batch files is to copy all the files needed for the packaging to a common folder named as "ForPackaging". The WiX setup project builds the MSI by using this folder path without having to look for files in different paths.
Download MyRealDWG_Sample

## 评论

**内容**: proje tasarim cizim said...
Thank you
Reply
02/05/2014 at 08:25 AM

---
