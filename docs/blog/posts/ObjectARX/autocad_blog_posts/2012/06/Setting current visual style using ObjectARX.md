---
title: "Setting current visual style using ObjectARX"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "You can use function “acdbSetViewportVisualStyle” to set the required visual style. The example below sets the current visual style to Realistic."
author: Autodesk
---
# Setting current visual style using ObjectARX

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/setting-current-visual-style-using-objectarx.html

## 文章内容

By Virupaksha Aithal
You can use function “acdbSetViewportVisualStyle” to set the required visual style. The example below sets the current visual style to Realistic.
static void ASDK_test(void)
{
    ACHAR *name =  ACRX_T("REALISTIC");
    AcDbObjectId visualStyleId = AcDbObjectId::kNull;
      // Open the visual style dictionary for reading
    AcDbDictionary *pVisualStyleDict = NULL;
    Acad::ErrorStatus dbStatus;
    AcDbVisualStyle *pVisualStyleObj = NULL;
      AcDbDatabase *pDb =
            acdbHostApplicationServices()->workingDatabase();
      if (pDb->getVisualStyleDictionary(pVisualStyleDict,
                                AcDb::kForRead) == Acad::eOk)
    {
        // Get the visual style
        dbStatus = pVisualStyleDict->getAt(name,
            (AcDbObject *&)pVisualStyleObj, AcDb::kForWrite);
          if (dbStatus == Acad::eOk)
        {
            // Get the visual style's object ID
            visualStyleId = pVisualStyleObj->objectId();
            pVisualStyleObj->close();
        }
          pVisualStyleDict->close();
    }
    acdbSetViewportVisualStyle(visualStyleId);
}

