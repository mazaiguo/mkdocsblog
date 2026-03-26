---
title: "How to use AcadLayout.GetPlotDeviceNames in .Net?"
date: 2012-09-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C#
  - COM
  - Plot
description: "I am using AutoCAD ActiveX interface from C# (or using VB.NET) and I need to get the list of plot devices returned from the method GetPlotDeviceNam..."
author: Autodesk
---
# How to use AcadLayout.GetPlotDeviceNames in .Net?

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/how-to-use-acadlayoutgetplotdevicenames-in-net.html

## 文章内容

By Philippe Leefsma
Q:
I am using AutoCAD ActiveX interface from C# (or using VB.NET) and I need to get the list of plot devices returned from the method GetPlotDeviceNames()
A:
The generic System.Object returned from GetPlotDeviceNames can be cast to an array of strings to access the name for each plot device.
Here is an example:
[CommandMethod("GetPlotDeviceNames")]
public void GetPlotDeviceNames()
{
    AcadApplication acadApp = Application.AcadApplication
        as AcadApplication;
      AcadLayout layout = acadApp.ActiveDocument.ActiveLayout;
      string[] devices = (string[])layout.GetPlotDeviceNames();
      foreach (string device in devices)
    {
        Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(
            "\nPlot Device: " + device);
    }
}

## 评论

**内容**: Jason Huffine said...
Just curious... is there a pure .Net API way without the ActiveX interface?
Reply
09/12/2012 at 08:22 AM

---
**内容**: Philippe said...
Yes there is, and I would say if you are running from a .Net dll in process with AutoCAD, there is no point on relying on the ActiveX API for that. But thing is we are migrating our old knowledge base once restricted to ADN members to that public devblog, so you might see appearing articles that are a bit outdated, although useful...
In .Net you would do as follow:
Editor ed = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
// Assign default return values
string devname = "";
PlotSettingsValidator psv = PlotSettingsValidator.Current;
StringCollection devlist = psv.GetPlotDeviceList();
for (int i = 0; i < devlist.Count; i++)
{
ed.WriteMessage("\n{0} {1}", i + 1, devlist[i]);
}
Reply
09/12/2012 at 08:51 AM

---
