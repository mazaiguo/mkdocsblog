---
title: "Get the Virtual Memory used by a process like AutoCAD"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - AutoLISP
  - Database
description: "I have a LISP benchmark program and would like to also log the virtual memory being used by AutoCAD."
author: Autodesk
---
# Get the Virtual Memory used by a process like AutoCAD

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/get-the-virtual-memory-used-by-a-process-like-autocad.html

## 文章内容

By Adam Nagy
I have a LISP benchmark program and would like to also log the virtual memory being used by AutoCAD.
Solution
You could use the .NET Framework to get information about the memory being used by AutoCAD. If you place your code in a .NET defined LISP function then it can also be used from a LISP program.
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Runtime;
using System.Diagnostics;
  [assembly: CommandClass(typeof(MyProcessMonitor.Commands))]
  namespace MyProcessMonitor
{
  public class Commands
  {
    [LispFunction("GetVirtualMemorySize")]
    static public ResultBuffer GetVirtualMemorySize(
      ResultBuffer rbIn)
    {
      Process cp = Process.GetCurrentProcess();
      ResultBuffer rbOut = new ResultBuffer(new TypedValue[]
      {
        // 1) use double so that we do not run into the Int32 limit
        // 2) if you want the "VM Size" column of Task Manager
        //    that is actually shown by cp.PrivateMemorySize64
        new TypedValue(
          (int)LispDataType.Double, cp.VirtualMemorySize64)
      });
        return rbOut;
    }
  }
}

