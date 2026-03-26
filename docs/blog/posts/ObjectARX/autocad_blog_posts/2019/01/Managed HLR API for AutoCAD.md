---
title: "Managed HLR API for AutoCAD"
date: 2019-01-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - HLR
  - ObjectARX
description: "We have recieved considerable amount of requests from developers to have a managed wrapper on classic HLR API, that comes with ObjectARX SDK of Aut..."
author: Autodesk
---
# Managed HLR API for AutoCAD

发布日期: 2019-01-01

原始链接: https://adndevblog.typepad.com/autocad/2019/01/managed-hlr-api-for-autocad.html

## 文章内容

By Madhukar Moogala
We have recieved considerable amount of requests from developers to have a managed wrapper on classic HLR API, that comes with ObjectARX SDK of AutoCAD
This sample was originally written by Cyrille, recently I managed to fix few issues with progress callback and migrated to latest AutoCAD 2019.
I'm happily welcome any pull requests you have
Complete source of wrapper can found on Github HLRManaged NET Sample

## 评论

**内容**: Dario said...
Hello,
i've setted $(OARX2019) to my local path, as well as the AcDbMgd.dll using in StdAfx.h, and I've compiled the sample project.
When I netload the HlrNetSample.dll and try the test command i get a FileNotFoundException, the same happens when I try to netload ASdkHlrApiMgd.dll. Stacktrace is the following:
Cannot load assembly. Error details: System.IO.FileNotFoundException: Could not load file or assembly 'AsdkHlrApiMgd.dll' or one of its dependencies.
File name: 'AsdkHlrApiMgd.dll'
at System.Reflection.RuntimeAssembly._nLoad(AssemblyName fileName, String codeBase, Evidence assemblySecurity, RuntimeAssembly locationHint, StackCrawlMark& stackMark, IntPtr pPrivHostBinder, Boolean throwOnFileNotFound, Boolean forIntrospection, Boolean suppressSecurityChecks)
at System.Reflection.RuntimeAssembly.InternalLoadAssemblyName(AssemblyName assemblyRef, Evidence assemblySecurity, RuntimeAssembly reqAssembly, StackCrawlMark& stackMark, IntPtr pPrivHostBinder, Boolean throwOnFileNotFound, Boolean forIntrospection, Boolean suppressSecurityChecks)
at System.Reflection.RuntimeAssembly.InternalLoadFrom(String assemblyFile, Evidence securityEvidence, Byte[] hashValue, AssemblyHashAlgorithm hashAlgorithm, Boolean forIntrospection, Boolean suppressSecurityChecks, StackCrawlMark& stackMark)
at System.Reflection.Assembly.LoadFrom(String assemblyFile)
at Autodesk.AutoCAD.Runtime.ExtensionLoader.Load(String fileName)
at loadmgd()
My experience with C++ is very limited, what I'm missing here?
Thank you
Reply
03/05/2019 at 07:22 AM

---
**内容**: Madhukar Moogala said...
Hi,
Thanks for stopping by.
Can you please appload the "$(OARX2019)\Redistrib-x64\AsdkHlrApi23.dbx", prior to loading your DLL
Reply
03/05/2019 at 11:08 PM

---
**内容**: Dario said...
Hello,
apploading the DBX solved the issue, thank you.
Reply
03/06/2019 at 02:19 AM

---
