---
title: "Feeding Extra information into a Command line selection using acedCmd in .NET"
date: 2013-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Selection
description: "Leading on from this post on The “correct” way to use AutoCAD acedCmd() acedCommand() in ObjectARX, .NET, or LISP and Synchronously Send (and wait ..."
author: Autodesk
---
# Feeding Extra information into a Command line selection using acedCmd in .NET

发布日期: 2013-08-01

原始链接: https://adndevblog.typepad.com/autocad/2013/08/feeding-extra-information-into-a-command-line-selection-using-acedcmd-in-net.html

## 文章内容

by Fenton Webb
Leading on from this post on The “correct” way to use AutoCAD acedCmd() acedCommand() in ObjectARX, .NET, or LISP and Synchronously Send (and wait for) commands in AutoCAD using C# .NET I thought I would tell you how to ensure programmatic selections are properly made using acedCmd in .NET.
Lots of factors can affect programmatic selection of entities via acedCmd, remember, acedCmd simply pumps commands to the Command line – a couple of good example of selection via acedCmd being affected is when object snaps are enabled, or say when an object is over the top of another.
It is totally possible to pass extra information into the acedCmd so that the selection input knows more about what you are trying to select – this is done by wrapping the point and entity name information in RTLB and RTLE codes… Here is an example of it in use:
      ResultBuffer rb = new ResultBuffer();
      rb.Add(new TypedValue(5005, "_.OFFSET"));
      rb.Add(new TypedValue(5001, 10.0)); // RTREAL
      rb.Add(new TypedValue(5016)); // RTLB
        rb.Add(new TypedValue(5006, ename)); // RTENAME
        rb.Add(new TypedValue(5009, point)); // RT3DPOINT
      rb.Add(new TypedValue(5017)); //RTLE
      rb.Add(new TypedValue(5009, point)); // RT3DPOINT
      rb.Add(new TypedValue(5005, ""); // RTSTR
      // start the insert command
      acedCmd(rb.UnmanagedObject);

