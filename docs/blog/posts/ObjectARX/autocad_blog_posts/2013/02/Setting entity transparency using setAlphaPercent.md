---
title: "Setting entity transparency using setAlphaPercent"
date: 2013-02-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "Here is a sample ObjectARX code to set the entity transparency using the "setAlphaPecent" method. This method can be used instead of the "setAlpha"..."
author: Autodesk
---
# Setting entity transparency using setAlphaPercent

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/setting-entity-transparency-using-setalphapercent.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample ObjectARX code to set the entity transparency using the "setAlphaPecent" method. This method can be used instead of the "setAlpha" method if you want to specify the alpha value in percentage.
ads_name ename;
ads_point pickPt;
  int rc = acedEntSel(_T("\nSelect Entity"), ename, pickPt);
if (rc != RTNORM)
    return;
  AcDbObjectId entId = AcDbObjectId::kNull;
acdbGetObjectId(entId, ename);
  AcDbEntity *pEntity = NULL;
Acad::ErrorStatus es
        = acdbOpenAcDbEntity(pEntity, entId, AcDb::kForRead);
  AcCmTransparency trans = pEntity->transparency();
  Adesk::UInt8 value = trans.alpha();
double percentage = value * 100.0 / 255.0;
acutPrintf(_T("Entity transparency Value : %d Percent : %lf"),
                                           value, percentage);
  pEntity->upgradeOpen();
  int nAlphaPercent = 1;
acedInitGet(RSG_NONULL + RSG_NONEG, NULL);
  // 100 % alpha - Fully opaque
// 0 % alpha - Fully transparent
rc = acedGetInt(_T("\nTransparency percentage (0 to 100):"),
                                               &nAlphaPercent);
if (rc != RTNORM)
    return;
  AcCmTransparency transparency1;
transparency1.setAlphaPercent(1.0 - (nAlphaPercent * 0.01));
  // To ensure that the transparency takes effect
pEntity->setColorIndex (pEntity->colorIndex());
  pEntity->setTransparency(transparency1);
  pEntity->close();
acDocManager->sendStringToExecute(
                    acDocManager->curDocument(), _T("_Regen "));

