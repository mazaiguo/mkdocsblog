---
title: "Switching tool palettes programmatically"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - CUI
  - Palette
description: "We can get the tool palette window using the global function AcTcUiGetToolPaletteWindow() and then get the active palette group using the function ..."
author: Autodesk
---
# Switching tool palettes programmatically

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/switching-tool-palettes-programmatically.html

## 文章内容

By Balaji Ramamoorthy
We can get the tool palette window using the global function AcTcUiGetToolPaletteWindow() and then get the active palette group using the function GetActivePaletteGroup() of the palette window.
If you already know the index of the tool palette to be activated then the SetActivePalette() function of the palette group can be used to set the active palette.
If not, we can get the count of palettes using the GetItemCount() method of CAcTcUiToolPaletteGroup class, loop through all the palettes, and find the palette index by checking the palette name returned by CAcTcUiToolPalette::GetName().
Here is a sample code snippet :
// Get the tool palette window
CAcTcUiToolPaletteSet *pToolPaletteWindow
                                = AcTcUiGetToolPaletteWindow();
  // Get the active tool palette group
CAcTcUiToolPaletteGroup *pToolPaletteGroup
        = AcTcUiGetToolPaletteWindow()->GetActivePaletteGroup();
  if(pToolPaletteGroup != NULL)
{
    // Find the number of tool palettes in the group
    int numOfPalettes = pToolPaletteGroup->GetItemCount();
      for(int index = 0; index < numOfPalettes; index++)
    {
        // Get the tool palette
        CAcTcUiToolPalette *pToolPalette = NULL;
        if(pToolPaletteGroup->GetItem(index, pToolPalette))
        {
            // Check if this is the one to be activated
            CString toolPaletteName = pToolPalette->GetName();
            if(toolPaletteName == ACRX_T("Mechanical"))
            {
                // Set it as active
                pToolPaletteGroup->SetActivePalette(index);
                  // Done
                break;
            }
        }
    }
}

