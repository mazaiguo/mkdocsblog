---
title: "How to convert AcGeMatrix3d to VARIANT"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Dimension
description: "AcAxMatrix3d converts VARIANT to AcGeMatrix3d but not vice-versa. How can I do the reverse conversion?"
author: Autodesk
---
# How to convert AcGeMatrix3d to VARIANT

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-convert-acgematrix3d-to-variant.html

## 文章内容

By Gopinath Taget
AcAxMatrix3d converts VARIANT to AcGeMatrix3d but not vice-versa. How can I do the reverse conversion?
The code below does the conversion from AcGeMatrix3d to VARIANT:
HRESULT GetVariantFromMatrix(VARIANT* pVal, AcGeMatrix3d mat)
{
 // Declare our Variant to be an array of doubles.
pVal->vt = VT_ARRAY | VT_R8;
  SAFEARRAYBOUND rgsaBound[2];// 2 dimensional array...
rgsaBound[0].lLbound = 0L;// First dimension size is 4
rgsaBound[0].cElements = 4;
rgsaBound[1].lLbound = 0L;// Second dimension size is 4
rgsaBound[1].cElements = 4;
  pVal->parray = SafeArrayCreate(VT_R8, 2, &rgsaBound[0]);// Create the VARIANT
 if (! pVal->parray)
  return E_OUTOFMEMORY;
   // Now populate it.
HRESULT hr;
 long i[2];
 for (i[0]=0;i[0]<4;i[0]++)
  for(i[1]=0;i[1]<4;i[1]++)
   if (hr = SafeArrayPutElement(pVal->parray, &i[0],
    (void*)&mat.operator()(i[0],i[1])) != S_OK)
    return hr;
   return S_OK;
}

