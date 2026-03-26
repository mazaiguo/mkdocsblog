---
title: "Converting AcGePoint3d to variant and vice versa"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
description: "When using C++, I have problems converting an AcGePoint3d type to a VARIANT. Is there sample code that does this?"
author: Autodesk
---
# Converting AcGePoint3d to variant and vice versa

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/converting-acgepoint3d-to-variant-and-vice-versa.html

## 文章内容

By Xiaodong Liang
Issue
When using C++, I have problems converting an AcGePoint3d type to a VARIANT. Is there sample code that does this?
Solution
The following code demonstrates how to convert an AcGePoint3d type to a VARIANT by calling asDblArray() global function from AcGePoint3d to a double array. Notice that the C++ code is generic.
Note that there is minimal error checking code for code brevity.
//convert to point from variant
HRESULT getDblArrayFromVariant(double pt[3],
                               const VARIANT* pVal)
{
    if (!(pVal->vt & VT_ARRAY && pVal->vt & VT_R8))
        return E_INVALIDARG;
      SAFEARRAY* sPt = pVal->parray;
      if (SafeArrayGetDim(sPt) != 1)
        return E_INVALIDARG;
      long lLbound;
    long lUbound;
    SafeArrayGetLBound(sPt, 1, &lLbound);
    SafeArrayGetUBound(sPt, 1, &lUbound);
      if ((lUbound - lLbound + 1) != 3)
        return E_INVALIDARG;
      HRESULT hr;
    for (long i = 0; i < 3; i++)
        if ((hr = SafeArrayGetElement(sPt, &i, &pt[i]))!=S_OK)
            return hr;
      return S_OK;
}
//
//
////convert to variant from point
HRESULT getVariantFromDblArray(VARIANT* pVal,
                               const double pt[3])
{
    pVal->vt = VT_ARRAY | VT_R8;
      SAFEARRAYBOUND rgsaBound;
    rgsaBound.lLbound = 0L;
    rgsaBound.cElements = 3;
      pVal->parray =
        SafeArrayCreate(VT_R8, 1, &rgsaBound);
    if (! pVal->parray)
        return E_OUTOFMEMORY;
      HRESULT hr;
    for (long i = 0; i < 3; i++)
        if ((hr = SafeArrayPutElement(
            pVal->parray, &i,
            (void*)&pt[i]))!=S_OK)
            return hr;
    return S_OK;
}
static void test()
{
    AcGePoint3d pt3d = AcGePoint3d(10,20,30);
      HRESULT hr;
    // AcGePoint3d to Variant
    VARIANT vt;
    hr = getVariantFromDblArray(&vt,asDblArray(pt3d));
      //Variant to AcGePoint3d
    double pt[3];
    hr = getDblArrayFromVariant(pt,&vt);
      AcGePoint3d pt3d_1 =  AcGePoint3d(pt[0],pt[1],pt[2]);
  }

## 评论

**内容**: Alexander Rivlis said...
Hi, Xiaodong!
What about using class AcAxPoint3d in order to converting VARINT <-> AcGePoint3d ?
As far as I know, this class was a creation just for this purpose.
Reply
01/10/2013 at 07:48 AM

---
**内容**: xiaodong said...
Hi Alexander,
yes, AcAxPoint3d is used to facilitate conversion of AcGePoint3d data to and from Automation-compatible types, a kind of class like a wrapper. I would say this blog post is generic, just for developer's reference :-)

Thanks,
Xiaodong
Reply
01/15/2013 at 02:38 AM

---
