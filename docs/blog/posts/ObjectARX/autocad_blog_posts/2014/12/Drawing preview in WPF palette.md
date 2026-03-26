---
title: "Drawing preview in WPF palette"
date: 2014-12-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Block
  - Palette
description: "As you may already know, the BlockView .Net sample demonstrates the use of Graphics system to preview a drawing in a Windows form. The migrated sam..."
author: Autodesk
---
# Drawing preview in WPF palette

发布日期: 2014-12-01

原始链接: https://adndevblog.typepad.com/autocad/2014/12/drawing-preview-in-wpf-palette.html

## 文章内容

By Balaji Ramamoorthy
As you may already know, the BlockView .Net sample demonstrates the use of Graphics system to preview a drawing in a Windows form. The migrated sample that works with AutoCAD 2015 is available here.
To get the preview displayed inside a WPF user control hosted in an AutoCAD palette, poses a small problem. In that sample, as the "GraphicsManager.CreateAutoCADDevice" requires a Window handle to display the graphics, there is no direct way to get the display in a WPF user control. In a WPF window, the controls are managed by the top level window and there are no individual handles assigned separately for the controls. Because of this difference, the only way to get this working in WPF is to host the Windows user control that displays the preview in a WindowsFormsHost.
The attached sample is a modified version of the BlockView .Net sample that demonstrates this.
Download Modified BlockView.NET

To try it, netload the dll and run the "bviewpal" command. To preview a drawing, click on the button in the palette and browse to a drawing.

Here is a screenshot of the WPF palette previewing a drawing :

## 评论

**内容**: Gary Manuel said...
I have an menu type app that uses PaletteSet also and is designed to be docked horizontally between the AutoCAD drawing window and the Ribbon. Prior to AutoCAD 2015, once the palette is docked, you could manually adjust the height of the palette within the AutoCAD UI. However in 2015, this ability is no longer available.
Using your WPF sample, I was able to duplicate this issue. I added + (int)DockSides.Top) to your _ps.DockEnabled...after compiling it, I loaded it in AutoCAD 2014...it will dock at the top and the palette height can be adjusted. In AutoCAD 2015, only the width can be adjusted when docked to the side but if docked at the top, the height is not adjustable.
Hopefully you can offer a solution to this?
Thanks
Gary
Reply
01/15/2015 at 10:24 AM

---
**内容**: MX said...
In the panel the block/DWG is not viewed after clicking preview drawing (and selecting a DWG).
Is seems there are some issues with:
using (BlockTableRecord curSpace = db.CurrentSpaceId.Open(OpenMode.ForRead, true, true) as BlockTableRecord)
mPreviewCtrl.mpView.Add(curSpace, mPreviewCtrl.mpModel);
Problem:
'ObjectId.Open(OpenMode, bool, bool)' is obsolete: 'For advanced use only. Use GetObject instead'
Does anybody know how to solve this for AutoCAD 2015?
Reply
06/18/2018 at 05:50 AM

---
