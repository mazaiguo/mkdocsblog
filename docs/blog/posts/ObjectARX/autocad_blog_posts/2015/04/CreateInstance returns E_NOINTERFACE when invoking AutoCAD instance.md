---
title: "CreateInstance returns E_NOINTERFACE when invoking AutoCAD instance"
date: 2015-04-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "When trying to launch an AutoCAD instance from an external application using CreateInstance, you may get ENOINTERFACE. In this blog post we will lo..."
author: Autodesk
---
# CreateInstance returns E_NOINTERFACE when invoking AutoCAD instance

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/createinstance-returns-e_nointerface-when-invoking-autocad-instance.html

## 文章内容

By Balaji Ramamoorthy
When trying to launch an AutoCAD instance from an external application using CreateInstance, you may get E_NOINTERFACE. In this blog post we will look at some possible reasons and ways to resolve it.
Please note that it is required to build separate 32 and 64 bit versions of your external exe that imports the right version of acax20ENU.tlb. There are GUIDs that are different in 32 and 64 bit versions of the acax20ENU.tlb and so cannot be used interchangeably.
Also, when you build the exe, try providing the absolute path to #import. This will ensure that the right version of the typelibrary gets imported in your project.
For example, use this when building the 32 bit version of your exe :
#import "D:\ObjectARX 2016\inc-win32\acax20ENU.tlb" no_implementation raw_interfaces_only named_guids
and this when building the 64 bit version of your exe :
#import "D:\ObjectARX 2016\inc-x64\acax20ENU.tlb" no_implementation raw_interfaces_only named_guids
If the absolute path is not specified, it can happen that the typelibrary is being picked up from a common location such as "C:\Program Files\Common Files\Autodesk Shared" and which on a 64 bit system is a 64 bit version of the typelibrary. This can cause issue on a 32 bit system and result in E_NOINTERFACE.
Also, from a general COM perspective, the calling thread is required to be a STA. You can have this set using ::CoInitializeEx. Including the following line should help with that :
::CoInitializeEx(NULL, COINIT_APARTMENTTHREADED);
Another reason for E_NOINTERFACE could be a mismatch between the typelibrary being imported and the CLSID used with CreateInstance. For example, if you are importing acax20ENU.tlb, the CLSID must be "AutoCAD.Application.20" which corresponds to AutoCAD 2016.
Here is a sample code to invoke an AutoCAD 2016 instance :
 #include  <acadi.h> 
   #pragma  warning ( disable  : 4278 )
 // Makes change to the tlb name  
 // based on the AutoCAD version.  
 #import  "D:\\ObjectARX 2016\\inc-x64\\acax20ENU.tlb"  \\
  no_implementation raw_interfaces_only named_guids
 using  namespace  AutoCAD; 
 #pragma  warning ( default  : 4278 )
   ::CoInitializeEx(NULL, COINIT_APARTMENTTHREADED);
   CLSID clsidAcad;
 HRESULT hr;
 hr = ::CLSIDFromProgID(
  L"AutoCAD.Application.20" , 
  &clsidAcad);
 if (FAILED(hr))
 {
  ::MessageBox(
  m_hWnd,
  _com_error(hr).ErrorMessage(),
  L"CLSIDFromProgID Error !" ,
  MB_OK);
  return ;
 }
   OLECHAR* bstrGuid; 
 ::StringFromCLSID(clsidAcad, &bstrGuid); 
    ::MessageBox(
   m_hWnd,
   bstrGuid,
   L"Got CLSID from ProgID !" ,
   MB_OK);
     LPUNKNOWN punkAcad = NULL;
 HRESULT hr = S_OK;
     IAcadApplicationPtr m_acPtr;
 hr = m_acPtr.GetActiveObject(clsidAcad);
 if (SUCCEEDED(hr))
 {
  ::MessageBox(
  m_hWnd,
  L"Success_GetActiveObject" ,
  L"Ok!" ,
  MB_OK);
    m_acPtr->put_Visible(VARIANT_TRUE);
 }
 else 
 {
  ::MessageBox(
  m_hWnd,
  L"GetActiveObject failed,  
  Will try  CreateInstance !", 
  L"GetActiveObject" ,
  MB_OK);
    hr = m_acPtr.CreateInstance(
   clsidAcad, NULL, CLSCTX_LOCAL_SERVER);
    if (SUCCEEDED(hr))
  {
   ::MessageBox(
   m_hWnd,
   L"Success_CreateInstance" ,
   L"Ok!" ,
   MB_OK);
     m_acPtr->put_Visible(VARIANT_TRUE);
  }
  else 
  {
   ::MessageBox(
   m_hWnd,
   _com_error(hr).ErrorMessage(),
   L"CreateInstance Error !" ,
   MB_OK);
   return ;
  }
 }
   if (punkAcad) 
  punkAcad->Release();

