---
title: "Querying the file paths of raster images in a drawing"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - Database
  - ObjectARX
description: "Just like a block reference (INSERT) entity refers to the underlying definition in a the block table, the raster image reference (IMAGE) entity ref..."
author: Autodesk
---
# Querying the file paths of raster images in a drawing

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/querying-the-file-paths-of-raster-images-in-a-drawing.html

## 文章内容

By Gopinath Taget
Just like a block reference (INSERT) entity refers to the underlying definition in a the block table, the raster image reference (IMAGE) entity refers to an underlying definition in a dictionary 'ACAD_IMAGE_DICT'. Using ObjectARX you can open up each AcDbRasterImageDef entry and retrieve its path information as shown in the sample ARX code below:
void ImagePath()
{
AcDbDictionary *pDict;
Acad::ErrorStatus es;
es=acdbHostApplicationServices()->workingDatabase()->
  getNamedObjectsDictionary(pDict, AcDb::kForRead);
 if (Acad::eOk != es)
{
  return;
}
  pDict->close();
AcDbObject *dictObj;
es=pDict->getAt(_T("ACAD_IMAGE_DICT"), dictObj, AcDb::kForRead);
 if (Acad::eOk != es)
{
  return;
}
  AcDbDictionary *dictImg = AcDbDictionary::cast(dictObj);
 if (NULL == dictImg)
{
  dictObj->close();
  return;
}
  AcDbDictionaryIterator *pIter;
AcDbObject *pObj;
pIter = dictImg->newIterator();
AcDbRasterImageDef *imgDef;
 for(; !pIter->done(); pIter->next())
{
  pIter->getObject(pObj, AcDb::kForRead);
  imgDef = AcDbRasterImageDef::cast(pObj);
  if (NULL != imgDef)
  {
   acutPrintf(_T("Image found at: "));
   acutPrintf(imgDef->activeFileName());
   acutPrintf(_T("\n"));
  }
  imgDef->close();
}
 delete pIter;
dictObj->close();
}

## 评论

**内容**: Mike Beebe said...
I'm currently researching if I can somehow programmatically change the path to raster images in thousands of drawings because we're wanting to restructure our folders on the network. It world be great if I can simply change the path property (Found At and/or Saved At) but if that's not possible then plan B is to collect enough info from the AcDbRasterImageDef and AcadRasterImage objects, detach it, copy the image file to the new location then attach it from the new location using the info collected. I'm hoping someone can shed some light, thank you.
Reply
09/24/2015 at 07:46 AM

---
