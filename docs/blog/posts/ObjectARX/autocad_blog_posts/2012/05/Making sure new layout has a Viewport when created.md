---
title: "Making sure new layout has a Viewport when created"
date: 2012-05-01
categories:
  - AutoCAD COM
tags:
  - API
  - AutoCAD
  - COM
  - Plugin
description: "An AutoCAD setting in the Options dialog controls behavior of adding a viewport to new layouts. You can turn off the creating viewports in newly cr..."
author: Autodesk
---
# Making sure new layout has a Viewport when created

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/making-sure-new-layout-has-a-viewport-when-created.html

## 文章内容

By Virupaksha Aithal
An AutoCAD setting in the Options dialog controls behavior of adding a viewport to new layouts. You can turn off the creating viewports in newly created layouts. You can find the setting along this path:
'Options' dialog
    -> 'Display' tab
        -> 'Layout Elements' group
            -> 'Create Viewport in New Layouts' check box.
This can be controlled using AutoCAD ActiveX API too. It's ThisDrawing.Application.Preferences.Display.LayoutCreateViewport. The following code does the work exactly:
[CommandMethod("LayoutTest")]
public static void LayoutTest()
{
    Object acadObject = Application.AcadApplication;
        object preferences =
            acadObject.GetType().InvokeMember("Preferences",
            BindingFlags.GetProperty,
            null, acadObject, null);
      object display =
                preferences.GetType().InvokeMember("Display",
                BindingFlags.GetProperty,
                null, preferences, null);
      object layoutProperty =
                display.GetType().InvokeMember("LayoutCreateViewport",
                BindingFlags.GetProperty,
                null, display, null);
    //now set the value to true.
    if (Convert.ToBoolean(layoutProperty) == false)
    {
        object[] dataArry = new object[1];
        dataArry[0] = true;
        display.GetType().InvokeMember("LayoutCreateViewport",
                          BindingFlags.SetProperty,
                          null, display, dataArry);
    }
  }

