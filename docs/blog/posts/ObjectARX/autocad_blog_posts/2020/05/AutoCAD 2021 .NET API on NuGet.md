---
title: "AutoCAD 2021 .NET API on NuGet"
date: 2020-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - NuGet
description: "For AutoCAD 2021 release we have posted API package on to Nuget."
author: Autodesk
---
# AutoCAD 2021 .NET API on NuGet

发布日期: 2020-05-01

原始链接: https://adndevblog.typepad.com/autocad/2020/05/autocad-2021-net-api-on-nuget.html

## 文章内容

By Madhukar Moogala
For AutoCAD 2021 release we have posted API package on to Nuget.
We have started posting AutoCAD .NET packages from AutoCAD 2015 release, from since then we regularly update and post .NET package as per AutoCAD release cycle.
You simply select Project –> Manage NuGet Packages in your Visual Studio project:
Search for AutoCAD .NET click install on the primary AutoCAD.NET package (the third in the list). This will install acmgd.dll and its related assemblies but also the other two dependent packages. You should install AutoCAD.NET.Core (i.e. acmgdcore.dll, etc.) if you want to create a Core Console-compatible project, of course. Either way AutoCAD.NET.Model (i.e. acdbmgd.dll, etc.) will get installed.

Further reading on .NET package can be found on Kean’s old post.

## 评论

**内容**: Greg said...
Is there any Autodesk developer info related to the use of Microsoft .NET 5?
Reply
05/20/2020 at 05:02 PM

---
**内容**: Madhukar Moogala said...
Hi Greg,
We are yet receive concrete roadmap on >NET 5, stay tuned. I will be posting any news I receive.
Reply
05/21/2020 at 07:46 AM

---
**内容**: David Snipp said in reply to Madhukar Moogala...
Any news on .net 5 support?
We are migrating our winforms .net 4.6 application over to .net 5 and not having support for .net 5 is blocking this work.
Reply
07/10/2021 at 07:05 AM

---
**内容**: Madhukar Moogala said in reply to David Snipp...
Hi David,
>NET 5 is not LTS, .NET 6 is LTS, we will be porting to .NET in future release of AutoCAD. I don't have concrete information as .NET 6 will have it's release in November this year.
Reply
07/11/2021 at 11:21 PM

---
**内容**: Tom James said...
About time but excellent work Autodesk, especially the 'NET.Core' version, can't have been quick.
Can people assume:
New NuGet packages will be released for each major update?
Other variants of AutoCAD (i.e. Civil 3D, Map, Architecture, etc.) will receive the necessary additional NuGet packages?
Reply
09/15/2020 at 02:09 PM

---
**内容**: Endrit Murseli said...
I'm new to AutoCad but wanted to know if the Nuget Package is compatible with older versions of Autocad? Or is each Nuget package related to a specific Autocad mayor release?
Reply
11/15/2020 at 12:23 AM

---
**内容**: Nerdle said...
Machinery has gradually replaced human strength and made a lot of profits in their work.
Reply
02/23/2023 at 11:59 PM

---
**内容**: Miguel Masó said...
Hi, are there any news about compatibility with .NET 6? Does anyone know where to find documentation?
Reply
12/06/2023 at 03:20 AM

---
**内容**: Madhukar Moogala said...
Hi Miguel,
Please refer https://adndevblog.typepad.com/autocad/2023/08/call-for-action-next-release-of-autocad.html
Reply
12/08/2023 at 12:22 AM

---
