---
title: "Rendering using RenderToImage API"
date: 2015-09-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - Database
  - ObjectARX
description: "As you may already know, the API for the graphics system changed in AutoCAD 2015 as explained in this blog post : Graphic changes in AutoCAD 2015. ..."
author: Autodesk
---
# Rendering using RenderToImage API

发布日期: 2015-09-01

原始链接: https://adndevblog.typepad.com/autocad/2015/09/rendering-using-rendertoimage-api-.html

## 文章内容

By Balaji Ramamoorthy
As you may already know, the API for the graphics system changed in AutoCAD 2015 as explained in this blog post : Graphic changes in AutoCAD 2015. Also, AutoCAD 2016 renders using the RapidRT renderer that replaced the MentalRay renderer that was used by the previous AutoCAD releases. To account for this, the "AcDbRapidRTRenderSettings" class was introduced in ObjectARX 2016. All these changes requires changes in your code if you rely on "AcGsView::RenderToImage" method to generate an image of an AutoCAD model.
Here is a code that should help generate the rendered image in previous releases and in AutoCAD 2016. To accommodate the various graphics system changes and the renderer, the below code makes extensive use of conditional compilation.
To try this, open a drawing and set the viewing direction in AutoCAD based on how you wish to generate the rendered image. Setup the rendering presets and render it in AutoCAD. After you are convinced with the results, make the render settings as current. This should save the render presets as Active. The above code, retrieves the render settings based on the active render preset and uses it to generate the rendered image.
 static  void  AdskMyTestRTITest(void )
 {
  AcDbDatabase *pDb 
   = acdbHostApplicationServices()->workingDatabase();
    AcGsManager *gsManager = acgsGetGsManager();
  if  (! gsManager)
   return ;
    #ifdef  ACAD2016 // 2016 and later uses RapidRT renderer 
   AcGsManager2 *gsManager2 
    = dynamic_cast <AcGsManager2 *>(gsManager);
   if  (! gsManager2)
    return ;
   AcGsKernelDescriptor descriptor;
   descriptor.addRequirement(
    AcGsKernelDescriptor::k3DRapidRTRendering);
   AcGsGraphicsKernel *pGraphicsKernel 
    = AcGsManager::acquireGraphicsKernel(descriptor);
   AcGsDevice *offDevice 
    = gsManager2->getOffScreenDevice(*pGraphicsKernel); 
   if  (! offDevice)
    return ;
  #elif  ACAD2015 
  // 2015 uses Mental Ray renderer. Includes GS API changes  
   AcGsKernelDescriptor descriptor;
   descriptor.addRequirement
    (AcGsKernelDescriptor::k3DDrawing);
   AcGsGraphicsKernel *pGraphicsKernel 
    = AcGsManager::acquireGraphicsKernel(descriptor);
   AcGsDevice *offDevice 
    = pGraphicsKernel->createOffScreenDevice();
   if  (! offDevice)
    return ;
  #else  // 2014 and earlier releases uses Mental ray renderer 
   AcGsClassFactory *factory 
    = gsManager->getGSClassFactory();
   if  (! factory)
    return ;
   AcGsDevice *offDevice 
    = factory->createOffScreenDevice();
   if  (! offDevice)
    return ;
  #endif 
    AcDbObjectId curVportId = AcDbObjectId::kNull;
  int  width = 10, height = 10;
    Adesk::IntDbId viewportObjectId;
  LONG_PTR acadWindowId;
  LONG_PTR viewportId;
    if  (pDb->tilemode()) 
  {// Modelspace 
   curVportId = acedActiveViewportId();
     struct  resbuf rb;
   int  rt = acedGetVar(_T("CVPORT" ), &rb);
   if (rt != RTNORM)
    return ;
       int  vportNum = rb.resval.rint;
     AcDbObjectPointer<AcDbViewportTableRecord> 
    curVTR (curVportId,AcDb::kForRead);
   if (curVTR.openStatus() == Acad::eOk)
   {
    curVTR.close();
   }
     int  l,r,b,t;
   acgsGetViewportInfo(vportNum,l,b,r,t);
   height = t - b - 1;
   width = r - l - 1;
     viewportObjectId = curVportId.asOldId();
   acadWindowId = vportNum;
   viewportId = curVportId.asOldId();
  } 
  else  
  {// Paperspace, but with a modelspace  
   // activated in viewport 
   curVportId = acedGetCurViewportObjectId();
     AcDbObjectPointer<AcDbViewport> 
    curVport (curVportId,AcDb::kForRead);
     if (curVport->number() < 2)
   {
    AfxMessageBox(_T("For Render to work,  
     modelspace in a viewport must be activated.")); 
    return ;
   }
     int  l,r,b,t;
   acgsGetViewportInfo(curVport->number(),l,b,r,t);
   height = t - b - 1;
   width = r - l - 1;
     viewportObjectId = curVportId.asOldId();
   acadWindowId = curVport->number();
   viewportId = curVportId.asOldId();
  }
    offDevice->onSize(width, height);
    #ifdef  ACAD2016
   AcGsClientViewInfo info;
   info.viewportId = viewportId;
   info.acadWindowId = acadWindowId;
   info.viewportObjectId = viewportObjectId;
   AcGsView* pView = 
   gsManager2->getOffScreenView(*pGraphicsKernel, info);
  #elif  ACAD2015
   AcGsView *pView = pGraphicsKernel->createView();
   if  (! pView)
    return ;
  #else 
   AcGsView *pView = factory->createView();
   if  (! pView)
    return ;
  #endif 
    acgsGetViewParameters(acadWindowId, pView);
  offDevice->setDeviceRenderer(AcGsDevice::kFullRender);
  offDevice->add(pView);
  offDevice->update();
    #if  defined (ACAD2016) || defined (ACAD2015)
   AcGsModel *pModel 
   = gsManager->createAutoCADModel(*pGraphicsKernel);
  #else 
   AcGsModel *pModel = gsManager->createAutoCADModel();
  #endif 
  if  (! pModel)
   return ;
    // Model space 
  AcDbBlockTable *pBT = NULL;
  AcDbBlockTableRecord *pBTR = NULL;
  AcDbObjectId msId;
  pDb->getBlockTable(pBT, AcDb::kForRead);
  pBT->getAt(ACDB_MODEL_SPACE, msId);
  pBT->close();
    AcDbBlockTableRecordPointer spaceRec(msId, AcDb::kForRead);
  if  (spaceRec.openStatus() != Acad::eOk)
   return ;
    pView->add(spaceRec, pModel);
  spaceRec.close();
    if  (pView != NULL)
  {
   pView->invalidate();
   pView->update();
  }
                  // get the filename to output 
  struct  resbuf *result = NULL;
  int  status = acedGetFileNavDialog(
   _T("Render Image" ), 
   NULL, 
   _T("jpg;png;tif;bmp" ), 
   _T("RenderImageDialog" ), 1, &result);  
  if  (status == RTNORM)
  {
   ACHAR *pFileName = result->resval.rstring;
   if  (! CreateAtilImage(
    pView, width, height, 32, 0, pFileName))
   AfxMessageBox(_T("Failed to create image..." ));
  }
    // now do the various GS clean up ops 
  pView->eraseAll();
  offDevice->erase(pView);
    #if  defined (ACAD2016)
   //pGraphicsKernel->deleteView(pView); 
   pGraphicsKernel->deleteModel(pModel);
   //pGraphicsKernel->deleteDevice(offDevice); 
   AcGsManager::releaseGraphicsKernel(pGraphicsKernel);
  #elif  ACAD2015
   pGraphicsKernel->deleteView(pView);
   pGraphicsKernel->deleteModel(pModel);
   pGraphicsKernel->deleteDevice(offDevice);
   AcGsManager::releaseGraphicsKernel(pGraphicsKernel);
  #else 
   factory->deleteView(pView);
   factory->deleteModel(pModel);
   factory->deleteDevice(offDevice);
  #endif 
 }
   #ifdef  ACAD2016
 static   Acad::ErrorStatus GetActiveRapidRTRenderSetting
  (AcDbRapidRTRenderSettings *&pRenderSetting)
 {
  AcApDocument *pActiveDoc = acDocManager->mdiActiveDocument();
  AcDbDatabase *pDB = pActiveDoc->database();
    AcDbDictionary *pNODContainer = NULL;
  Acad::ErrorStatus es 
   = pDB->getNamedObjectsDictionary
   (pNODContainer, 
   AcDb::OpenMode::kForRead); 
    AcDbObject *pMyDictObject = NULL;
  if (pNODContainer->has(
   ACRX_T("ACAD_RENDER_ACTIVE_RAPIDRT_SETTINGS" )))
  {
   es = pNODContainer->getAt(ACRX_T(
    "ACAD_RENDER_ACTIVE_RAPIDRT_SETTINGS" ), 
    pMyDictObject, AcDb::OpenMode::kForRead); 
   AcDbObjectId myObjectId = AcDbObjectId::kNull;
   if (es == Acad::eOk)
   {
    AcDbRapidRTRenderSettings *pRapidRTActiveSetting 
     = AcDbRapidRTRenderSettings::cast(pMyDictObject);
    if (pRapidRTActiveSetting != NULL)
    {
     pRenderSetting = new  AcDbRapidRTRenderSettings();
     es = pRenderSetting->copyFrom(pRapidRTActiveSetting);
    }
    es = pRapidRTActiveSetting->close();
   }
  }
  else 
  {
   acutPrintf(
   ACRX_T("ACAD_RENDER_ACTIVE_RAPIDRT_SETTINGS not found !!" ));
  }
  pNODContainer->close();
  return  Acad::eOk;
 }
    #else 
   static   Acad::ErrorStatus GetActiveRenderSetting
  (AcDbMentalRayRenderSettings *&pRenderSetting)
 {
  AcApDocument *pActiveDoc = acDocManager->mdiActiveDocument();
  AcDbDatabase *pDB = pActiveDoc->database();
    AcDbDictionary *pNODContainer = NULL;
  Acad::ErrorStatus es = pDB->getNamedObjectsDictionary
   (pNODContainer, AcDb::OpenMode::kForRead); 
    AcDbObject *pMyDictObject = NULL;
  if (pNODContainer->has(ACRX_T("ACAD_RENDER_ACTIVE_SETTINGS" )))
  {
   es = pNODContainer->getAt(
    ACRX_T("ACAD_RENDER_ACTIVE_SETTINGS" ), 
    pMyDictObject, AcDb::OpenMode::kForRead); 
     AcDbObjectId myObjectId = AcDbObjectId::kNull;
   if (es == Acad::eOk)
   {
    AcDbMentalRayRenderSettings 
     *pMentalRayActiveSetting = 
     AcDbMentalRayRenderSettings::cast(pMyDictObject);
    if (pMentalRayActiveSetting != NULL)
    {
     pRenderSetting = new  AcDbMentalRayRenderSettings();
     es = pRenderSetting->copyFrom(pMentalRayActiveSetting);
    }
    es = pMentalRayActiveSetting->close();
   }
  }
  else 
  {
   acutPrintf(ACRX_T("ACAD_RENDER_ACTIVE_SETTINGS not found !!" ));
  }
  pNODContainer->close();
  return  Acad::eOk;
 }
    #endif 
   static  bool  CreateAtilImage(AcGsView *pView, 
       int  width, int  height, 
       int  colorDepth, int  paletteSize, 
       ACHAR *pFileName)
 {
  bool  done = false ;
    AcGsDCRect screenRect(0,width-1,0, height-1);
      // we want colorDepth to be either 24 or 32 
  if  (colorDepth < 24)
   colorDepth = 24;
  if  (colorDepth > 24)
   colorDepth = 32;
    // create rbgmodel 32 bit true color 
  Atil::RgbModel rgbModel(colorDepth);
  Atil::ImagePixel initialColor(rgbModel.pixelType());
  // create the Atil image on the stack 
  Atil::Image imgSource
   (Atil::Size(width, height), 
   &rgbModel, initialColor);
    bool  ok = false ;
  #ifdef  ACAD2016 // 2016 uses Rapid RT renderer 
   AcDbRapidRTRenderSettings 
    *pCurrentSetting = NULL;
   Acad::ErrorStatus es 
    = GetActiveRapidRTRenderSetting(pCurrentSetting);
   if (pCurrentSetting != NULL)
   {
    ok = pView->renderToImage
     (&imgSource, pCurrentSetting, 
     nullptr , screenRect);
    delete  pCurrentSetting;
   }
  #else  // 2015 and earlier releases uses Mental Ray renderer 
   AcDbMentalRayRenderSettings *pCurrentSetting = NULL;
   Acad::ErrorStatus es 
    = GetActiveRenderSetting(pCurrentSetting);
   if (pCurrentSetting != NULL)
   {
    ok = pView->RenderToImage
     (&imgSource, pCurrentSetting, 
     nullptr , screenRect);
    delete  pCurrentSetting;
   }
  #endif 
    if  (!ok)
  {
   AfxMessageBox(_T("Failed to RenderToImage" ));
   return  false ;
  }
  else 
  {
   done = WriteImageToFile(&imgSource, pFileName); 
  }
  return  done;
 }
  The sample project and a drawing with render presets configured can be downloaded here :
Download RTI
Download Torus_2016
Here is a screenshot of the rendered image that was created in AutoCAD 2016 using the RapidRT renderer :

## 评论

**内容**: Christopher Fugitt said...
Why no .NET example?
Reply
09/24/2017 at 08:50 PM

---
**内容**: Maxence said...
Looks like it can't work in. NET because of bugs in the API. Check my post here: https://forums.autodesk.com/t5/net/rendertoimage/m-p/7567717/highlight/true#M56077
Reply
12/07/2017 at 12:32 AM

---
