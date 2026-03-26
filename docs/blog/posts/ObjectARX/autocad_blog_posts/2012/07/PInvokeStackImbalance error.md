---
title: "PInvokeStackImbalance error"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Unicode
description: "I'm trying to P/Invoke acedPostCommand() so that I could use it to cancel the current command, but I get a PInvokeStackImbalance error when calling..."
author: Autodesk
---
# PInvokeStackImbalance error

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/pinvokestackimbalance-error.html

## 文章内容

By Adam Nagy
I'm trying to P/Invoke acedPostCommand() so that I could use it to cancel the current command, but I get a PInvokeStackImbalance error when calling acedPostCommand inside my .NET code:
How could I solve this?
Here is the P/Invoke I'm using:
[DllImport("acad.exe",
  CharSet = CharSet.Unicode,
  EntryPoint = "?acedPostCommand@@YAHPB_W@Z")]
public static extern bool acedPostCommand(string cmd);
Solution
You also need to specify the calling convention. Once that's done acedPostCommand() works fine:
[DllImport("acad.exe",
  CharSet = CharSet.Unicode,
  CallingConvention = CallingConvention.Cdecl,
  EntryPoint = "?acedPostCommand@@YAHPB_W@Z")]
public static extern bool acedPostCommand(string cmd);

