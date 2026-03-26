---
title: "Load a .NET managed assembly from an ObjectARX application"
date: 2012-10-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - C++
  - ObjectARX
description: "How do I load a .NET managed assembly from an ObjectARX application?"
author: Autodesk
---
# Load a .NET managed assembly from an ObjectARX application

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/load-a-net-managed-assembly-from-an-objectarx-application.html

## 文章内容

By Philippe Leefsma
Q:
How do I load a .NET managed assembly from an ObjectARX application?
A:
To load a managed assembly from an arx application, you can use LoadManagedDll API exported from acdbmgd.dll.

The signature is Acad::ErrorStatus LoadManagedDll(const char* fname)
You must use GetProcAddress since we do not provide the import library for acmgd.dll:
typedef Acad::ErrorStatus (__stdcall* funcPtr)(const TCHAR* fname);
   static void TestMyNetLoad(void)
 {
  ACHAR fileName[MAX_PATH];
    if( RTNORM != acedGetString(true, _T("\nDLL full name: "), fileName) )
  {
   acutPrintf(_T("\nSomething wrong with the file name input!"));
   return;
  }
    HMODULE hAcMgd = ::GetModuleHandle(_T("ACDBMGD.DLL"));
    funcPtr pLoadMgd = (funcPtr)::GetProcAddress(hAcMgd, "LoadManagedDll");
    if( pLoadMgd )
  {
   Acad::ErrorStatus es = (*pLoadMgd)(fileName);
   if( es != Acad::eOk )
   {
    acutPrintf(_T("\nError in loading the .NET DLL!"));
    return;
   }
  }
  else
  {
   acutPrintf(_T("\nError getting function pointer to LoadManagedDll()!"));
   return;
  }
 }

## 评论

**内容**: Alexander Rivilis said...
Hi, Philippe!
As I remember acdbmgd.lib export function LoadMangedDll. That is why code may be simpler: http://forums.autodesk.com/t5/Autodesk-ObjectARX/netload-in-arx/m-p/2191113#M24126
Reply
10/02/2012 at 01:35 PM

---
