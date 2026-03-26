---
title: "Rearranging ribbon panels"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Palette
description: "Here is a small code snippet that uses the "Move" method to change the ribbon panel position within the same ribbon tab :"
author: Autodesk
---
# Rearranging ribbon panels

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/rearranging-ribbon-panels.html

## 文章内容

By Balaji Ramamoorthy
Here is a small code snippet that uses the "Move" method to change the ribbon panel position within the same ribbon tab :
string tabName = "MyTab";
string panelName = "MyPanel2";
  Autodesk.Windows.RibbonControl ribCntrl =
Autodesk.AutoCAD.Ribbon.RibbonServices.RibbonPaletteSet.RibbonControl;
foreach (Autodesk.Windows.RibbonTab tab in ribCntrl.Tabs)
{
    if (tab.Name != tabName) continue;
      int oldIndex = -1;
    foreach (Autodesk.Windows.RibbonPanel panel in tab.Panels)
    {
        oldIndex++;
          if (panel.Source.Title != panelName)
            continue;
           //To ensure that our panel gets displayed as the
         // first panel in the ribbon tab
        tab.Panels.Move(oldIndex, 0);
          return;
    }
}

