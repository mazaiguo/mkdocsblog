---
title: "Setting default plot to file path"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Plot
description: "The Default Plot to File Path can be set in AutoCAD using the Options Dialog. To do this programmaticaly using ARX, you can use the automation func..."
author: Autodesk
---
# Setting default plot to file path

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/setting-default-plot-to-file-path.html

## 文章内容

By Balaji Ramamoorthy
The Default Plot to File Path can be set in AutoCAD using the Options Dialog. To do this programmaticaly using ARX, you can use the automation function IAcadPreferencesOutput::put_DefaultPlotToFilePath().
Please find below some code which shows you how to do this programmatically.
#pragma warning( disable : 4278 )
// Makes change to the tlb name based on the AutoCAD version.
// For ex : acax18enu.tlb for AutoCAD 2010/2011 and 2012
//          acad19enu.tlb for AutoCAD 2013 
#import "acax19ENU.tlb" no_implementation raw_interfaces_only named_guids
#pragma warning( default : 4278 )
  #include <acadi.h>
static void AdskMyCommand(void)
{
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
      CComPtr<AutoCAD::IAcadPreferences>  pComPref;
    hRes=pComApp->get_Preferences(&pComPref);
    if(FAILED(hRes))
        return;
      CComPtr<AutoCAD::IAcadPreferencesOutput>  pComOutputPref;
    hRes=pComPref->get_Output(&pComOutputPref);
    if(FAILED(hRes))
        return;
      BSTR bstDefaultFilePath;
    hRes=pComOutputPref->get_DefaultPlotToFilePath(&bstDefaultFilePath);
    if(FAILED(hRes))
        return;
      CString cstrVal = "C:\\Temp";
    BSTR bstNewDefaultFilePath = cstrVal.AllocSysString();
      hRes=pComOutputPref->put_DefaultPlotToFilePath(bstNewDefaultFilePath);
    if(SUCCEEDED(hRes))
    {
        acutPrintf
        (
            ACRX_T("DefaultPlotToFilePath has been changed from %s to %s."),
            bstDefaultFilePath,
            bstNewDefaultFilePath
        );
    }
}

