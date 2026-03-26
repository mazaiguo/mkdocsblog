---
title: "Running a Tool from ToolPalette"
date: 2013-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Palette
description: "Here is a sample code to run the "Anchor Rod - Imperial" tool available in the "Mechanical" ToolPalette in AutoCAD. It iterates the catalog items a..."
author: Autodesk
---
# Running a Tool from ToolPalette

发布日期: 2013-12-01

原始链接: https://adndevblog.typepad.com/autocad/2013/12/running-a-tool-from-toolpalette.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to run the "Anchor Rod - Imperial" tool available in the "Mechanical" ToolPalette in AutoCAD. It iterates the catalog items and executes the tool. It is similar to what a left mouse button click on the tool would do using the AutoCAD UI.
AcString toolName2Run = "Anchor Rod - Imperial";
  INT_PTR catalogCount = AcTcGetManager()->GetCatalogCount();
for( int catIndex = 0 ;
    (catIndex < catalogCount) && ! toolExecuted ;
     catIndex ++)
{
    AcTcCatalogItem *pCatItem
                    = AcTcGetManager()->GetCatalog(catIndex);
      INT_PTR nChildren1 = pCatItem->GetChildCount();
    for( int childIndex1 = 0 ;
         (childIndex1 < nChildren1) && ! toolExecuted;
         childIndex1++ )
    {
        AcTcCatalogItem *pCatItem1
                            = pCatItem->GetChild(childIndex1);
          INT_PTR nChildren2 = pCatItem1->GetChildCount();
        for( int childIndex2 = 0;
            (childIndex2 < nChildren2) && ! toolExecuted ;
            childIndex2++ )
        {
            AcTcCatalogItem *pCatItem2
                        = pCatItem1->GetChild(childIndex2);
              CatalogItemType ItemType = pCatItem2->GetType();
            if(ItemType == kItemTool )
            {
                AcTcTool *pTool
                        = static_cast<AcTcTool *>(pCatItem2);
                if (pTool != NULL)
                {
                    ACHAR szToolName[MAX_PATH];
                    pTool->GetName(szToolName, MAX_PATH);
                    if(toolName2Run.compareNoCase(
                                   AcString(szToolName)) == 0)
                    {
                        int nFlag = 0; // LButton clicked
                        HWND hWnd = NULL;
                        POINT point;
                        point.x = 0; point.y = 0;
                        DWORD dwKeyState = 0;
                        toolExecuted
                            = pTool->Execute( nFlag,
                                              hWnd,
                                              point,
                                              dwKeyState
                                            );
                    }
                }
            }
        }
    }
}

