---
title: "Programmatically saving the active document in C++/ARX applications"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - COM
  - DWG
  - ObjectARX
description: "Use the Automation interfaces inside your ARX application. The following code samples demonstrate two approaches to consider (Make sure your ARX pr..."
author: Autodesk
---
# Programmatically saving the active document in C++/ARX applications

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/programmatically-saving-the-active-document-in-carx-applications.html

## 文章内容

By Gopinath Taget
Use the Automation interfaces inside your ARX application. The following code samples demonstrate two approaches to consider (Make sure your ARX projects supports the AutoCAD ActiveX client interfaces. The ARX wizard makes this easy to do):
First Approach:
void saveDwg()
{
 try
{
IAcadApplicationPtr pApp =
acedGetAcadWinApp()->GetIDispatch(FALSE);
IAcadDocumentPtr pDoc;
pApp->get_ActiveDocument(&pDoc);
pDoc->Save();
}
 catch(_com_error& e)
{
acutPrintf(_T("\nCOM error: %s"), (ACHAR*)e.Description());
}
}
Second Approach:
#include <acadi_i.c>
// minimal error check for code brevity
void saveDwg()
{
CWinApp* pWinApp = acedGetAcadWinApp();
 if(!pWinApp)
  return;
CComPtr<IDispatch> pDisp = pWinApp->GetIDispatch(TRUE);
 if(!pDisp)
  return;
  CComPtr<IAcadApplication> pComApp;
HRESULT hr = pDisp->QueryInterface(IID_IAcadApplication,
  (void**)&pComApp);
 if(FAILED(hr))
  return;
  CComPtr<IAcadDocument> pDoc;
hr = pComApp->get_ActiveDocument(&pDoc);
 if(FAILED(hr))
  return;
  hr = pDoc->Save();
 if(FAILED(hr))
  acutPrintf(_T("\nFailed to save current dwg file."));
}

