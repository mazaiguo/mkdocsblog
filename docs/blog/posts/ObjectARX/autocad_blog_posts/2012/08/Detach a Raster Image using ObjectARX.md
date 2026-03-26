---
title: "Detach a Raster Image using ObjectARX"
date: 2012-08-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Database
  - ObjectARX
description: "To delete a raster image, first remove the AcDbRasterImageDef reference from the dictionary. Then erase the AcDbRasterImageDef object from AutoCAD ..."
author: Autodesk
---
# Detach a Raster Image using ObjectARX

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/detach-a-raster-image-using-objectarx.html

## 文章内容

By Augusto Goncalves
To delete a raster image, first remove the AcDbRasterImageDef reference from the dictionary. Then erase the AcDbRasterImageDef object from AutoCAD database. The following sample code demonstrates the process. A raster image named "rasterimage" is removed from the drawing.
static void AsdkDetachImage_detachimage()
{
  Acad::ErrorStatus es; 
  AcDbObjectId  imageDefId;
    // get the image definition dictionary
  AcDbDictionaryPointer pImageDict (
    AcDbRasterImageDef::imageDictionary (
    curDoc()->database()), AcDb::kForWrite);
  if ((es = pImageDict.openStatus ()) != Acad::eOk)
  {
    acutPrintf(acadErrorStatusText (es));
    return;
  }
  // get the object ID of the image definition
  if ((es = pImageDict->getAt (_T("rasterimage"),
    imageDefId)) != Acad::eOk)
  {
    pImageDict->close();
    acutPrintf(acadErrorStatusText (es));
    return;
  }
    // remove the image definition from the dictionary
  if ((es = pImageDict->remove (
    _T("rasterimage"))) != Acad::eOk)
  {
    pImageDict->close();
    acutPrintf(acadErrorStatusText (es));
    return;
  }
  pImageDict->close();
    //delete raster image definition object
  AcDbRasterImageDef * pImageDef;
  AcDbObject *pObj;
  if ((es = acdbOpenAcDbObject(pObj,
    imageDefId, AcDb::kForWrite)) != Acad::eOk)
  {
    acutPrintf(acadErrorStatusText (es));
    return;
  }
  pImageDef=(AcDbRasterImageDef *)pObj;
  if ((es = pImageDef->erase ()) != Acad::eOk)
  {
    pImageDef->close();
    acutPrintf(acadErrorStatusText (es));
    return;
  }
  pImageDef->close();
}

