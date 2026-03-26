---
title: "Synchronizing model space viewports"
date: 2014-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Here is a sample code to synchronize the view parameters between two model space viewports. For simplicity, this sample code assumes that the drawi..."
author: Autodesk
---
# Synchronizing model space viewports

发布日期: 2014-07-01

原始链接: https://adndevblog.typepad.com/autocad/2014/07/synchronizing-model-space-viewports.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to synchronize the view parameters between two model space viewports. For simplicity, this sample code assumes that the drawing already has two vertically split model space viewports of equal width. If the model space viewports are manually resized to different widths, the code resizes them to be of equal width before synchronizing the view parameters.
To get view change notification, the sample code uses the "AcEditorReactor::viewChanged" event handler. Because a view changed notification by pan or mouse wheel does not fire the "viewChanged" notification, we also need to monitor mouse related windows messages using a message filter. After the view change occurs, we will sync the view parameters at the next right oppurtunity by waiting for AutoCAD to reach its quiescent state.
  Here are the relevant code snippets. The full sample project is available for download here :
SampleProject
 // Command to sync the model space viewport parameters 
 static  void  AdskMyTestSyncVTR()
 {
  // Get the VTR updated  
  acedVports2VportTableRecords();
    // We will update the other VTR only if  
  // view parameters change 
  Adesk::Boolean updateNeeded = Adesk::kFalse;
    Acad::ErrorStatus es;
  AcDbDatabase *pDb 
   = acdbHostApplicationServices()->workingDatabase();
    AcApDocument *pDoc = acDocManager->document(pDb);
  if ( pDoc == NULL )
   return ;
  es = acDocManager->lockDocument(pDoc);
    // This code at present can only deal with 2 Modelspace 
  // viewports split vertically in half 
  if (pDb->tilemode() == Adesk::kFalse)
  {
   struct  resbuf rb;
   if (ads_getvar(_T("cvport" ), &rb) != RTNORM)
   {
    acutPrintf(_T("\\nError using ads_getvar().\\n" ));
    return ;
   }
     if (rb.resval.rint == 1)
   {
    // Can only work with model space viewports. 
    return ;
   }
  }
    AcDbViewportTable *pVT = NULL; 
  pDb->getViewportTable(pVT,AcDb::kForRead);
     // Identify the left and right modelspace viewports 
  AcDbViewportTableRecord *pLeftVTR = NULL;
  AcDbViewportTableRecord *pRightVTR = NULL;
    AcDbViewportTableIterator *pIter = NULL;
  es = pVT->newIterator(pIter);
  if (es == Acad::eOk)
  {
   for  (;!pIter->done();pIter->step())
   {
    AcDbViewportTableRecord *pVTR = NULL;
    es = pIter->getRecord(pVTR, AcDb::kForRead);
    if (es == Acad::eOk)
    {
     AcGePoint2d ll = pVTR->lowerLeftCorner();
     AcGePoint2d ur = pVTR->upperRightCorner();
       if (ll.isEqualTo(AcGePoint2d(0, 0)))
     {// Left modelspace viewport 
      pLeftVTR = pVTR;
     }
     else  if (ur.isEqualTo(AcGePoint2d(1.0, 1.0)))
     {// Right modelspace viewport 
      pRightVTR = pVTR;
     }
     else 
      pVTR->close();
    }
   }
     // If for some reason, we did not have  
   // two modelspace viewports, lets stop here. 
   if (pLeftVTR == NULL)
   {
    if (pRightVTR != NULL)
     pRightVTR->close();
    return ;
   }
   if (pRightVTR == NULL)
   {
    if (pLeftVTR != NULL)
     pLeftVTR->close();
    return ;
   }
     // Ensure that the two viewports are split  
   // vertically in half. 
   // If not, the view parameters when applied  
   // from one to another may not apply directly  
   // using this code. 
   // If the viewports were resized manually,  
   // we will set them right. 
   AcGePoint2d ll1 = pLeftVTR->lowerLeftCorner();
   AcGePoint2d ur1 = pLeftVTR->upperRightCorner();
     AcGePoint2d ll2 = pRightVTR->lowerLeftCorner();
   AcGePoint2d ur2 = pRightVTR->upperRightCorner();
     if (ll1.isEqualTo(AcGePoint2d(0.0, 0.0)) == false )
   {
    if (! pLeftVTR->isWriteEnabled())
     pLeftVTR->upgradeOpen();
      pLeftVTR->setLowerLeftCorner
         (AcGePoint2d(0.0, 0.0));
   }
     if (ur1.isEqualTo(AcGePoint2d(0.5, 1.0)) == false )
   {
    if (! pLeftVTR->isWriteEnabled())
     pLeftVTR->upgradeOpen();
      pLeftVTR->setUpperRightCorner
         (AcGePoint2d(0.5, 1.0));
   }
     if (ll2.isEqualTo(AcGePoint2d(0.5, 0.0)) == false )
   {
    if (! pRightVTR->isWriteEnabled())
     pRightVTR->upgradeOpen();
      pRightVTR->setLowerLeftCorner
         (AcGePoint2d(0.5, 0.0));
   }
     if (ur2.isEqualTo(AcGePoint2d(1.0, 1.0)) == false )
   {
    if (! pRightVTR->isWriteEnabled())
     pRightVTR->upgradeOpen();
      pRightVTR->setUpperRightCorner
         (AcGePoint2d(1.0, 1.0));
   }
     // Get the active model space viewport 
   struct  resbuf res;
   acedGetVar(L"CVPORT" , &res); 
   short  vpnumber = res.resval.rint;
     // Identify the model space viewports  from/to which 
   // settings will be copied. 
   // The active modelspace viewport is the viewport  
   // from which settings will be copied 
   AcDbViewportTableRecord *pFromVTR = NULL;
   AcDbViewportTableRecord *pToVTR = NULL;
     if (pLeftVTR->number() == vpnumber)
   {
    pFromVTR = pLeftVTR;
    pToVTR = pRightVTR;
   }
   if (pRightVTR->number() == vpnumber)
   {
    pFromVTR = pRightVTR;
    pToVTR = pLeftVTR;
   }
     // Sorry, we did not identify the active viewport  
   // from which settings need to be copied. 
   if (pFromVTR == NULL || pToVTR == NULL)
    return ;
     // Copy the VTR settings from one modelspace viewport 
   // to another only if they are different. We will use 
   // a tolerance to ensure very small differences do not 
   // get us in a soup. I meant loop :) 
     AcGeTol newTol;
   newTol.setEqualPoint (0.00001);
   newTol.setEqualVector(0.00001);
     // ViewDirection 
   AcGeVector3d fromViewDir = pFromVTR->viewDirection();
   AcGeVector3d toViewDir = pToVTR->viewDirection();
   if (pFromVTR->viewDirection().isEqualTo(
     pToVTR->viewDirection(), newTol) == false )
   {
    if (! pToVTR->isWriteEnabled())
     pToVTR->upgradeOpen();
      pToVTR->setViewDirection(
        pFromVTR->viewDirection()); 
    updateNeeded = Adesk::kTrue;
   }
     // ViewTwist 
   if (abs(pFromVTR->viewTwist() 
       - pToVTR->viewTwist()) > 0.01)
   {
    if (! pToVTR->isWriteEnabled())
     pToVTR->upgradeOpen();
      pToVTR->setViewTwist(pFromVTR->viewTwist());
    updateNeeded = Adesk::kTrue;
   }
     // Target 
   if (pFromVTR->target().isEqualTo(
      pToVTR->target(), newTol) == false )
   {
    if (! pToVTR->isWriteEnabled())
     pToVTR->upgradeOpen();
      pToVTR->setTarget(pFromVTR->target()); 
    updateNeeded = Adesk::kTrue;
   }
     // BackClipEnabled 
   if (pFromVTR->backClipEnabled() 
       != pToVTR->backClipEnabled())
   {
    if (! pToVTR->isWriteEnabled())
     pToVTR->upgradeOpen();
    pToVTR->setBackClipEnabled(
       pFromVTR->backClipEnabled());
    updateNeeded = Adesk::kTrue;
   }
     // BackClipDistance 
   if (abs(pFromVTR->backClipDistance() 
     - pToVTR->backClipDistance()) > 0.01)
   {
    if (! pToVTR->isWriteEnabled())
     pToVTR->upgradeOpen();
      pToVTR->setBackClipDistance(
       pFromVTR->backClipDistance());
    updateNeeded = Adesk::kTrue;
   }
     // FrontClipEnabled 
   if (pFromVTR->frontClipEnabled() 
       != pToVTR->frontClipEnabled())
   {
    if (! pToVTR->isWriteEnabled())
     pToVTR->upgradeOpen();
    pToVTR->setFrontClipEnabled(
       pFromVTR->frontClipEnabled());
    updateNeeded = Adesk::kTrue;
   }
     // FrontClipDistance 
   if (abs(pFromVTR->frontClipDistance() 
      - pToVTR->frontClipDistance()) > 0.01)
   {
    if (! pToVTR->isWriteEnabled())
     pToVTR->upgradeOpen();
      pToVTR->setFrontClipDistance(
        pFromVTR->frontClipDistance());
    updateNeeded = Adesk::kTrue;
   }
     // Elevation 
   if (abs(pFromVTR->elevation() 
        - pToVTR->elevation()) > 0.01)
   {
    if (! pToVTR->isWriteEnabled())
     pToVTR->upgradeOpen();
      pToVTR->setElevation(pFromVTR->elevation());
    updateNeeded = Adesk::kTrue;
   }
     // centerPoint 
   if (pFromVTR->centerPoint().isEqualTo(
      pToVTR->centerPoint(), newTol) == false )
   {
    if (! pToVTR->isWriteEnabled())
     pToVTR->upgradeOpen();
      pToVTR->setCenterPoint(pFromVTR->centerPoint()); 
    updateNeeded = Adesk::kTrue;
   }
     // Height 
   if (abs(pFromVTR->height() - pToVTR->height()) > 0.01)
   {
    if (! pToVTR->isWriteEnabled())
     pToVTR->upgradeOpen();
      pToVTR->setHeight(pFromVTR->height());
    updateNeeded = Adesk::kTrue;
   }
     // Width 
   if (abs(pFromVTR->width() - pToVTR->width()) > 0.01)
   {
    if (! pToVTR->isWriteEnabled())
     pToVTR->upgradeOpen();
      pToVTR->setWidth(pFromVTR->width());
    updateNeeded = Adesk::kTrue;
   }
     // Done with the VTR 
   pLeftVTR->close();
   pRightVTR->close();
     delete  pIter;
  }
  es = pVT->close();
    es = acDocManager->unlockDocument(pDoc);
    // Update the Vports if we did change any of  
  // the VTR parameters 
  if (updateNeeded)
  {
   acedVportTableRecords2Vports();
  }
 }
   // Viewchanged notification is not received during  
 // a pan or zoom using mouse wheel. 
 // So identify those using WM messages. 
 BOOL WinCallBack(MSG *pMsg)
 {
  if ( pMsg->message == WM_VSCROLL   || 
   pMsg->message == WM_HSCROLL   ||
   pMsg->message == WM_MOUSEWHEEL   ||
   pMsg->message == WM_MBUTTONUP)
  {
   // Sync the modelspace viewports 
   acDocManager->sendStringToExecute(
    acDocManager->mdiActiveDocument(), 
    ACRX_T("SyncVTR " ), 
    false , true , false ); 
  } 
  return  FALSE;
 }
   // Setting up reactors and message filter 
 virtual  AcRx::AppRetCode On_kInitAppMsg (void  *pkt) 
 {
  AcRx::AppRetCode retCode 
     = AcRxArxApp::On_kInitAppMsg (pkt) ;
    // Editor reactor to receive to ViewChanged notification 
  pEditorReactor = new  AcMyEditorReactor(true );
    // InputContext reactor to receive quiescent state 
  // change notification 
  pInputContextReactor = new  AcMyInputContextReactor();
    // Viewchanged notification is not received during a  
  // pan or zoom using mouse wheel. 
  // So identify those using WM messages. 
  acedRegisterFilterWinMsg(WinCallBack);
    return  (retCode);
 }
   // Cleanup of the reactors and message filter 
 virtual  AcRx::AppRetCode On_kUnloadAppMsg (void  *pkt) 
 {
  AcRx::AppRetCode retCode 
     =AcRxArxApp::On_kUnloadAppMsg (pkt) ;
    // cleanup 
  if (pEditorReactor)
  {
   delete  pEditorReactor;
   pEditorReactor = NULL;
  }
    if (pInputContextReactor)
  {
   delete  pInputContextReactor;
   pInputContextReactor = NULL;
  }
    acedRemoveFilterWinMsg(WinCallBack);
    return  (retCode);
 }
   // Overridden beginQuiescentState method to initiate a sync 
 void  AcMyInputContextReactor::beginQuiescentState()
 {
  // See if the view has changed 
  if (_viewChanged)
  {
   // Sync the view once 
   _viewChanged = false ;
     // Send a command to Sync the modelspace viewports 
   acDocManager->sendStringToExecute(
    acDocManager->mdiActiveDocument(), 
    ACRX_T("SyncVTR " ), 
    false , true , false ); 
  }
 }
   // Overridden viewChanged method to know if the view changed 
 void  AcMyEditorReactor::viewChanged()
 {
  // View changed notification is received several times 
  // and we only want to sync the view parameters when  
  // AutoCAD attains a quiescent state next time. 
  // So only flaggin to sync in  
  // InputContextReactor::beginQuiescentState event handler. 
  AcMyInputContextReactor::_viewChanged = true ;
 }

## 评论

**内容**: Wojciech said...
Great job! There seems to be a bit of trouble in building with different VS versions, could you please provide a built version for AutoCad 2014 ? Many thanks!
Reply
10/23/2015 at 04:34 PM

---
**内容**: Balaji said...
Hi Wojciech,
Sorry, we do not provide binaries.
But, it should be possible to build it by downloading the sample project attached to the blog post.
For AutoCAD 2014, the platform toolset while building the sample project is to be set as v100.
"v100" should get listed in the toolset dropdown in any of the Visual Studio versions, if VS 2010 is installed is also installed in the system.
If there are specific issues that you face in getting it to work with AutoCAD 2014, please let me know.
Regards,
Balaji
Reply
10/24/2015 at 04:54 AM

---
**内容**: Briam Ramon said...
Un gran trabajo, no se mucho de C++ podrían indicarme como es la forma de cargar el .arx a AutoCAD, ya que el archivo adjunto cuando se esta compilando da error por no tener un archivo de esa extensión, utilizo VS2019, si no es mucha molestia agradecería me ayudaran a poder iniciar con este código. Agradezco de antemano
Reply
04/28/2021 at 09:39 AM

---
