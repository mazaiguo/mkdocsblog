---
title: "Zooming to drawing extents"
date: 2012-09-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - COM
description: "Simple and direct method to zoom the drawing to its extents is use the ActiveX API “ZoomExtents” as shown in below code."
author: Autodesk
---
# Zooming to drawing extents

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/zooming-to-drawing-extents.html

## 文章内容

By Virupaksha Aithal
Simple and direct method to zoom the drawing to its extents is use the ActiveX API “ZoomExtents” as shown in below code.
VB.NET
        <CommandMethod("TestZoomExtent")> _
        Public Sub TestZoomExtent()
            'AcadApplication has a function to zoom extent
            Dim acadApp As Object = Application.AcadApplication
            acadApp.ZoomExtents()
        End Sub
C#
[CommandMethod("zoomExtentTest")]
public static void zoomExtentTest()
{
    //using InvokeMember to support .NET 3.5
    Object acadObject = Application.AcadApplication;
    acadObject.GetType().InvokeMember("ZoomExtents",
                BindingFlags.InvokeMethod, null, acadObject, null);
}

## 评论

**内容**: Emanuel Ceballos said...
Is there a way to use the "browser" command with InvokeMember? Something like:
acadObject.GetType().InvokeMember("browser",
BindingFlags.InvokeMethod, null, acadObject, null);
Thanks.
Reply
07/16/2013 at 01:33 PM

---
**内容**: Viru said in reply to Emanuel Ceballos...
Hi,
Sorry not clear about your question. Can you please provide detail explanation?
regards
Viru
Reply
07/25/2013 at 02:21 AM

---
**内容**: fabian said...
C#
in .NET 4.0 you can also use this:
dynamic acadObject = Application.AcadApplication;
acadObject.ZoomExtents();
Reply
03/13/2014 at 08:31 AM

---
**内容**: karl said...
can this be used to "zoom" 0.75x? or "xp" for paperspace?
thanx,
karl
Reply
01/19/2015 at 04:25 AM

---
**内容**: BKSpurgeon said...
thanks - for an operation i want to get the whole drawing with this zoom extent - the code provided above does this, but after the operation is complete i want to be able to give the user the zoom she was using before the command was run. how do i get the old zoom extents?
Reply
12/22/2016 at 03:53 PM

---
