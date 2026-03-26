---
title: "Using Entitlement API within ObjectARX C++"
date: 2020-07-01
categories:
  - AutoCAD .NET
tags:
  - API
  - C++
  - Entitlement
  - ObjectARX
description: "We have .NET (C#) example on how to secure and protect your app on AutoCAD and other Autodesk products, for AutoCAD, Kean has written long back"
author: Autodesk
---
# Using Entitlement API within ObjectARX C++

发布日期: 2020-07-01

原始链接: https://adndevblog.typepad.com/autocad/2020/07/using-entitlement-api-within-objectarx-c.html

## 文章内容

By Madhukar Moogala
We have .NET (C#) example on how to secure and protect your app on AutoCAD and other Autodesk products, for AutoCAD, Kean has written long back
For Revit – A blog from Mikako
For Fusion 360 – A C++ code, which I used most part of it and made few changes to best fit with AutoCAD
There is an introductory briefing on Entitlement API by Daniel.
For reading brevity, I will give simple statement what it brings to the table.
Entitlement API is a rest enabled API, allows you to check if the user is entitled to access your app i.e., user has bought the app from Autodesk App Store
To call Rest API with in ObjectARX, we need to use a Rest Client, for this I’m using restclient-cpp from mrtazz, a Json library to parse the response and make code more readable (this an optional not a must to run the sample)
Full instructions to build the sample is provided in Github

  if (getUserId()[0] == _T('\0')) {
   //User is not logged in, we will prompt to login!
   onlineUI();
  }
  //plumbing wide
  TCHAR buffer[512];
  acedGetString(0,_T("Enter AppId To Test CheckEntitlement:\t"), buffer);
  string userId = toNarrow(getUserId().kwszPtr());  
  string appId = toNarrow(buffer);
  string url ="https://apps.exchange.autodesk.com/webservices/checkentitlement"+
     string("?userid=") + userId + string("&appid=") + appId;
  RestClient::Response response = RestClient::get(url);

  Json::Reader reader;
  Json::Value root;

  bool isparseSuccessful = reader.parse(response.body, root);
  if (!isparseSuccessful) {
   acutPrintf(_T("Error parsing URL"));
  }
  if ((root["IsValid"].asString()) == "true")
  {
   acutPrintf(_T("IsValid is True"));
  }
  else
  {
   acutPrintf(_T("IsValid is False"));
  }
Working Gif - https://pasteboard.co/JgZaD71.gif

## 评论

**内容**: suika game said...
A very detailed guide that helped me fix my current problem.
Reply
11/30/2023 at 02:13 AM

---
