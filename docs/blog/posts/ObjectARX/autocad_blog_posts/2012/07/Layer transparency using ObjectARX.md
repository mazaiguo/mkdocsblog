---
title: "Layer transparency using ObjectARX"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Database
  - Layer
  - ObjectARX
description: "Below code sample shows the procedure to modify the “transparency” of the layer using ObjectARX. Below code makes the transparency of layer 0 as 60..."
author: Autodesk
---
# Layer transparency using ObjectARX

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/layer-transparency-using-objectarx.html

## 文章内容

By Virupaksha Aithal
Below code sample shows the procedure to modify the “transparency” of the layer using ObjectARX. Below code makes the transparency of layer 0 as 60%. It is required to call regen to make the “transparency” changes reflects on the screen.
void transparency()
{
    AcDbDatabase *pDb =
      acdbHostApplicationServices()->workingDatabase();
      AcDbLayerTable *pLayerTblSrc = NULL;
    AcDbLayerTableRecord *pLayerTblRcdSrc;
    AcDbObjectId layerId;
      Acad::ErrorStatus es =
        pDb->getLayerTable(pLayerTblSrc,AcDb::kForRead);
      if(es != Acad::eOk)
     return;
      pLayerTblSrc->getAt(_T("0"), pLayerTblRcdSrc,AcDb::kForRead);
    pLayerTblSrc->close();
      AcCmTransparency trans = pLayerTblRcdSrc->transparency();
      Adesk::UInt8 value = trans.alpha();
    int percentage = (int)(((255 - value) * 100) / 255);
      acutPrintf(_T("Layer 0 transparency is %d"), percentage);
      pLayerTblRcdSrc->upgradeOpen();
      //60%
    Adesk::UInt8 alpha = (255 * (100 - 60) / 100);
    AcCmTransparency newTrans(alpha);
    pLayerTblRcdSrc->setLineWeight(pLayerTblRcdSrc->lineWeight());
    pLayerTblRcdSrc->setTransparency(newTrans);
      pLayerTblRcdSrc->close();
      acDocManager->sendStringToExecute(acDocManager->curDocument(),
                                                    _T("_Regen "));
}

