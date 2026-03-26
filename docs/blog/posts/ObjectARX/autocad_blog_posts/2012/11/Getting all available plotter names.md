---
title: "Getting all available plotter names"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plot
description: "You can use plot configuration manager "PlotConfigManager" to get all the plotter devices available for AutoCAD. “PlotConfigManager” has a property..."
author: Autodesk
---
# Getting all available plotter names

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/getting-all-plotter-names-1.html

## 文章内容

By Virupaksha Aithal
You can use plot configuration manager "PlotConfigManager" to get all the plotter devices available for AutoCAD. “PlotConfigManager” has a property called “Devices”, which provides the access to all the devices.  Below code shows the procedure.
[CommandMethod("ListPlotDevices")]
static public void ListPlotDevices()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      PlotConfigInfoCollection devices = PlotConfigManager.Devices;
    foreach(PlotConfigInfo info in devices)
    {
        ed.WriteMessage(info.DeviceName + "\n");
    }
}

