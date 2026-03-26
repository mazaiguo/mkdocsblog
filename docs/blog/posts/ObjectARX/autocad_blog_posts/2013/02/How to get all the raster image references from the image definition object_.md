---
title: "How to get all the raster image references from the image definition object?"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - DWG
description: "If the raster images were correctly created, then each AcDbRasterImage object has an AcDbRasterImageDefReactor attached to it."
author: Autodesk
---
# How to get all the raster image references from the image definition object?

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/how-to-get-all-the-raster-image-references-from-the-image-definition-object.html

## 文章内容

By Gopinath Taget
If the raster images were correctly created, then each AcDbRasterImage object has an AcDbRasterImageDefReactor attached to it.
A particular AcDbRasterImageDef object will contain soft pointer references to these reactors, so if you create a custom filer class, deriving from AcDbDwgFiler, you can easily retrieve the sofPointers Id of the reactor when calling "dwgOut()" on your image definition. Once you have collected the reactors, open the "owner" object, which is one of the RasterImages referencing this definition.
Below is the relevant code. Here is the the full project.
void GetRasterImageReferences(const ACHAR* strRasterImgName)
{
Acad::ErrorStatus es;
  AcDbObjectId dicoId;
   if((dicoId = AcDbRasterImageDef::imageDictionary(acdbCurDwg()))
  == AcDbObjectId::kNull)
{
  acutPrintf(L"\nImage dictionary does not exist...");
  return;
}
  AcDbDictionary* pDict;
 if((es = acdbOpenObject((AcDbObject*&)pDict,
  dicoId, AcDb::kForRead)) != Acad::eOk)
{
  acutPrintf(L"\nCould not open image dictionary...");
  return;
}
    AcDbRasterImageDef* pImageDef;
   if (!pDict->has(strRasterImgName))
{
  acutPrintf(L"\nImage dictionary does not \
     contain specified definition...");
  return;
}
  es = pDict->getAt(strRasterImgName,
  (AcDbObject*&)pImageDef, AcDb::kForRead);
pDict->close();
  AcDbObjectIdArray hardPointerIds;
AcDbObjectIdArray softPointerIds;
AcDbObjectIdArray hardOwnershipIds;
AcDbObjectIdArray softOwnershipIds;
        asdkReferencesFiler filer;
  pImageDef->dwgOut(&filer);
    pImageDef->close();
      hardPointerIds   = filer.m_hardPointerIds;
    softPointerIds   = filer.m_softPointerIds;
    hardOwnershipIds = filer.m_hardOwnershipIds;
    softOwnershipIds = filer.m_softOwnershipIds;
     for (int i = 0; i < softPointerIds.length(); i++)
{
  AcDbObject* pReference;
  if((es = acdbOpenObject((AcDbObject*&)pReference,
   softPointerIds[i], AcDb::kForRead)) != Acad::eOk)
  {
   acutPrintf(L"\nCould not open object");
   continue;
  }
    //acutPrintf(L"\nReference type: %s", pReference->isA()->name());
    AcDbRasterImageDefReactor* pImgReactor = NULL;
    if ((pImgReactor =
   AcDbRasterImageDefReactor::cast(pReference)) != NULL )
  {
   AcDbRasterImage* pImgReference;
   if((es = acdbOpenObject((AcDbObject*&)pImgReference,
    pImgReactor->ownerId(), AcDb::kForRead)) != Acad::eOk)
   {
    acutPrintf(L"\nCould not open image ref...");
   }
   else
   {
    AcDbExtents extents;
    pImgReference->getGeomExtents(extents);
      acutPrintf(L"\nImage Reference position: [%f, %f, %f]",
     extents.minPoint().x, extents.minPoint().y,
     extents.minPoint().z);
    pImgReference->close();
   }
  } 
    pReference->close();
}
  }

