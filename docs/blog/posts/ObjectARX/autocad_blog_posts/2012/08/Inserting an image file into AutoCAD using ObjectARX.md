---
title: "Inserting an image file into AutoCAD using ObjectARX"
date: 2012-08-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "Inside ObjectARX, there are two classes that we use to represent images, one is AcDbRasterImage and the other is AcDbRasterImageDef."
author: Autodesk
---
# Inserting an image file into AutoCAD using ObjectARX

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/inserting-an-image-file-into-autocad-using-objectarx.html

## 文章内容

By Virupaksha Aithal
Inside ObjectARX, there are two classes that we use to represent images, one is AcDbRasterImage and the other is AcDbRasterImageDef.
The AcDbRasterImage entity (image entity) works with theAcDbRasterImageDef object (image definition object) to implement rasterimages inside AutoCAD. The relationship between these two classes is much likethe relationship between an AutoCAD block definition object and a block insert entity.
The image entity is a drawable, selectable AutoCAD entity that places a rasterimage in model or paper space at a particular location and orientation. The image entity is linked to exactly one image definition object, to which it sends requests for image processing operations needed for displaying and plotting images. Because the image definition object manages all the image information he image entity is relatively small. Besides the image location and orientation, it contains a clip boundary, image fade, contrast and brightness parameters and other typical AcDbEntity properties like layer and color.
void InsertImage()
{
    ACHAR* szName = _T("MyTest");
    ACHAR *fileName = _T("C:\\temp\\newImage.jpeg");
    AcGePoint3d org(10,10,0);
      AcDbDatabase *pDb =
      acdbHostApplicationServices()->workingDatabase();
       AcDbRasterImageDef* pImageDef = new AcDbRasterImageDef();
     Acad::ErrorStatus es = pImageDef->setSourceFileName(fileName);
     if(es != Acad::eOk)
     {
          delete pImageDef;
          return;
     }
     es = pImageDef->load();
     ASSERT(es == Acad::eOk);
     AcDbObjectId dictID = AcDbRasterImageDef::imageDictionary(pDb);
       if (dictID==AcDbObjectId::kNull)
     {
         es = AcDbRasterImageDef::createImageDictionary(pDb, dictID);
         if(es!= Acad::eOk)
         {
              delete pImageDef;
              ads_printf(_T("\nCould not create dictionary\n"));
              return;
         }
     }
     AcDbDictionary* pDict = NULL;
     es = acdbOpenObject((AcDbObject*&)pDict,
                                            dictID, AcDb::kForWrite);
     if(es != Acad::eOk)
     {
          delete pImageDef;
          ads_printf(_T("\nCould not open dictionary\n"));
          return;
     }
     BOOL bExist = pDict->has(szName);
     AcDbObjectId objID;
     if (!bExist)
     {
          pDict->setAt(szName, pImageDef, objID);
     }
     else
     {
          pDict->getAt(szName,
                    (AcDbObject*&)pImageDef,AcDb::kForWrite);
          objID = pImageDef->objectId();
     }
     // close Dictionary and Definition.
     pDict->close();
     pImageDef->close();
       AcDbRasterImage* pImage = new AcDbRasterImage;
     es = pImage->setImageDefId(objID);
     if (es != Acad::eOk)
     {
          delete pImage;
          return;
     }
      AcDbObjectId modelId;
    modelId = acdbSymUtil()->blockModelSpaceId(pDb);
      AcDbBlockTableRecord *pBTRecord;
    acdbOpenAcDbObject((AcDbObject*&)pBTRecord,
                                    modelId, AcDb::kForWrite);
       es = pBTRecord->appendAcDbEntity(pImage);
       pBTRecord->close();
     AcDbObjectId entID = pImage->objectId();
     AcGePoint3d TempPoint3d(3.0, 0, 0);
     AcGeVector3d LowerRightVector = TempPoint3d.asVector();
     AcGePoint3d TempPoint3d2(0, 1.5, 0);
     AcGeVector3d OnPlaneVector = TempPoint3d2.asVector();
     if (pImage->setOrientation(org,
                LowerRightVector, OnPlaneVector) !=Adesk::kTrue)
     {
          ads_printf(_T("\nSet Orientation failed."));
          pImage->close();
          return;
     }
     pImage->setDisplayOpt(AcDbRasterImage::kShow, Adesk::kTrue);
     pImage->setDisplayOpt(AcDbRasterImage::kTransparent,
                                                    Adesk::kTrue);
      AcDbObjectPointer<AcDbRasterImageDefReactor>
                                            rasterImageDefReactor;
      // new it
    rasterImageDefReactor.create();
      // Set the entity to be its owner.
    es = rasterImageDefReactor->setOwnerId(pImage->objectId());
      // if ok
    if (es == Acad::eOk)
    {
        AcDbObjectId defReactorId;
        // assign the object an objectId
        es = pDb->addAcDbObject(defReactorId,
                            rasterImageDefReactor.object());
          // if ok
        if (es == Acad::eOk)
        {
            // set the image reactor id
            pImage->setReactorId(defReactorId);
              AcDbObjectPointer<AcDbRasterImageDef>
                rasterImagedef(pImage->imageDefId(),
                                            AcDb::kForWrite);
              // if ok
            if (rasterImagedef.openStatus() == Acad::eOk)
            {
                rasterImagedef->addPersistentReactor(defReactorId);
            }
        }
    }
       pImage->close();
}

## 评论

**内容**: Mehmet Kurt said...
Hi,
How To insert bitmap file to Autocad DWG as an OLE embedde object with C#?
Thanks
Reply
08/08/2012 at 06:55 AM

---
**内容**: Bryce said...
It might depend on the version of AutoCAD, but the above code can fail if you don't do this:
if (pDict->setAt(szName, pImageDef, objID) == eWrongObjectType)
{
AcDbRasterImage::rxInit();
AcDbRasterVariables::rxInit();
AcDbRasterImageDef::rxInit();
acrxBuildClassHierarchy();
pDict->setAt(szName, pImageDef, objID);
}
Reply
04/15/2014 at 02:55 PM

---
**内容**: Bryce said in reply to Bryce...
Actually, the code I posted above is insufficient. It will keep AutoCAD from crashing during the insertion, but as soon as it tries to use the reactor (i.e. screen redraw), there's an access violation, so something else needs to be initialized in the RasterImage subsystem. I can force initialization by calling an existing command like "IMAGEFRAME" or "IMAGECLIP", but I don't know how to initialize the RasterImage subsystem properly in C++. Does anyone know how?
Reply
04/17/2014 at 12:31 PM

---
**内容**: Bryce said in reply to Bryce...
I finally found the example of how to initialize the AcDbRasterImage subsystem. It doesn't involve any explicit calls to rxInit or anything like that, just a simple loadModule:
acrxDynamicLinker->loadModule("acISMobj15.dbx", true)
Reply
12/29/2014 at 07:28 AM

---
**内容**: aravindhan said...
hi sir

how to remove the frame in inserted image

Reply
05/13/2020 at 10:23 AM

---
**内容**: Mahdi Kooshesh said in reply to aravindhan...
You must change the line type of radterimage to a invisible line type (for invisible line type read this : https://forums.autodesk.com/t5/autocad-architecture-forum/invisible-linetype/td-p/3207240)
Or you can change IMAGEFRAME system variable to 0 but in this way all rasterimages in all files are affected.
Reply
06/12/2024 at 03:52 AM

---
