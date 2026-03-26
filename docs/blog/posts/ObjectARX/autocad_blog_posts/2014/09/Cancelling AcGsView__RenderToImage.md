---
title: "Cancelling AcGsView::RenderToImage"
date: 2014-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "To interrupt and cancel the AcGsView::RenderToImage call while its doing the rendering, create a custom progress monitor class. In the class derive..."
author: Autodesk
---
# Cancelling AcGsView::RenderToImage

发布日期: 2014-09-01

原始链接: https://adndevblog.typepad.com/autocad/2014/09/cancelling-acgsviewrendertoimage.html

## 文章内容

By Balaji Ramamoorthy
To interrupt and cancel the AcGsView::RenderToImage call while its doing the rendering, create a custom progress monitor class. In the class derived from AcGsRenderProgressMonitor, override the OnProgress method and return true to stop the RenderToImage. AutoCAD UI may not react to mouse events when the rendering is underway. To ensure that the AutoCAD UI is responsive during the rendering and to let the user cancel the operation, pump the Windows messages from OnProgress method.
Here is a sample code snippet :
 #include  "acgsRender.h" 
   class  MyRenderProgressMonitor :
  public  AcGsRenderProgressMonitor
 {
 public :
  MyRenderProgressMonitor(void ){}
    ~MyRenderProgressMonitor(void ){}
    static  Adesk::Boolean gAbortRender;
    virtual  bool  OnProgress(Phase ePhase, 
       float  fProgress)
  {
   // Pump windows message to let AutoCAD 
   // respond to user interaction.  
   // User may want to cancel the rendering 
   CWinApp *app = acedGetAcadWinApp();
   CWnd *wnd = app->GetMainWnd ();
       MSG msg; 
   while  (::PeekMessage (&msg, wnd->m_hWnd, 
        0, 0, PM_NOREMOVE)) 
   { 
    if  (!app->PumpMessage()) 
    { 
     break ; 
    } 
   } 
     LONG lIdle = 0;
   while  (app->OnIdle (lIdle++));
     if (gAbortRender)
    return  true ;
   return  false ;
  }
     virtual  void  OnTile(int  x, int  y, int  w, 
     int  h, const  BYTE* pPixels)
  {}
    virtual  void  SetStatistics(
   const  AcGsRenderStatistics* pStats)
  {}
    virtual  bool  ShouldReuseDatabase()
       {return  false ;}
 };
   Adesk::Boolean 
  MyRenderProgressMonitor::gAbortRender
        = Adesk::kFalse;
  To use it, create an instance of the progress monitor class and use it with RenderToImage as in this code snippet :
 // pView is an AcGsView  
 // screenRect is an AcGsDCRect 
 MyRenderProgressMonitor pm;
 AcDbMentalRayRenderSettings mentalRayRenderer;
 bool  ok = pView->RenderToImage(
       &imgSource, 
       &mentalRayRenderer, 
       &pm, 
       screenRect);

## 评论

**内容**: Keroro68K said...
Does it work with AutoCAD2020?
Reply
12/10/2019 at 09:39 PM

---
