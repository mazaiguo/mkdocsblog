---
title: "Set Palette into Auto Hide mode"
date: 2013-01-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
  - Palette
description: "Try use the AutoRollup property of the Palette throw the exception: "Operation is not valid due to the current state of the object", even if the pa..."
author: Autodesk
---
# Set Palette into Auto Hide mode

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/set-palette-into-auto-hide-mode.html

## 文章内容

By Augusto Goncalves
Try use the AutoRollup property of the Palette throw the exception: "Operation is not valid due to the current state of the object", even if the palette is docked and visible.
The behavior can be reproduced with the DockingPalette .NET sample in the ObjectARX SDK. The exception occurs when  you Auto Hide a palette which is docked. AutoCAD does not allow a docked palette window to Auto Hide (AutoRollup). This can be seen from native AutoCAD palettes such as Property Palette and Toolpalettes. So, we have to undock the palette window before setting its AutoRollup property as TRUE.
First we need to check if the current docking status. If it is none, we can set the AutoRollUp property to true. However, there is a potential issue here. When the position of the mouse cursor is located in the palette window, the palette will not be automatically refreshed after the AutoRollup property is set as TRUE. We have to move the cursor off the palette window and back onto it and move the cursor off again manually to have the change take effect. The programmatic way is to turn the whole palette window off and on again to refresh the window.
Second, if the palette window is docked, we need to set the Dock property as none and then set its AutoRollup property as true. But we need to give the palette some time to reinitialize itself. In the sample, the palette window is given a moment using a timer.
case "AutoRollup":
{
    // If the palette is not docked, we just
    // set the AutoRollup property as true
    if (ps.Dock == DockSides.None)
    {
        ps.AutoRollUp = true;
        // Note: we need to update the
        // palette window. I found turning
        // it off and on is the most robust way.
        ps.Visible = false;
        ps.Visible = true;
    }
    // If the palette is docked,
    // we need to undock it first.
    else
    {
        ps.Dock = DockSides.None;
        e.WriteMessage(
          "Palette can not AutoRollup if it's" +
          "docked! We undocked it first here.\n");
            // Note: we need to update the palette
        // window. I found turning it off and
        // on is the most robust way.
        ps.Visible = false;
        ps.Visible = true;
        CreateTimer();
    }
    break;
}
The following code is to create a timer, call the relevant methods and properties of the palette in the Tick event, and finally stop and destroy the timer:
static System.Windows.Forms.Timer Clock;
public static void CreateTimer()
{
  Clock = new System.Windows.Forms.Timer();
  Clock.Interval = 500;
  Clock.Start();
  Clock.Tick += new EventHandler(Timer_Tick);
}
    static public void Timer_Tick(object sender,
  EventArgs eArgs)
{
  if (sender == Clock)
  {
    ps.AutoRollUp = true;
    // Note: we need to update the palette
    // window. I found turning it off and
    // on is the most robust way.
    ps.Visible = false;
    ps.Visible = true;
    //ps.Activate(0);
    // Stop the clock and destroy it.
    Clock.Stop();
    Clock.Dispose();
  }
}

