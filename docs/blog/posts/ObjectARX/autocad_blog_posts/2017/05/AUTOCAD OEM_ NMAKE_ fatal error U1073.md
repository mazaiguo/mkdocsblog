---
title: "AUTOCAD OEM: NMAKE: fatal error U1073"
date: 2017-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
  - Surface
description: "This is error is not uncommon to AUTOCAD OEM and it not issue with latest AutoCAD OEM 2018, I do get queries on this error hence I though I will blog."
author: Autodesk
---
# AUTOCAD OEM: NMAKE: fatal error U1073

发布日期: 2017-05-01

原始链接: https://adndevblog.typepad.com/autocad/2017/05/autocad-oem-nmake-fatal-error-u1073.html

## 文章内容

By Madhukar Moogala
  This is error is not uncommon to AUTOCAD OEM and it not issue with latest AutoCAD OEM 2018, I do get queries on this error hence I though I will blog.
May this error is more surface now because newer operating systems might have disabled 8dot3filename by default.
You must enable 8.3 Name Creation on NTFS Partitions to allow the OEM makewizard engine to work with long file names or with spaces and nonstandard characters in the file name during conversion. To do so:
You can query for the volume in which your planning to build OEM, if it is enabled or not.
for example :  type following example at an elevated command prompt, 
fsutil 8dot3name query D:
In my case it is not enabled;
So now we will enable 8dot3file name on our Volume D:, so the command would be
fsutil behavior set sisable8dot3 D: 0
  Or alternatively you enable on all drives
fsutil.exe behavior set disable8dot3 0
  Refer this for more information
https://technet.microsoft.com/en-us/library/ff621566(v=ws.11).aspx

