---
title: "DIM update command in ObjectARX"
date: 2012-09-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Database
  - Dimension
  - ObjectARX
description: "If you change some dimension variables (for example DIMTXT) and if you want to apply the changes to a dimension entity, you first have to create a ..."
author: Autodesk
---
# DIM update command in ObjectARX

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/dim-update-command-in-objectarx.html

## 文章内容

By Augusto Goncalves
If you change some dimension variables (for example DIMTXT) and if you want to apply the changes to a dimension entity, you first have to create a new temporary dimension style which contains the actual dimension variables. Then you can assign this temporary style to a dimension.
To build the temporary dimension style you have to use the function AcDbDatabase::getDimstyleData(). This function applies the current dimension variables to a dimension style. Then use AcDbDimension::setDimstyleData() to apply this style to a dimension.
The following codes shows how to get a dimension entity and to assign the current dimension settings to it:
//
// Get dimension entity
//
ads_name ename;
ads_point pt;
if (RTNORM != ads_entsel(_T("\nSelect dimension: "), ename, pt))
  return;
  AcDbObjectId objId;
AcDbEntity *pEnt;
  acdbGetObjectId(objId, ename);
if (Acad::eOk != acdbOpenAcDbEntity(pEnt, objId, AcDb::kForRead)) {
  ads_printf(_T("\nCannot open selected entity."));
  return;
}
  if (!pEnt->isKindOf(AcDbDimension::desc())) {
  ads_printf(_T("\nSelected entity is not a dimension."));
  pEnt->close();
  return;
}
  //
// Get current dimension var's and apply them to the dimension entity
// 
AcDbDimension *pDim = (AcDbDimension*) pEnt;
// Create the temporary dimension style
AcDbDimStyleTableRecord *pDimStyle = new AcDbDimStyleTableRecord;
// Apply the current dim var's to the temp dim style
acdbCurDwg()->getDimstyleData(pDimStyle);
  // Now assign this style to the selected dimension
pDim->upgradeOpen();
pDim->setDimstyleData(pDimStyle);
pDim->close();
  // Don't forget to delete the temporary dimension style
delete pDimStyle;

