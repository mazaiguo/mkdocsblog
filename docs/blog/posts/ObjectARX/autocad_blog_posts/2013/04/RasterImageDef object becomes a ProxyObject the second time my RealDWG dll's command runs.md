---
title: "RasterImageDef object becomes a ProxyObject the second time my RealDWG dll's command runs"
date: 2013-04-01
categories:
  - AutoCAD
tags:
  - DWG
description: "I have a RealDWG exe application and its installed version runs fine."
author: Autodesk
---
# RasterImageDef object becomes a ProxyObject the second time my RealDWG dll's command runs

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/rasterimagedef-object-becomes-a-proxyobject-the-second-time-my-realdwg-dlls-command-runs.html

## 文章内容

By Adam Nagy
Issue
I have a RealDWG exe application and its installed version runs fine.
However, when I place the same functionality/code in a RealDWG dll and call that from an exe, then in case of its installed version, the second time I call my function from the dll the RasterImageDef objects are only available as ProxyObjects.
Solution
The RuntimeSystem.Initialize() and Terminate() functions are only supposed to be called once within an application session.
The easiest solution is to have a single static/Shared instance of your DwgHost class in your RealDWG dll and its constructor and destructor is implemented the way shown in the below code.
This way even if you provide static/Shared public functions in your RealDWG dll that can be called from your other applications, the RealDWG system is already initialized and its Initialize and Terminate functions are only called once:
Public Class RealDwgDLL
  Public Class DwgHost
    Inherits Autodesk.AutoCAD.DatabaseServices.HostApplicationServices

    Public Sub New()
      Autodesk.AutoCAD.Runtime.RuntimeSystem.Initialize(Me, 1033)
    End Sub

    Protected Overrides Sub Finalize()
      Autodesk.AutoCAD.Runtime.RuntimeSystem.Terminate()
      MyBase.Finalize()
    End Sub

    ' ...

  End Class

  Public Shared mInstance As DwgHost = New DwgHost

  ' ...

