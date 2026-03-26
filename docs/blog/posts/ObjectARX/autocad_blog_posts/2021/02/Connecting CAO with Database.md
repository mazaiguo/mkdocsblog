---
title: "Connecting CAO with Database"
date: 2021-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - Database
description: "NOTE - This workflow describes how to connect to CAO with MS Access database (.mdb/.accdb)"
author: Autodesk
---
# Connecting CAO with Database

发布日期: 2021-02-01

原始链接: https://adndevblog.typepad.com/autocad/2021/02/connecting-cao-with-database.html

## 文章内容

NOTE - This workflow describes how to connect to CAO with MS Access database (*.mdb/*.accdb)
From AutoCAD 2020, we have retired 32-bit AutoCAD, to connect to MS Access database from 64 Bit AutoCAD, you need install 64-bit MS Access DB Engine. 
(thanks for pointing out -Norman Yuan)
About version of Microsoft Office and its bitness 
Please refer this blog on Microsoft
I'm using MS Access 64 Bit (MS Office 365)
          Step1: Launch AutoCAD 2021
Open the "Floor Planning" drawing from "C:\~\AutoCAD 2021\Sample\Database Connectivity\Floor Plan Sample.dwg"
Enter "DBCONNECT"
From DBCONNECT MANAGER, select Jet_dbSamples in "Data Sources" field.
Right Click and Select "Configure"
Step2: Configure DB
In the "Data Link Properties", select Microsoft OLE DB provider for ODBC Drivers and "NEXT."
In Next page, check "Use Connection String" and click Build.
In the "Select Data Source" window, select "Machine Data Source "page and click New.
Create New Data Source -> Check "User Data Source" -> Next
Select "Microsoft Access Driver (*.mdb,*.accdb) -> Next -> Finish
Step3: ODBC Microsoft Access Setup
In ODBC Microsoft Access Setup window, write Data Source name of your choice.
Select `Database` and pick the folder where db-samples.mdb is located.
In my example, it is located at C:\~\AutoCAD 2021\Sample\Database Connectivity.
OK
OK
OK
OK
Step4: Testing Connection
Come Back to "Data Link Properties" and Select "Test Connection"

## 评论

**内容**: Norman Yuan said...
Well, the whole description of how to connect to CAO with database is only focus on how to connect to *.mdb/*.accdb (MS Access database). It would be better to pointed out at beginning, because CAO can also connect to other database via ODBC data source.
However, this article omitted a most important requirement for connecting MS Access database: one must install 64-bit MS Access DB Engine (because latest AutoCAD does not have 32-bit version any more), which has been a troublesome issue, especially most CAD users would have 32-bit MS Office suite (or even 32-bit MS Access installed). So, post article with this important omission would encourage the use of bad combination of AutoCAD and MS Access database.
Also, Jet database has long gone, yet, AutoCAD carries the pre-configured sample data source "Jet_dbsample" version by version, which is useless without 64-bit MS Access DB Engine pre-installed on almost all CAD computers. If AutoCAD is to keep a not-working preconfigured sample CAO data source, at least change its name (i.e. removing "Jet_" from the source name).
Reply
03/11/2021 at 07:55 AM

---
**内容**: Keyur Khalasi said...
Hello Madhukar Sir,
Hi, I am Keyur Khalasi RuleBuddy PlanAssist Developer from Softtech Team Pune,
I had one question for your.
As My Visual Studio 2019 ENterprise is Updated to 16.11.19 and i had made my .arx and .dll file using this for making Our AutoCAD OEM 2021 setup of RuleBuddy PlanAssist. But its give me the error like
rulebuddy2021.arx is incompatible with this version of PlanAssist Software. So please help me out on this.

Development environment: Microsoft® Visual Studio® 2019 version 16.11.19 (with C++ option installed) and .NET 4.8
Autocad oem 2021 make wizard version 5.0 product release version 24.0.47.0

Regards,
Keyur Khalasi.
Reply
10/10/2022 at 12:29 AM

---
**内容**: Madhukar Moogala said...
Hi Keyur,
I'm struggling to understand the problem here, do you mean that you have created an ARX rulebuddy2021.arx compiled with VS2019, when bound with OEM program you are getting this error ?
Is the OEM stamp successful ?
I request you to raise a developer ticket with A D N support. Some one from our team will gladly assist you.
Reply
10/10/2022 at 09:43 PM

---
**内容**: flappy bird said...
These instructions are easier to follow than I thought. I have applied and succeeded.
Reply
04/03/2023 at 02:48 AM

---
