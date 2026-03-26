---
title: "Load DVB and run VBA macro using AutoCAD COM API in ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - COM
  - ObjectARX
description: "How can I load a .dvb and run the macro using AutoCAD COM interface?"
author: Autodesk
---
# Load DVB and run VBA macro using AutoCAD COM API in ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/load-dvb-and-run-vba-macro-using-autocad-com-api-in-objectarx.html

## 文章内容

By Fenton Webb
Issue
How can I load a .dvb and run the macro using AutoCAD COM interface?
Solution
#import "acax19ENU.tlb" no_implementation raw_interfaces_only
  #include <comdef.h>
#include <atlbase.h>
#include <acadi_i.c>
using namespace AutoCAD;
  LoadVBARunMacro()
{
  // setup the VBA macro DVB details
  CComBSTR bsrtVBAName = _T("d:\\temp\\Project.dvb");
  // setup the macro name :pass your macro name here
  CComBSTR bstrMacro = _T("test");
  // get acad's iDispatch
  IAcadApplicationPtr pAcad = acedGetIDispatch(FALSE);
  // now load the DVB
  HRESULT hr = pAcad->LoadDVB(bsrtVBAName.m_str);
  // if ok
  if (SUCCEEDED(hr))
  {
    // run the macro
    hr = pAcad->RunMacro(bstrMacro.m_str);
    // unload the DVB if you want
    hr = pAcad->UnloadDVB(bsrtVBAName.m_str);
  }
}

## 评论

**内容**: Suom Sarou said...
I don't know how to load file dvb in autocad
Reply
01/20/2014 at 01:33 AM

---
**内容**: Alexander Rivilis said in reply to Suom Sarou...
Are you talking about manual loading? Command VBALOAD can help you: http://docs.autodesk.com/ACD/2013/ENU/files/GUID-CA16C415-2CC0-4707-8018-23A464F019AD.htm
Reply
01/20/2014 at 04:39 PM

---
