---
title: "Getting current plotter name"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plot
description: "You can use plot configuration manager "PlotConfigManager" to get the current plotter device used by AutoCAD. Below code shows the procedure."
author: Autodesk
---
# Getting current plotter name

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/getting-current-plotter-name.html

## 文章内容

By Virupaksha Aithal
You can use plot configuration manager "PlotConfigManager" to get the current plotter device used by AutoCAD. Below code shows the procedure.
[CommandMethod("CurrentPlotDevice")]
static public void CurrentPlotDevice()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
    try
    {
        PlotConfig config = PlotConfigManager.CurrentConfig;
        ed.WriteMessage("Current plot device :"
                                            + config.DeviceName);
    }
    catch
    {
        ed.WriteMessage("Unable to get the" +
                                    "current plot comfigartion\n");
    }
}

