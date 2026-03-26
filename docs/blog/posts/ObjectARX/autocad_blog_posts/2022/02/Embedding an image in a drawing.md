---
title: "Embedding an image in a drawing"
date: 2022-02-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
description: "In this blog post we will look at creating a custom object derived from AcDbRasterImageDef that saves/loads the image data to/from the drawing usin..."
author: Autodesk
---
# Embedding an image in a drawing

发布日期: 2022-02-01

原始链接: https://adndevblog.typepad.com/autocad/2022/02/embedding-an-image-in-a-drawing.html

## 文章内容

By Balaji Ramamoorthy
In this blog post we will look at creating a custom object derived from AcDbRasterImageDef that saves/loads the image data to/from the drawing using ATIL. This will ensure that your drawing is independent of the external image file and the image data will get loaded to the AcDbRasterImageDef if the arx is loaded in AutoCAD.
For other ways to embed an image in a drawing without having a dependency on an external image file, please refer to this blog post :
Embedding an image in a drawing
 // AcDbMyRasterImageDef.h 
 class  DLLIMPEXP AcDbMyRasterImageDef : 
  public  AcDbRasterImageDef 
 {
 protected :
  static  Adesk::UInt32 kCurrentVersionNumber;
   public :
    ACRX_DECLARE_MEMBERS(AcDbMyRasterImageDef) ;
     AcDbMyRasterImageDef () ;
  virtual  ~AcDbMyRasterImageDef () ;
    virtual  Acad::ErrorStatus 
   dwgOutFields (AcDbDwgFiler *pFiler) const  ;
    virtual  Acad::ErrorStatus dwgInFields 
   (AcDbDwgFiler *pFiler) ;
    //----- deepClone 
  virtual  Acad::ErrorStatus 
   subDeepClone (AcDbObject *pOwnerObject, 
   AcDbObject *&pClonedObject, AcDbIdMapping &idMap, 
   Adesk::Boolean isPrimary =true ) const  ;
    //----- wblockClone 
  virtual  Acad::ErrorStatus subWblockClone 
   (AcRxObject *pOwnerObject, AcDbObject *&pClonedObject, 
   AcDbIdMapping &idMap, Adesk::Boolean isPrimary =true )
   const  ;
        Acad::ErrorStatus 
   setEmbeddedImage(const  ACHAR* imageFilePath);
   private :
  void  *operator  new [](size_t) throw (){ return  (void *)0;}
     void  operator  delete [](void  *) {};
     void  *operator  new [](size_t , const  char  *, int  ) throw ()
  { return  (void *)0;}
    Atil::Image *m_pAtilImage;
 };
     // AcDbMyRasterImageDef.cpp 
 AcDbMyRasterImageDef::AcDbMyRasterImageDef () 
  : AcDbRasterImageDef () 
 {
  m_pAtilImage = NULL;
 }
   AcDbMyRasterImageDef::~AcDbMyRasterImageDef() 
 {
  if (m_pAtilImage != NULL)
  {
   delete  m_pAtilImage;
   m_pAtilImage = NULL;
  }
 }
   Acad::ErrorStatus AcDbMyRasterImageDef::dwgOutFields
  (AcDbDwgFiler *pFiler) const  {
  assertReadEnabled () ;
  //----- Save parent class information first. 
  Acad::ErrorStatus es =
   AcDbRasterImageDef::dwgOutFields (pFiler) ;
  if  ( es != Acad::eOk )
   return  (es) ;
  //----- Object version number needs to be saved first 
  if  ( (es =pFiler->writeUInt32 
   (AcDbMyRasterImageDef::kCurrentVersionNumber))
   != Acad::eOk )
   return  (es) ;
    if (m_pAtilImage)
  {
   Atil::Size size = m_pAtilImage->size();
   Int32 width = size.width;
   Int32 height = size.height;
     pFiler->writeInt32(width);
   pFiler->writeInt32(height);
     // Write the image data on to the Atil image 
   // using an Image Context 
   Atil::Offset upperLeft(0,0);
   Atil::ImageContext *pImgContext 
    = m_pAtilImage->createContext(
     Atil::ImageContext::kRead,
     size,
     upperLeft);
     if  (pImgContext != NULL)
   {
    for  (int  xf=0;xf<width;xf++)
    {
     for  (int  yf=0;yf<height;yf++)
     {
      Atil::RgbColor p;
      p = pImgContext->get32(xf, yf);
      pFiler->writeInt32(p.packed);
     }
    }
      }
   pImgContext->flush();
   delete  pImgContext;
  }
    return  (pFiler->filerStatus ()) ;
 }
   Acad::ErrorStatus AcDbMyRasterImageDef::dwgInFields
  (AcDbDwgFiler *pFiler) 
 {
  assertWriteEnabled () ;
  Acad::ErrorStatus es =
   AcDbRasterImageDef::dwgInFields (pFiler) ;
  if  ( es != Acad::eOk )
   return  (es) ;
     Adesk::UInt32 version =0 ;
  if  ( (es =pFiler->readUInt32 (&version)) 
   != Acad::eOk )
   return  (es) ;
  if  ( version > 
   AcDbMyRasterImageDef::kCurrentVersionNumber)
   return  (Acad::eMakeMeProxy) ;
    Int32 width = 0;
  Int32 height = 0;
    pFiler->readInt32(&width);
  pFiler->readInt32(&height);
    // Create an Atil::Image. 
     // The AcDbRasterImageDef::setImage requires it 
     Atil::ImagePixel initialImage;
     initialImage.setToZero();
     initialImage.type 
   = Atil::DataModelAttributes::kBgra;
     initialImage.value.rgba = 0xff000000;
        Atil::Size size(width, height);
     const  Atil::RgbModel *pDm 
   = new  Atil::RgbModel(
         Atil::RgbModelAttributes::k4Channels,
         Atil::DataModelAttributes::kBlueGreenRedAlpha);
     if (m_pAtilImage != NULL)
  {
   delete  m_pAtilImage;
   m_pAtilImage = NULL;
  }
     m_pAtilImage
   = new  Atil::Image(size, pDm, initialImage);
    // Write the image data on to the Atil image 
  // using an Image Context 
  Atil::Offset upperLeft(0,0);
  Atil::ImageContext *pImgContext 
   = m_pAtilImage->createContext(
     Atil::ImageContext::kWrite,
     size,
     upperLeft);
  if  (pImgContext != NULL)
  {
   for  (int  xf=0;xf<width;xf++)
   {
    for  (int  yf=0;yf<height;yf++)
    {
     Int32 value;
     pFiler->readInt32(&value);
     pImgContext->put32(xf, yf, value);
    }
   }
  }
  pImgContext->flush();
  delete  pImgContext;
    setImage (m_pAtilImage, NULL) ;
    return  (pFiler->filerStatus ()) ;
 }
   //----- deepClone 
 Acad::ErrorStatus AcDbMyRasterImageDef::subDeepClone 
  (AcDbObject *pOwnerObject, AcDbObject *&pClonedObject, 
  AcDbIdMapping &idMap, Adesk::Boolean isPrimary) const  
 {
  assertReadEnabled () ;
  return  (AcDbRasterImageDef::subDeepClone 
   (pOwnerObject, pClonedObject, idMap, isPrimary)) ;
 }
   //----- wblockClone 
 Acad::ErrorStatus AcDbMyRasterImageDef::subWblockClone 
  (AcRxObject *pOwnerObject, AcDbObject *&pClonedObject, 
  AcDbIdMapping &idMap, Adesk::Boolean isPrimary) const  
 {
  assertReadEnabled () ;
  return  (AcDbRasterImageDef::subWblockClone 
   (pOwnerObject, pClonedObject, idMap, isPrimary)) ;
 }
   Acad::ErrorStatus  AcDbMyRasterImageDef::setEmbeddedImage
        (const  ACHAR* imageFilePath)
 {
     AcString imagePath(imageFilePath);
        AcTcImage tc;
     tc.Load(imagePath);
        HBITMAP bmp=0;
     tc.GetHBITMAP(RGB(0xff,0xff,0xff),bmp);
        if  (bmp == NULL)
   return  Acad::eFileNotFound;
        BITMAP _bmp={0};
     GetObject(bmp,sizeof  BITMAP,&_bmp);
        HDC hdcScr=GetDC(NULL);
     HDC    hdcMem=CreateCompatibleDC(hdcScr);
     SelectObject(hdcMem,bmp);
        Atil::ImagePixel initialImage;
     initialImage.setToZero();
  initialImage.type = Atil::DataModelAttributes::kBgra;
     initialImage.value.rgba = 0xff000000;
        Atil::Size size(_bmp.bmWidth, _bmp.bmHeight);
     const  Atil::RgbModel *pDm = new  Atil::RgbModel(
         Atil::RgbModelAttributes::k4Channels,
         Atil::DataModelAttributes::kBlueGreenRedAlpha);
     if (m_pAtilImage != NULL)
  {
   delete  m_pAtilImage;
   m_pAtilImage = NULL;
  }
     m_pAtilImage 
   = new  Atil::Image(size, pDm, initialImage);
        Atil::Offset upperLeft(0,0);
     Atil::ImageContext *pImgContext
         = m_pAtilImage->createContext(
                     Atil::ImageContext::kWrite,
                     size,
                     upperLeft);
     if  (pImgContext != NULL)
     {
         for  (int  xf=0;xf<_bmp.bmWidth;xf++)
         {
             for  (int  yf=0;yf<_bmp.bmHeight;yf++)
             {
                 BYTE alpha= 0xff;
                 COLORREF pix=GetPixel(hdcMem,xf,yf);
                    BYTE rr = (pix&0xff);
                 BYTE gg = (pix>>8)&0xff;
                 BYTE bb = (pix>>16)&0xff;
                    Atil::RgbColor p;
                 p.set(rr, gg, bb, alpha);
                 pImgContext->put32(xf, yf, p);
             }
         }
     }
     pImgContext->flush();
     delete  pImgContext;
        bool  isImageValid = m_pAtilImage->isValid();
     assert(isImageValid);
        // Cleanup 
     DeleteDC(hdcMem);
     ReleaseDC(NULL,hdcScr);
        DeleteObject( bmp);
    return  setImage (m_pAtilImage, NULL) ;
 }
   // Embed image command 
 static  void  AdskMyTestEmbedImage(void )
 {
  AcDbMyRasterImageDef *pImageDef 
   = new  AcDbMyRasterImageDef();
  pImageDef->setEmbeddedImage(
   ACRX_T("D:\\TestFiles\\MyTexture.jpg" ));
  Acad::ErrorStatus es 
   = InsertImageInDwg(pImageDef);
  if (es != Acad::eOk)
  {
   delete  pImageDef;
   return ;
  }
 }
    static  Acad::ErrorStatus 
  InsertImageInDwg(AcDbRasterImageDef *pImageDef)
 {
  Acad::ErrorStatus es;
  if (! pImageDef->isLoaded())
  {
   es = pImageDef->load();
   if (es != Acad::eOk)
    return  es;
  }
     AcApDocument *pActiveDoc 
   = acDocManager->mdiActiveDocument();
  AcDbDatabase *pDB = pActiveDoc->database();
     // Get the image dictionary 
  // Create it if not available already 
  AcDbObjectId dictID
  = AcDbRasterImageDef::imageDictionary(pDB);
    if (dictID == AcDbObjectId::kNull)
  {
   es = AcDbRasterImageDef::createImageDictionary
    (pDB, dictID);
     if (es != Acad::eOk)
    return  es;
  }
     AcDbDictionary* pDict;
  es = acdbOpenObject(pDict, dictID, AcDb::kForWrite);
  if (es != Acad::eOk)
    return  es;
     ACHAR *DICT_NAME = ACRX_T("RASTER_USING_BUFFER" );
  BOOL bExist = pDict->has(DICT_NAME);
  AcDbObjectId objID = AcDbObjectId::kNull;
  if  (!bExist)
  {
   es = pDict->setAt(DICT_NAME, pImageDef, objID);
   if (es != Acad::eOk)
   {
    pDict->close();
    return  es;
   }
  }
  else 
  {
   pDict->getAt(DICT_NAME,
      (AcDbObject*&)pImageDef,
      AcDb::kForWrite);
   objID = pImageDef->objectId();
  }
     // close Dictionary and Definition. 
  pDict->close();
  pImageDef->close();
     // Create a raster image using the RasterImage Def 
  AcDbRasterImage* pImage = new  AcDbRasterImage;
  es = pImage->setImageDefId(objID);
  if  (es != Acad::eOk)
  {
   delete  pImage;
   return  es;
  }
     // Add the raster image to the model space 
  AcDbBlockTable* pBlockTable;
  AcDbBlockTableRecord* pBTRecord;
  es = acdbCurDwg()->getBlockTable(pBlockTable,
        AcDb::kForRead);
  assert(es == Acad::eOk);
  es = pBlockTable->getAt(ACDB_MODEL_SPACE,
        pBTRecord,
        AcDb::kForWrite);
  assert(es == Acad::eOk);
     es = pBTRecord->appendAcDbEntity(pImage);
  assert(es == Acad::eOk);
     pBTRecord->close();
  pBlockTable->close();
     AcDbObjectId entID = pImage->objectId();
     AcDbObjectPointer<AcDbRasterImageDefReactor>
       rasterImageDefReactor;
  rasterImageDefReactor.create();
     es = rasterImageDefReactor->setOwnerId(
        pImage->objectId());
  if  (es == Acad::eOk)
  {
   AcDbObjectId defReactorId;
   es = curDoc()->database()->addAcDbObject(
     defReactorId,
     rasterImageDefReactor.object());
      if  (es == Acad::eOk)
   {
    pImage->setReactorId(defReactorId);
    AcDbObjectPointer<AcDbRasterImageDef> 
     rasterImagedef
     (pImage->imageDefId(), AcDb::kForWrite);
    if  (rasterImagedef.openStatus() == Acad::eOk)
    {
     rasterImagedef->addPersistentReactor
       (defReactorId);
          }
   }
  }
     pImageDef->close();
  pImage->close();
    return  Acad::eOk;
 }
   virtual  AcRx::AppRetCode On_kInitAppMsg (void  *pkt) 
 {
  AcRx::AppRetCode retCode =
   AcRxArxApp::On_kInitAppMsg (pkt) ;
  acrxDynamicLinker->loadModule
   (L"acismobj20.dbx" ,true ); 
  AcDbMyRasterImageDef::rxInit();
  acrxBuildClassHierarchy();
  return  (retCode) ;
 }
  The sample project can be downloaded here :
Download EmbedImage
If you are looking to create an embedded raster image using the AutoCAD .Net API, a way to do it is by creating a managed wrapper for the custom object that we created. A .Net only solution is not possible at present since custom objects can only be created using C++. Also, ATIL is a C++ only library which we use in this case.
A way to access it in .Net is demonstrated in the following sample project. To try this sample, appload the .arx and netload the managed wrapper and custom .Net module. Run the "EmbedImageMgd" command.
Download CustomRasterImageDef
  Update:
the broker code is fixed and updated to ObjectARX 2022, is posted in Github
https://github.com/MadhukarMoogala/EmbedRasterImage

## 评论

**内容**: Dale Bartlett said...
Hi Balaji, Is there any way to achieve this with C#? Many thanks for your blog contributions by the way. Regards, Dale
Reply
07/26/2015 at 01:23 AM

---
**内容**: Balaji said in reply to Dale Bartlett...
Thanks Dale.
I have update the blog post to include another sample project.
A .Net only solution is not possible, but a managed wrapper can be created for the custom object and used from the .Net module.
Regards,
Balaji
Reply
07/26/2015 at 06:23 AM

---
**内容**: Dale Bartlett said...
Thanks Balaji, I'll have a play with this. Regards, Dale
Reply
07/27/2015 at 06:02 AM

---
**内容**: drift boss said...
I am a new bie of C#? Regarding your blog contributions, many thanks. Regards, Dale
Reply
09/19/2022 at 06:35 PM

---
**内容**: eggy car said...
It's so complex and hard for me to understand.
Reply
06/16/2023 at 12:50 AM

---
**内容**: Austin Keaney said...
I stumbled upon Mannen Gadgets while researching Beste powerbank options, and I must say their website is a treasure trove of tech insights. After reading their reviews, I finally found the perfect power bank that suits my needs. Thanks to Mannen Gadgets, I now have the confidence to make informed tech purchases!
Reply
09/12/2023 at 03:27 AM

---
**内容**: Tunnel Rush said...
This approach ensures that the drawing remains independent of external image files.
Reply
05/21/2024 at 01:53 AM

---
**内容**: love tester said...
Encourages Friendship Bonding
Love Tester isn’t just about romance—it’s also a fun way to test the compatibility of friendships. Playing the game with your best friend can spark giggles and deepen your bond.
Reply
12/09/2024 at 08:17 PM

---
