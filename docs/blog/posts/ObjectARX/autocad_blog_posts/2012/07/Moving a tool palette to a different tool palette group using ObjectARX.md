---
title: "Moving a tool palette to a different tool palette group using ObjectARX"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - C++
  - CUI
  - ObjectARX
  - Palette
description: "Here is a sample ObjectARX code to move a palette belonging to a tool palette group to another group."
author: Autodesk
---
# Moving a tool palette to a different tool palette group using ObjectARX

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/moving-a-tool-palette-to-a-different-tool-palette-group-using-objectarx.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample ObjectARX code to move a palette belonging to a tool palette group to another group.
This code assumes that you have a palette called "MyPalette" that belongs to the "Annotation and Design" tool palette group. This palette will be moved to the "Parametric Design" tool palette group.
CAcTcUiToolPaletteSet *pTPSet = AcTcUiGetToolPaletteWindow();
CAcTcUiToolPaletteGroup *pPaletteGroups
                        = pTPSet->GetToolPaletteGroup(false); 
  // Find the "Annotation and Design" tool palette group
CAcTcUiToolPaletteGroup *pAnnotationDesignGrp
    = pPaletteGroups->FindGroup(ACRX_T("Annotation and Design"));
  // Find the "Parametric Design" tool palette group
CAcTcUiToolPaletteGroup *pParametricDesignGrp
        = pPaletteGroups->FindGroup(ACRX_T("Parametric Design"));
  if(pAnnotationDesignGrp != NULL && pParametricDesignGrp != NULL)
{
    // Find the tool palette called "MyPalette"
    CAcTcUiToolPalette *pMyPalette
            = pAnnotationDesignGrp->FindPalette
                        (
                            ACRX_T("MyPalette"),
                            NULL
                        );
    if(pMyPalette != NULL)
    {
        // Remove the palette from the
        // "Annotation and Design" tool palette group
        pAnnotationDesignGrp->RemoveItem(pMyPalette, TRUE);
          // Add the palette to the
        // "Parametric Design" tool palette group
        pParametricDesignGrp->AddItem(pMyPalette);
    }
}
Unfortunately, at present it is not possible to do this using the AutoCAD .Net API since the class "CAcTcUiToolPaletteGroup" does not have an equivalent.

