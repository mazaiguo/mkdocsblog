---
title: "Iterate Palette Groups to make a specific Palette group current using ObjectARX"
date: 2013-02-01
categories:
  - AutoCAD C++
tags:
  - C++
  - CUI
  - ObjectARX
  - Palette
description: "Is there a way to programmatically set a palette group as the active palette group?"
author: Autodesk
---
# Iterate Palette Groups to make a specific Palette group current using ObjectARX

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/iterate-palette-groups-to-make-a-specific-palette-group-current-using-objectarx.html

## 文章内容

By Fenton Webb
Issue
Is there a way to programmatically set a palette group as the active palette group?
Solution
The palette group returned by CAcTcUiToolPaletteSet::GetToolPaletteGroup() can be iterated. If the item is not a palette and the palette group has the name you want, you can make it the active palette group with SetActivePaletteGroup().
This example gets all the pallet groups and displays the name of each palette group in a MessageBox. If the name of the palette group is "wbPGroup", it is made into the current group.
static void ASDKtestTpGroup(void)
{
  CAcTcUiToolPaletteSet * pTpset = AcTcUiGetToolPaletteWindow();
  CAcTcUiToolPaletteGroup * pTpgroup = pTpset->GetToolPaletteGroup(false);
  CAcTcUiToolPaletteGroup * pTpSubGroup;
    CString groupName;
  int iCount = pTpgroup->GetItemCount();
  for(int i = 0; i<iCount; i++)
  {
    if(!pTpgroup->IsItemPalette(i))
    {
      pTpgroup->GetItem(i, pTpSubGroup);
      groupName = pTpSubGroup->GetName();
      ::MessageBox(NULL, groupName, _T("Summary Information"), MB_OK);
      if(groupName == "wbPGroup")
        pTpset->SetActivePaletteGroup(pTpSubGroup);
    }
  }
}

