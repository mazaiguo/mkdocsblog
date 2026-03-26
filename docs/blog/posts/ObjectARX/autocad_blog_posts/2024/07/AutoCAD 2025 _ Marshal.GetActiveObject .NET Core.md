---
title: "AutoCAD 2025 : Marshal.GetActiveObject .NET Core"
date: 2024-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C#
  - COM Interop
description: "The GetActiveObject method is deprecated in .NET 8, specifically starting from .NET Core 3.0. The Marshal.GetActiveObject() API is a simple wrapper..."
author: Autodesk
---
# AutoCAD 2025 : Marshal.GetActiveObject .NET Core

发布日期: 2024-07-01

原始链接: https://adndevblog.typepad.com/autocad/2024/07/autocad-2025-marshalgetactiveobject-net-core.html

## 文章内容

By Madhukar Moogala
The GetActiveObject method is deprecated in .NET 8, specifically starting from .NET Core 3.0. The Marshal.GetActiveObject() API is a simple wrapper over the Running Object Table (ROT) and relies on folllwing Win32 APIs that can easily be called via P/Invoke.
CLSIDFromProgIDEx
GetActiveObject
An example of how to manually communicate with the ROT can be found at this GitHub repository. It is unlikely that Microsoft will bring this API back.
Let's write a our own method GetActiveObject
    
```csharp
  [DllImport("ole32")]
  private static extern int CLSIDFromProgIDEx(
    [MarshalAs(UnmanagedType.LPWStr)] string lpszProgID,
    out Guid lpclsid);
  [DllImport("oleaut32")]
  private static extern int GetActiveObject(
    [MarshalAs(UnmanagedType.LPStruct)] Guid rclsid,
    IntPtr pvReserved,
    [MarshalAs(UnmanagedType.IUnknown)] out object ppunk);

  public static object? GetActiveObject(string progId,
                                       bool throwOnError = false)
  {
  if (progId == null)
      throw new ArgumentNullException(nameof(progId));

  var hr = CLSIDFromProgIDEx(progId, out var clsid);
  if (hr < 0)
  {
      if (throwOnError)
          Marshal.ThrowExceptionForHR(hr);

      return null;
  }
  hr = GetActiveObject(clsid, IntPtr.Zero, out var obj);
  if (hr < 0)
  {
      if (throwOnError)
          Marshal.ThrowExceptionForHR(hr);

      return null;
  }
  return obj;
  }
```

