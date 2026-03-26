---
title: "Migration Tip : ACAD2011\12 to 13\14\15"
date: 2014-12-01
categories:
  - AutoCAD
tags:
  - API
  - Migration
description: "This tip is not purely on ACAD per se ,but from Visual Studio perspective and will be helpful for guys who are using VS template CMap where on its ..."
author: Autodesk
---
# Migration Tip : ACAD2011\12 to 13\14\15

发布日期: 2014-12-01

原始链接: https://adndevblog.typepad.com/autocad/2014/12/migration-tip-acad201112-to-131415.html

## 文章内容

By Madhukar Moogala
This tip is not purely on ACAD per se ,but from Visual Studio perspective and will be helpful for guys who are using VS template CMap where on its key is AcDbHandle&
CMap<AcDbHandle, AcDbHandle&, CString, CString> handleMap;
I recently received a case query where customer is getting this compilation error C2440: 'type cast' : cannot convert from 'AcDbHandle' to 'long' ,which is working fine VS 90.0 compiler but failing in VS 100.0\110.0 , after investigating it is found that the  default implementation of
template<class ARG_KEY>
AFX_INLINE UINT AFXAPI HashKey(ARG_KEY key)
is changed in one of the atlmfc includes Afxtempl.h, the new definition is not allowing the type conversion, so we have two options either to understand new definition  ,which I didn’t get completely so expecting some expert opinion or to override HashKey template to suit to our need.
Here I’m going with the second option ,to override HashKey template.
You can incorporate the following definition in your DLLMain file to avoid type conversion error.
template<>
AFX_INLINE UINT AFXAPI HashKey<AcDbHandle&>(AcDbHandle& key)
{
  // default identity hash - works for most primitive values
return (DWORD)(((DWORD_PTR)key)>>4);
  }
You are welcome for comments and insights , I’m no expert on this ,I’m learning with you

