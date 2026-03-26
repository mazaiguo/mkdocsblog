---
title: "PaletteSet minimum docked width"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - Palette
description: "I have a PaletteSet that contains a toolbar and its width is set to 40 pixels. This works fine in AutoCAD 2008, but in AutoCAD 2011 I cannot make t..."
author: Autodesk
---
# PaletteSet minimum docked width

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/paletteset-minimum-docked-width.html

## 文章内容

By Adam Nagy
I have a PaletteSet that contains a toolbar and its width is set to 40 pixels. This works fine in AutoCAD 2008, but in AutoCAD 2011 I cannot make the width smaller than 150 pixels when the PaletteSet is docked.
Solution
In AutoCAD 2009 the minimum docked width of dockable windows including PaletteSets has been changed from 40 to 150 pixels and it is so in AutoCAD 2011 as well.
In AutoCAD 2012 however a new ARX function is being introduced which can override this value:
bool AdUiSetDockBarMinWidth(int width)
You can also use it from .NET via P/Invoke:
public class Commands
{
  PaletteSet ps;
    // The function signature passed in for EntryPoint
  // is different in case of AutoCAD x64
  [DllImport(
    "adui18.dll", CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "?AdUiSetDockBarMinWidth@@YA_NH@Z")]
  public static extern bool AdUiSetDockBarMinWidth(int width);
    [CommandMethod("MyPalette")]
  public void MyPalette()
  {
    AdUiSetDockBarMinWidth(40);
      if (ps == null)
    {
      ps = new PaletteSet("My Palette 1");
      ps.MinimumSize = new System.Drawing.Size(30, 300);
      ps.Dock = DockSides.Top;
      MyControl1 myCtrl = new MyControl1();
      myCtrl.Dock = System.Windows.Forms.DockStyle.Fill;
      ps.Add("test", myCtrl);
    }
    ps.Visible = true;
  }
}

## 评论

**内容**: PM said...
I realise this is an old post but I need to do exactly this for AutoCAD 2016.
Could you please tell me which dll I need to import and how I find the entry point?
Thank you
Reply
11/17/2015 at 03:05 AM

---
**内容**: Adam Nagy said...
Hi,
The DllImport part has the info:
dll: "adui18.dll"
entry point: "?AdUiSetDockBarMinWidth@@YA_NH@Z"
Cheers,
Adam
Reply
11/17/2015 at 05:07 AM

---
