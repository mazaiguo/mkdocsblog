---
title: "Integrating AutoCAD with Oculus Rift DK2"
date: 2015-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Solid
description: "Oculus Rift DK2 provides a great virtual reality experience that is very immersive. In this blog post, I have attached a sample project that enable..."
author: Autodesk
---
# Integrating AutoCAD with Oculus Rift DK2

发布日期: 2015-03-01

原始链接: https://adndevblog.typepad.com/autocad/2015/03/integrating-autocad-with-oculus-rift-dk2.html

## 文章内容

By Balaji Ramamoorthy
Oculus Rift DK2 provides a great virtual reality experience that is very immersive. In this blog post, I have attached a sample project that enables viewing solids from the drawing database for viewing in Oculus Rift. The code makes use of helper methods from the "Win32_DX11AppUtil" of the "OculusRoomTiny" sample which is included in the Oculus SDK. Some of the helper methods have also been modified to extend it for AutoCAD solids. Here is a short video before we look at the sample code.
Here is the relevant code snippet that renders the view. The full sample project can be downloaded here :
Download OVRAutoCADSolids
 CAcModuleResourceOverride resourceOverride;
   gpDX11 = new  DirectX11();
   // Initializes LibOVR, and the Rift 
 ovrBool ovrInitialized = ovr_Initialize();
 HMD = ovrHmd_Create(0);
   if  (!HMD)
 { 
  MessageBoxA(NULL,"Oculus Rift not detected." ,"" , MB_OK); 
  return ;
 }
   if  (HMD->ProductName[0] ==  )
 {
  MessageBoxA(NULL,
     "Rift detected, display not enabled." , 
     "" , MB_OK);
 }
   bool  windowed = (HMD->HmdCaps & ovrHmdCap_ExtendDesktop) 
                         ? false  : true ; 
   HINSTANCE hInstance = GetModuleHandle(NULL);
   CWinApp *app = acedGetAcadWinApp();
 CWnd *pWnd = app->GetMainWnd ();
 HWND hWndParent = pWnd->m_hWnd;
   gpDX11->InitWindowAndDevice(
                 hInstance, 
                 hWndParent, 
                 Recti(HMD->WindowsPos, HMD->Resolution), 
                 true );
   EnableWindow(hWndParent, FALSE);
   gpDX11->SetMaxFrameLatency(1);
 ovrHmd_AttachToWindow(HMD, gpDX11->Window, NULL, NULL);
 ovrHmd_SetEnabledCaps(
             HMD, 
             ovrHmdCap_LowPersistence | 
             ovrHmdCap_DynamicPrediction);
   ovrHmd_ConfigureTracking(HMD, 
             ovrTrackingCap_Orientation | 
             ovrTrackingCap_MagYawCorrection |
             ovrTrackingCap_Position, 0);
   for  (int  eye=0; eye<2; eye++)
 {
  Sizei idealSize = ovrHmd_GetFovTextureSize(
                     HMD, (ovrEyeType)eye,
      HMD->DefaultEyeFov[eye], 1.0f);
  pEyeRenderTexture[eye] 
                 = new  ImageBuffer(true , false , idealSize);
  pEyeDepthBuffer[eye]   
                 = new  ImageBuffer(
                         true , 
                         true , 
                         pEyeRenderTexture[eye]->Size);
  EyeRenderViewport[eye].Pos  = Vector2i(0, 0);
  EyeRenderViewport[eye].Size 
                 = pEyeRenderTexture[eye]->Size;
 }
   ovrD3D11Config d3d11cfg;
 d3d11cfg.D3D11.Header.API            
         = ovrRenderAPI_D3D11;
 d3d11cfg.D3D11.Header.BackBufferSize 
         = Sizei(HMD->Resolution.w, HMD->Resolution.h);
 d3d11cfg.D3D11.Header.Multisample    
         = 1;
 d3d11cfg.D3D11.pDevice               
         = gpDX11->Device;
 d3d11cfg.D3D11.pDeviceContext        
         = gpDX11->Context;
 d3d11cfg.D3D11.pBackBufferRT         
         = gpDX11->BackBufferRT;
 d3d11cfg.D3D11.pSwapChain            
         = gpDX11->SwapChain;
   if  (!ovrHmd_ConfigureRendering(HMD, &d3d11cfg.Config,
  ovrDistortionCap_Chromatic | ovrDistortionCap_Vignette |
  ovrDistortionCap_TimeWarp | ovrDistortionCap_Overdrive,
  HMD->DefaultEyeFov, EyeRenderDesc))
  return ;
   ovrHmd_DismissHSWDisplay(HMD);
   // Create the scene based on AutoCAD model  
 Acad::ErrorStatus es;
 AcDbDatabase *pDb 
     = acdbHostApplicationServices()->workingDatabase();
   AcDbBlockTable *pBlockTable;
 es = pDb->getSymbolTable(pBlockTable, AcDb::kForRead);
   AcDbBlockTableRecord *pMS = NULL;
 es = pBlockTable->getAt(
         ACDB_MODEL_SPACE, pMS, AcDb::kForRead);
 pBlockTable->close();
   Scene acadScene;
   AcDbBlockTableRecordIterator *pBTRIterator = NULL;
 es = pMS->newIterator(pBTRIterator);
 if  (es == Acad::eOk)
 {
     for  (pBTRIterator->start(); 
         ! pBTRIterator->done(); 
         pBTRIterator->step())
     {
   AcDbEntity *pEnt = NULL;
         es = pBTRIterator->getEntity(
                         pEnt, AcDb::kForRead);
         if  (es == Acad::eOk)
         {
    AcDb3dSolid *pSolid = NULL;
    AcDbSubDMesh *pSubDMesh = NULL;
             if  (pSolid = AcDb3dSolid::cast(pEnt))
             {//solid 
     AcDbFaceterSettings settings;
     settings.faceterMeshType = 2;
       AcDbExtents sldExtents;
     es = pSolid->getGeomExtents(sldExtents);
     AcGeVector3d dir = 
                 sldExtents.maxPoint() - sldExtents.minPoint();
                       settings.faceterMaxEdgeLength 
                                 = dir.length() * 0.02;
       AcGePoint3dArray vertices;
     AcArray<Adesk::Int32> faceArr; 
     AcGiFaceData* faceData;
     es = acdbGetObjectMesh(
                         pSolid, 
                         &settings, 
                         vertices, 
                         faceArr, 
                         faceData);
       if  (faceData) 
     {
      delete [] faceData->trueColors(); 
      delete [] faceData->materials();
      delete faceData;
     }
       AcArray<MeshVertex> modelVertices;
     AcArray<Adesk::Int32> modelFaceInfo;
       try 
     {
      AcArray<Adesk::Int32> faceVertices;
        int  verticesInFace = 0;
      int  facecnt = 0;
      for  (int  x = 0; x < faceArr.length(); 
                         facecnt++, x = x + verticesInFace + 1)
      {
       faceVertices.removeAll();
         verticesInFace = faceArr[x];
       for  (int  y = x + 1; 
                             y <= x + verticesInFace; y++)
       {
        faceVertices.append(faceArr[y]);
       }
         Adesk::Boolean continueCollinearCheck 
                                             = Adesk::kFalse;
       do 
       {
        continueCollinearCheck 
                                         = Adesk::kFalse;
        for  (int  index = 0; 
                             index < faceVertices.length(); 
                             index++)
        {
         int  v1 = index;
                                           int  v2 = 
                                 (index + 1) >= faceVertices.length() ? 
                                 (index + 1) - faceVertices.length() : 
                                 index + 1;
           int  v3 = 
                                 (index + 2) >= faceVertices.length() ? 
                                 (index + 2) - faceVertices.length() : 
                                 index + 2;
           // Check collinear 
         AcGePoint3d p1 
                                 = vertices[faceVertices[v1]];
                                           AcGePoint3d p2 
                                 = vertices[faceVertices[v2]];
                                           AcGePoint3d p3 
                                 = vertices[faceVertices[v3]];
           AcGeVector3d vec1 = p1 - p2;
         AcGeVector3d vec2 = p2 - p3;
         if  (vec1.isCodirectionalTo(vec2))
         {
          faceVertices.removeAt(v2);
          continueCollinearCheck 
                                     = Adesk::kTrue;
          break ;
         }
        }
       } while  (continueCollinearCheck);
         if  (faceVertices.length() == 3)
       {
        AcGePoint3d p1 
                             = vertices[faceVertices[0]];
                                      AcGePoint3d p2 
                             = vertices[faceVertices[1]];
                                      AcGePoint3d p3 
                             = vertices[faceVertices[2]];
          AppendVertex(
                             modelVertices, 
                             modelFaceInfo, 
                             p1, p2, p3);
       }
       else  if  (faceVertices.length() == 4)
       {
        AcGePoint3d p1 
                             = vertices[faceVertices[0]];
                                      AcGePoint3d p2 
                             = vertices[faceVertices[1]];
                                      AcGePoint3d p3 
                             = vertices[faceVertices[2]];
          AppendVertex(
                             modelVertices, 
                             modelFaceInfo, 
                             p1, p2, p3);
          p1 = 
                             vertices[faceVertices[2]];
                                      p2 = 
                             vertices[faceVertices[3]];
                                      p3 = 
                             vertices[faceVertices[0]];
          AppendVertex(
                             modelVertices, 
                             modelFaceInfo, 
                             p1, p2, p3);
       }
       else 
       {
        acutPrintf(
                             ACRX_T("Face with more than 4  
                             vertices will need triangulation 
                             to import in  Direct3D ")); 
       }
      }
     }
     catch (...)
     {
      acutPrintf(ACRX_T("Error !!" ));
      return ;
     }
       AcDbHandle handle 
                 = pSolid->objectId().handle();
                       ACHAR sHandle[50];
     handle.getIntoAsciiBuffer(sHandle);
       AcGePoint3d minPt = sldExtents.minPoint();
     AcGePoint3d maxPt = sldExtents.maxPoint();
       COLORREF colorRef = RGB(255, 255, 255);
     AcCmColor color = pSolid->color();
     Adesk::UInt8 blue, green, red;
     Adesk::UInt16 ACIindex;
     long  acirgb, r,g,b; 
     // get the RGB value as an Adesk::Int32 
     Adesk::Int32 nValue = color.color();
     // now extract the values 
     AcCmEntityColor::ColorMethod cMethod;
     cMethod = color.colorMethod();
     Model::Color modelColor;
     switch (cMethod)
     {
      case  AcCmEntityColor::kByColor :
       blue = nValue;
       nValue = nValue>>8;
       green = nValue;
       nValue = nValue>>8;
       red = nValue;
       modelColor.R = red;
       modelColor.G = green;
       modelColor.B = blue;
       colorRef = RGB(red, green, blue);
       break ;
        case  AcCmEntityColor::kByACI :
       ACIindex = color.colorIndex(); 
       acirgb = acedGetRGB ( ACIindex );
       r = ( acirgb & 0xffL ); 
       g = ( acirgb & 0xff00L ) >> 8;
       b = acirgb >> 16;
       modelColor.R = r;
       modelColor.G = g;
       modelColor.B = b;
       colorRef = RGB(r, g, b);
       break ;
        case  AcCmEntityColor::kByLayer :
       break ;
        default  :
       break ;
     }
       acadScene.AppendCustomModel(
                 modelVertices, 
                 modelFaceInfo, 
                 modelColor);
       modelVertices.removeAll();
     modelFaceInfo.removeAll();
             }
             pEnt->close();
         }
     }
     delete pBTRIterator;
 }
 pMS->close(); 
   while  (!(gpDX11->Key[ ] && 
         gpDX11->Key[VK_CONTROL]) && 
         ! gpDX11->Key[VK_ESCAPE])
 {
  gpDX11->HandleMessages();
    ovrVector3f useHmdToEyeViewOffset[2] = 
     {EyeRenderDesc[0].HmdToEyeViewOffset,
  EyeRenderDesc[1].HmdToEyeViewOffset};
         ovrHmd_BeginFrame(HMD, 0);
    // Keyboard inputs to adjust player orientation 
  if  (gpDX11->Key[VK_LEFT])  Yaw += 0.02f;
  if  (gpDX11->Key[VK_RIGHT]) Yaw -= 0.02f;
    // Keyboard inputs to adjust player position 
  if  (gpDX11->Key[ ]||gpDX11->Key[VK_UP])   
     Pos+=Matrix4f::RotationY(Yaw).
          Transform(Vector3f(0,0,-0.05f));
        if  (gpDX11->Key[ ]||gpDX11->Key[VK_DOWN]) 
     Pos+=Matrix4f::RotationY(Yaw).
         Transform(Vector3f(0,0,+0.05f));
    if  (gpDX11->Key[ ])
         Pos+=Matrix4f::RotationY(Yaw).
         Transform(Vector3f(0,+0.05f,0));
        if  (gpDX11->Key[ ])
         Pos+=Matrix4f::RotationY(Yaw).
         Transform(Vector3f(0,-0.05f,0));
    if  (gpDX11->Key[ ]) 
   Pos.y+=0.05f;
    if  (gpDX11->Key[ ])
   Pos.y-=0.05f;
      ovrPosef temp_EyeRenderPose[2];
  ovrHmd_GetEyePoses(
             HMD, 0, 
             useHmdToEyeViewOffset, 
             temp_EyeRenderPose, NULL);
    // Render the two undistorted eye views  
  for  (int  eye = 0; eye < 2; eye++)
  {
   ImageBuffer * useBuffer
         = pEyeRenderTexture[eye];  
             ovrPosef    * useEyePose
         = &EyeRenderPose[eye];
             float  * useYaw
         = &YawAtRender[eye];
             bool  clearEyeImage  = true ;
   bool  updateEyeImage = true ;
     if  (clearEyeImage)
    gpDX11->ClearAndSetRenderTarget(
             useBuffer->TexRtv,
    pEyeDepthBuffer[eye], 
             Recti(EyeRenderViewport[eye]));
     if  (updateEyeImage)
   {
    *useEyePose = temp_EyeRenderPose[eye];
    *useYaw     = Yaw;
      // Get view and projection matrices 
    Matrix4f rollPitchYaw       
             = Matrix4f::RotationY(Yaw);
                  Matrix4f finalRollPitchYaw
             = rollPitchYaw * Matrix4f(useEyePose->Orientation);
                  Vector3f finalUp
             = finalRollPitchYaw.Transform(Vector3f(0, 1, 0));
                  Vector3f finalForward
             = finalRollPitchYaw.Transform(Vector3f(0, 0, -1));
                  Vector3f shiftedEyePos
             = Pos + rollPitchYaw.Transform(useEyePose->Position);
      Matrix4f view = Matrix4f::LookAtRH(
             shiftedEyePos, shiftedEyePos + finalForward, 
             finalUp);
      Matrix4f proj = ovrMatrix4f_Projection(
             EyeRenderDesc[eye].Fov, 0.2f, 1000.0f, true ); 
                  Vector4f viewDir = Vector4f(finalForward, 1.0);
      acadScene.Render(
             viewDir, 
             view, proj.Transposed());
   }
  }
    // Do distortion rendering, Present and flush/sync 
  ovrD3D11Texture eyeTexture[2]; 
  for  (int  eye = 0; eye<2; eye++)
  {
   eyeTexture[eye].D3D11.Header.API
         = ovrRenderAPI_D3D11;
             eyeTexture[eye].D3D11.Header.TextureSize
         = pEyeRenderTexture[eye]->Size;
             eyeTexture[eye].D3D11.Header.RenderViewport 
         = EyeRenderViewport[eye];
             eyeTexture[eye].D3D11.pTexture
         = pEyeRenderTexture[eye]->Tex;
             eyeTexture[eye].D3D11.pSRView
         = pEyeRenderTexture[eye]->TexSv;
  }
  ovrHmd_EndFrame(
         HMD, 
         EyeRenderPose, 
         &eyeTexture[0].Texture);
 }
   EnableWindow(hWndParent, TRUE);
   // Release and close down 
 ovrHmd_Destroy(HMD);
 ovr_Shutdown();
 gpDX11->ReleaseWindow(hInstance);
   delete gpDX11;
 gpDX11 = NULL;
  If you are already familiar with the "OculusRoomTiny" sample from the Oculus SDK, the following list of changes will make it easier for you to track the changes :
1. Includes code to add custom solid to the scene based on the meshed solids from AutoCAD
2. Included surface Normal input to the vertex and pixel shader to highlight edges. This works well if the solid color has all components such as R, G and B values.
3. Increased the number of solids in the scene to 20 and generalized it to accept variable number of vertices and indices.

