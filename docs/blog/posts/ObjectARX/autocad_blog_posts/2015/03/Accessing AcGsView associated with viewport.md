---
title: "Accessing AcGsView associated with viewport"
date: 2015-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "In releases prior to AutoCAD 2015, the "acgsGetGsView" method provided access to the AcGsView of a viewport. In AutoCAD 2015, this method is not av..."
author: Autodesk
---
# Accessing AcGsView associated with viewport

发布日期: 2015-03-01

原始链接: https://adndevblog.typepad.com/autocad/2015/03/accessing-acgsview-associated-with-viewport.html

## 文章内容

By Balaji Ramamoorthy
In releases prior to AutoCAD 2015, the "acgsGetGsView" method provided access to the AcGsView of a viewport. In AutoCAD 2015, this method is not available and as a replacement, two other methods - "acgsGetCurrentAcGsView" and "acgsGetCurrent3dAcGsView" have been introduced. The sample code in this blog post and the comments are meant to clarify the differences and their usage.
 #include "acgs.h"
    // Prior to AutoCAD 2015 
   // Get the current viewport number 
 struct  resbuf  rb;
 int  rt = acedGetVar(_T("CVPORT" ), &rb);
 if (rt != RTNORM)
 {
  acutPrintf(_T("\\nError !" ));
  return ;
 }
 int  vportNum = rb.resval.rint;
   // Get the GS View associated with the viewport 
 AcGsView *pView1 = acgsGetGsView
                         (vportNum, false );
 // If AutoCAD is in a shaded view,  
 // then pView will be non-null. 
 if (pView1)
 {   //'re in shaded mode OR  
  // a GS view has been already been created  
     // and associated with viewport 
     acutPrintf(ACRX_T("We are in shaded mode..." ));
 }
 else 
 {
     //'re in a 2D wireframe or a GsView has not  
     // been created for this viewport ... 
       // To create a GS View and associate with the  
     // viewport use : 
  // AcGsView *pView2 = acgsGetGsView(vportNum, true); 
     //if(pView2 != NULL) 
     //{ 
     //    acutPrintf(ACRX_T("Created a 3D GS View  
     //            and associated with viewport..")); 
     //} 
    acutPrintf(ACRX_T("We are in 2D wireframe mode..." ));
 }
     // For AutoCAD 2015+ 
   // Get the current viewport number 
 struct  resbuf  rb;
 int  rt = acedGetVar(_T("CVPORT" ), &rb);
 if (rt != RTNORM)
 {
  acutPrintf(_T("\\nError ! " ));
  return ;
 }
 int  vportNum = rb.resval.rint;
   Acad::ErrorStatus es;
   // Returns a GS View regardless of 2D or 3D 
 AcGsView *pGsView1 = acgsGetCurrentAcGsView(vportNum);
 ASSERT(pGsView1 != NULL);
   // Returns a 3D GS view if a view is associated  
 // with the viewport. If not this will return null.  
 // But, a null value does not let us 
 // assume it is 2D Wireframe, as a 3d AcGsView can  
 // be created and associated with the viewport. 
 AcGsView *pGsView2 = acgsGetCurrent3dAcGsView(vportNum);
 if (pGsView2 != NULL)
 {
  //'re in shaded mode OR  
  // a 3D GS view has been created and  
     // associated with viewport 
  acutPrintf(ACRX_T("We are in shaded mode..." ));
 }
 else 
 { 
  //'re in a 2D wireframe and a 3D GS view has  
     // not been created yet... 
  // Lets create a 3D GS View. 
       // After the 3D GS view is created, both  
     // acgsGetCurrentAcGsView and  acgsGetCurrent3dAcGsView  
     // will return the newly created GS View. 
    // To create a GS View and associate it with the  
     // viewport use : 
  /* 
  AcGsKernelDescriptor desc; 
  desc.addRequirement( AcGsKernelDescriptor::k3DDrawing ); 
  AcGsView* pView2 = acgsObtainAcGsView(vportNum, desc); 
  if(pView2 != NULL) 
  { 
   acutPrintf(ACRX_T("Created a 3D GS View  
                 and associated with viewport..")); 
  } 
  */ 
    acutPrintf(ACRX_T("We are in a 2D wireframe mode..." ));
 }

