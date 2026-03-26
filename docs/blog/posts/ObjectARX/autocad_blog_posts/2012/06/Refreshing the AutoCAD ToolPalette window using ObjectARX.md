---
title: "Refreshing the AutoCAD ToolPalette window using ObjectARX"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - CUI
  - ObjectARX
  - Palette
description: "If you ever wanted to refresh the ToolPalette GUI programmatically, then here’s how..."
author: Autodesk
---
# Refreshing the AutoCAD ToolPalette window using ObjectARX

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/refreshing-the-autocad-toolpalette-window-using-objectarx.html

## 文章内容

by Fenton Webb
If you ever wanted to refresh the ToolPalette GUI programmatically, then here’s how...
In ObjectARX, you can refresh the ToolPalette Palette window by calling these functions:
1) Get the ToolPaletteWindow (defined in AcTcUi.h)
CAcTcUiToolPaletteSet* AcTcUiGetToolPaletteWindow(void);
2) From the CAcTcUiToolPaletteSet find your Palette (defined in AcTcUiToolPalette.h)
CAcTcUiToolPalette* FindPalette (LPCTSTR pszPalName,
CAcTcUiToolPaletteGroup** ppGroup,
BOOL bSearchOnlyCurrentGroup) const;
3) From the CAcTcUiToolPalette get the Palette View (defined in AcTcUiToolPalette.h)
CAcTcUiPaletteView* GetView (void);
4) From the CAcTcUiPaletteView call the update function (defined in AcTcUiCatalogView.h)
BOOL Update (BOOL bRedraw = TRUE);

