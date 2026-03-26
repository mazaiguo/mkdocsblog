---
title: "getDimstyleData() does not work for some Dimensions"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Dimension
description: "AcDbDimension::getDimstyleData() will fail on a dimension which has no dimstyle overrides (xdata's). To avoid the problem, ask with xData() if a di..."
author: Autodesk
---
# getDimstyleData() does not work for some Dimensions

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/getdimstyledata-does-not-work-for-some-dimensions.html

## 文章内容

By Augusto Goncalves
AcDbDimension::getDimstyleData() will fail on a dimension which has no dimstyle overrides (xdata's). To avoid the problem, ask with xData() if a dimension objects has dimstyle overrides. The following function will do this. The first parameter is the dimension from which to get the dimension style and the second parameter is an already allocated AcDbDimStyleTableRecord which will receive the dimension style.
Acad::ErrorStatus getDimstyleDataFromDimension(
  AcDbDimension *pDim,
  AcDbDimStyleTableRecord*& pDimStyle)
{
  Acad::ErrorStatus es;
    if (!pDim) return Acad::eNullEntityPointer;
    // Check if there are any XData's
  resbuf *xdata = pDim->xData(_T("ACAD"));
    if (xdata != NULL) {
      // Use getDimstyleData()
    if (Acad::eOk != (es = pDim->getDimstyleData(pDimStyle))) {
      return es;
    }
  } else {
      // Get information from original dimension style.
    // Because there are no dimstyle overrides you can
    // work with a 'normal' copy of the original style.
    AcDbObjectId dimstyleId = pDim->dimensionStyle();
    AcDbDimStyleTableRecord *pDimStyleTableRec;
      if (Acad::eOk != (es =
      acdbOpenObject(pDimStyleTableRec,
      dimstyleId, AcDb::kForRead)))
      return es;
      pDimStyle->copyFrom(pDimStyleTableRec);
      pDimStyleTableRec->close();
  }
    return Acad::eOk;
}

