---
title: "Running AutoCAD VBA from C# .NET"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C#
  - VBA
description: "Here’s how to invoke a function Public Sub Test() declared in VBA from .NET; use acedCmd() and run –vbarun"
author: Autodesk
---
# Running AutoCAD VBA from C# .NET

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/running-autocad-vba-from-c-net.html

## 文章内容

by Fenton Webb
Here’s how to invoke a function Public Sub Test() declared in VBA from .NET; use acedCmd() and run –vbarun
    // how to call VBA from .NET
#if AC2013
    [DllImport("accore.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "acedCmd")]
#else
    [DllImport("acad.exe", CallingConvention = CallingConvention.Cdecl, EntryPoint = "acedCmd")]
#endif
    private static extern int acedCmd(System.IntPtr vlist);
    [CommandMethod("callVBA")]
    public void callVBA()
    {
      ResultBuffer rb = new ResultBuffer();
      // RTSTR = 5005
      rb.Add(new TypedValue(5005, "_.-vbarun"));
      rb.Add(new TypedValue(5005, "test"));
      // start vbarun running 'ThisDrawing.Test()
      acedCmd(rb.UnmanagedObject);
    }

## 评论

**内容**: Account Deleted said...
Hi Fenton!
There is another method with AcadApplication.RunMacro
Reply
08/06/2012 at 10:27 PM

---
