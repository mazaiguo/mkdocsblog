---
title: "Automatically opening a drawing and closing default drawing"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - Block
  - C++
  - COM
  - DWG
description: "When AutoCAD is first loaded, it creates a default empty drawing. When I use AutoCAD's tools to open another drawing, such as File - Open, Drawing1..."
author: Autodesk
---
# Automatically opening a drawing and closing default drawing

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/automatically-opening-a-drawing-and-closing-default-drawing.html

## 文章内容

By Xiaodong Liang
Issue
When AutoCAD is first loaded, it creates a default empty drawing. When I use AutoCAD's tools to open another drawing, such as File - Open, Drawing1 automatically disappears. When I do the same thing programmatically, such as using AcApDocManager::appContextOpenDocument() and register its caller function in session context, Drawing1.dwg does not close. Why?
Solution
If you use AcApDocManager::closeDocument() in the same function block as AcApDocManager::appContextOpenDocument(), closeDocument() always fails because AutoCAD "thinks" that something is still active on the command line. As a result, it will not close the document even appContextOpenDocument() has done
its job successfully.
The answer is to use the Acad ActiveX Automation interfaces in your ARX application. The following code closes the default drawing and opens a drawing you request in MDI mode.
//
// make sure you register the linked command with ACRX_CMD_SESSION bit
//
// minimal error check for code brevity
//
void openDwg()
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
      BSTR fName;
    hr = pDoc->get_Name(&fName);
      _bstr_t dwg1("Drawing1.dwg");
    _bstr_t dwg2(fName);
    if(SUCCEEDED(hr) && dwg1 == dwg2)
    {
        _variant_t vb(VARIANT_FALSE);
        _variant_t vnam(dwg1);
        hr = pDoc->Close(vb, vnam);
        if(FAILED(hr))
        {
            acutPrintf(L"\nFailed to close drawing1.dwg.");
            return;
        }
    }
      _bstr_t fileName("c:\\test.dwg");
      CComPtr<IAcadDocuments> pDocs;
    hr = pComApp->get_Documents(&pDocs);
    if(FAILED(hr))
        return;
      _variant_t b(VARIANT_FALSE);
    _variant_t password("");
    CComPtr<IAcadDocument> pDoc1;
    hr = pDocs->Open(fileName, b,password, &pDoc1);
    if(FAILED(hr))
        acutPrintf(L"\nFailed to open the dwg file.");
}
Note that in SDI mode, the code is changed as follows:
//
// minimal error check for code brevity
//
void openDwg_SDI()
{
    CWinApp* pWinApp = acedGetAcadWinApp();
    if(!pWinApp)
      return;
    CComPtr<IDispatch> pDisp = pWinApp->GetIDispatch(TRUE);
    if(!pDisp)
      return;
      CComPtr<IAcadApplication> pComApp;
    HRESULT hr = pDisp->QueryInterface(IID_IAcadApplication, (void**)&pComApp);
    if(FAILED(hr))
      return;
      CComPtr<IAcadDocument> pDoc;
    hr = pComApp->get_ActiveDocument(&pDoc);
    if(FAILED(hr))
      return;
      _bstr_t fileName("c:\\test.dwg");
    _variant_t password("");
    hr = pDoc->Open(fileName,password, &pDoc);
    if(FAILED(hr))
      acutPrintf(L"\nFailed to open the dwg file.");

## 评论

**内容**: jignesh said...
hi,
after closing the document my autocadframe not updating means if i close the document Drawing1.dwg when open another drawing at that time autocad window not updated or refreshed because my another command call after it so what i have to do ? if i return to autocad command without calling the command then it's work properly..
Reply
11/16/2016 at 10:24 PM

---
