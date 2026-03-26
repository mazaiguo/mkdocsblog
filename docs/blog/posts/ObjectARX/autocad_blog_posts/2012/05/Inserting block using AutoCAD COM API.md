---
title: "Inserting block using AutoCAD COM API"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - Block
  - COM
description: "Here is a sample ObjectARX code to demonstrate the usage of InsertBlock method of the AutoCAD COM API."
author: Autodesk
---
# Inserting block using AutoCAD COM API

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/inserting-block-using-autocad-com-api.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample ObjectARX code to demonstrate the usage of InsertBlock method of the AutoCAD COM API.
#pragma warning( disable : 4278 )
// Makes change to the tlb name based on the AutoCAD version.
// For ex : acax18enu.tlb for AutoCAD 2010/2011 and 2012
//          acax19enu.tlb for AutoCAD 2013 
#import "acax19ENU.tlb" no_implementation raw_interfaces_only named_guids
#pragma warning( default : 4278 )
  #include <acadi.h>
static void ADSProjectInsertBlock(void)
{
    int ret = RTNORM;
      TCHAR drawingFilePath[500];
    drawingFilePath[0] = _T('\0');
    ret = acedGetString (
                            NULL,
                            _T("Enter file path : "),
                            drawingFilePath
                        );
    if(ret != RTNORM)
        return;
      ads_point insertionPoint;
    ret = acedGetPoint(
                        NULL,
                        _T("\nEnter insertion point: "),
                        insertionPoint
                       );
    if(ret != RTNORM)
        return;
      CWinApp *pApp = acedGetAcadWinApp();
    HRESULT hRes;
    LPDISPATCH pDisp=NULL;
      if(!pApp)
        return;
      pDisp=pApp->GetIDispatch(TRUE);
    if    (!pDisp)
          return;
      CComPtr<AutoCAD::IAcadApplication>  pComApp;
    hRes=pDisp->QueryInterface(
                                IID_IAcadApplication,
                                (void**)&pComApp
                              );
    if (FAILED(hRes))
          return;
      CComPtr<AutoCAD::IAcadDocument> pComDoc;
    hRes=pComApp->get_ActiveDocument(&pComDoc);
    if(FAILED(hRes))
        return;
      CComPtr<AutoCAD::IAcadModelSpace> pMSpace = NULL;
    pComDoc->get_ModelSpace(&pMSpace);
      _bstr_t block(drawingFilePath);
    CComPtr<AutoCAD::IAcadBlockReference> pBlkRef = NULL;
      SAFEARRAYBOUND rgsaBound;
    rgsaBound.lLbound = 0L;
    rgsaBound.cElements = 3;
    SAFEARRAY* pInsertionPoint = NULL;
    pInsertionPoint = SafeArrayCreate(VT_R8, 1, &rgsaBound);
      for(long i = 0; i < 3; i++)
    {
        double value = insertionPoint[i];
        SafeArrayPutElement(
                                pInsertionPoint,
                                &i,
                                &value
                            );
    }
      VARIANT vInsertionPoint;
    VariantInit(&vInsertionPoint);
    V_VT(&vInsertionPoint) = VT_ARRAY | VT_R8;
    V_ARRAY(&vInsertionPoint) = pInsertionPoint;
      double scaleX = 1.0;
    double scaleY = 1.0;
    double scaleZ = 1.0;
    double rotation = 0.0;
      pMSpace->InsertBlock(
                            vInsertionPoint,
                            block,
                            scaleX,
                            scaleY,
                            scaleZ,
                            rotation,
                            vtMissing,
                            &pBlkRef
                        );
      VariantClear(&vInsertionPoint);
}

## 评论

**内容**: petcon said...
i think there is a way not using com,show me
Reply
05/16/2012 at 09:51 PM

---
