---
title: "Dumping the COM Running Object Table (ROT) in ObjectARX"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - COM
  - ObjectARX
  - VBA
description: "How can I inspect the running Automation servers on my computer? I'd like to retrieve Automation objects with GetObject in Visual Basic."
author: Autodesk
---
# Dumping the COM Running Object Table (ROT) in ObjectARX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/dumping-the-com-running-object-table-rot-in-objectarx.html

## 文章内容

by Fenton Webb
Issue
How can I inspect the running Automation servers on my computer? I'd like to retrieve Automation objects with GetObject in Visual Basic.
Solution
The following code is a simple console application that dumps the contents of the Running Object Table. Use the AdskPlainCOMDocSamp in the ObjectARX SDK to test it…
  #include <comdef.h>
#include <objbase.h>
#include <iostream>
  using namespace std;
_COM_SMARTPTR_TYPEDEF(IRunningObjectTable, __uuidof(IRunningObjectTable));
_COM_SMARTPTR_TYPEDEF(IEnumMoniker, __uuidof(IEnumMoniker));
_COM_SMARTPTR_TYPEDEF(IMoniker, __uuidof(IMoniker));
_COM_SMARTPTR_TYPEDEF(IBindCtx, __uuidof(IBindCtx));
    class SimpleException
{
  const WCHAR* m_strDisc;
  HRESULT m_hr;
public:
  SimpleException(const WCHAR* strDisc = NULL,HRESULT hr=S_OK):m_strDisc(strDisc),m_hr(hr) {}
  wostream& reportIt(wostream& out)const {return out << m_strDisc << L" HRESULT=" << m_hr;}
};
    #define RETRIEVE_AT_ONCE 10
void main()
{
  CoInitialize(NULL);
  try
  {
    IRunningObjectTablePtr pROT;
    HRESULT hr;
    if (FAILED(hr = GetRunningObjectTable(0,&pROT)))
      throw SimpleException(L"GetRunningObjectTable",hr);
    IEnumMonikerPtr pEnum;
    if (FAILED(hr = pROT->EnumRunning(&pEnum)))
      throw SimpleException(L"EnumRunning on IRunningObjectTable",hr);
    IMoniker* elems[RETRIEVE_AT_ONCE];
    LPOLESTR  pbstrName;
    unsigned long fetched;
    IBindCtxPtr pBndCtx;
    if (FAILED(hr = CreateBindCtx(0,&pBndCtx)))
      throw SimpleException(L"CreateBindCtx",hr);
    while (true)
    {
      if (FAILED(hr=pEnum->Next( RETRIEVE_AT_ONCE,elems,&fetched)))
        throw SimpleException(L"Next on IEnumMoniker",hr);
      for (unsigned long i=0;i<fetched;i++){
        if (FAILED(hr=elems[i]->GetDisplayName(pBndCtx,NULL,&pbstrName))){
          wcout << L"GetDisplayName failed. hr=" << hr;
          elems[i]->Release();
          continue;
        }
        elems[i]->Release();
        wcout << L"Name = " << pbstrName << endl;
        CoTaskMemFree(pbstrName);
        }
      if (fetched < RETRIEVE_AT_ONCE)
        break;
    }
  }
  catch (const SimpleException& exc){
    wcout << L"Error in function: ";
    exc.reportIt(wcout);
    wcout << endl << L"Aborting." << endl;
  }
  CoUninitialize();
}

