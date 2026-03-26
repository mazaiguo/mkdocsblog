---
title: "Detecting Ribbon Panel Visibility Change"
date: 2015-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I’ve received a query from an ADN partner on how to get notified when Ribbon panel visibility is changed."
author: Autodesk
---
# Detecting Ribbon Panel Visibility Change

发布日期: 2015-05-01

原始链接: https://adndevblog.typepad.com/autocad/2015/05/detecting-ribbon-panel-visibility-change.html

## 文章内容

By Madhukar Moogala
I’ve received a query from an ADN partner on how to get notified when Ribbon panel visibility is changed.
Here is a self explanatory code, all we need is to listen to
IsVisibleChanged event.
private const String TAB_ID = "ID_CUSTOMCMDS";
[CommandMethod("addRibbon")]
public void addRibbon()
{
Autodesk.Windows.RibbonControl rbnCtrl =
    RibbonServices.RibbonPaletteSet.RibbonControl;
RibbonTab rbnTab = new  RibbonTab();
rbnTab.Title = "Custom commands";
rbnTab.Id = TAB_ID;
rbnCtrl.Tabs.Add(rbnTab);
Autodesk.Windows.RibbonPanelSource rbnPnlSrc =
    new Autodesk.Windows.RibbonPanelSource();
rbnPnlSrc.Title = "Custom Panel";
/*Ribbon Panel visibility */
RibbonPanel rbnPnl = new RibbonPanel();
rbnPnl.IsVisibleChanged += rbnPnl_IsVisibleChanged;
rbnPnl.Source = rbnPnlSrc;
rbnTab.Panels.Add(rbnPnl);
Autodesk.Windows.RibbonButton rbnBtn =
    new Autodesk.Windows.RibbonButton();
rbnBtn.Text = "NETLOAD";
rbnBtn.CommandParameter = "NETLOAD";
rbnBtn.ShowText = true;
  Autodesk.Windows.RibbonToolTip rbnTT =
    new RibbonToolTip();
rbnTT.Command = "NETLOAD";
rbnTT.Title = "Load a.NET assembly";
rbnTT.Content = "Command to load a.NET assembly in AutoCAD";
rbnBtn.ToolTip = rbnTT;
rbnPnlSrc.Items.Add(rbnBtn);
rbnTab.IsActive = true;
}
  void rbnPnl_IsVisibleChanged(object sender, EventArgs e)
{
Application.ShowAlertDialog("Event triggered, Panel visiblity changed");
}

