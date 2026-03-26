---
title: "Retrieving property values from entity's COM wrapper"
date: 2014-12-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - COM
  - DWG
description: "When implementing an AutoCAD plugin, its quite easy to retrieve entity properties without having to directly deal with the entity's COM wrapper. Bu..."
author: Autodesk
---
# Retrieving property values from entity's COM wrapper

发布日期: 2014-12-01

原始链接: https://adndevblog.typepad.com/autocad/2014/12/retrieving-property-values-from-entitys-com-wrapper-.html

## 文章内容

By Balaji Ramamoorthy
When implementing an AutoCAD plugin, its quite easy to retrieve entity properties without having to directly deal with the entity's COM wrapper. But when implementing a RealDWG host application, this can become necessary to retrieve some of the entity properties. 
If you are using .Net languages, using reflection can come very handy. Here is a blog post that can help :
Get ActiveX/COM class properties and methods from .NET
If you are using C++, here are the changes to the DumpDwg sample from the RealDWG SDK. In this code snippet, our objective is to retrieve properties of a custom entity using the IDispatch interface of its COM wrapper. For example, a drawing that includes a "AsdkPoly" entity from "ObjectARX 2015\samples\entity\polysampPolySamp".
 // Info on each IDispatch member item 
 struct  stringdispid
 {
     CComBSTR bstr;
     int  nLen;
     DISPID id;
 };
   // DispId map to retrieve properties 
 static  stringdispid* m_pMap;
 static  int  m_nMapLen;
 static  int  m_nCount;
   // Helper method to convert VARIANT to ads_point 
 static  HRESULT get_PointFromVariant(
  VARIANT &variant, 
  ads_point &pt)
 {
  if  (V_VT(&variant) != VT_EMPTY) 
  {
   if  (V_VT(&variant) == (VT_ARRAY | VT_R8))
   {
    SAFEARRAY *psa = variant.parray;
    long  lStartIndex = 0;
    long  lEndIndex = 0;
    SafeArrayGetLBound(psa, 1, &lStartIndex);
    SafeArrayGetUBound(psa, 1, &lEndIndex);
      if (lEndIndex == 2)
    {
     AcAxPoint3d tmpPt(variant);
     pt[X] = tmpPt[X];
     pt[Y] = tmpPt[Y];
     pt[Z] = tmpPt[Z];
    }
      if (lEndIndex == 1)
    {
     AcAxPoint2d tmpPt(variant);
     pt[X] = tmpPt[X];
     pt[Y] = tmpPt[Y];
     pt[Z] = 0.0;
    }
       return  S_OK;
   }
  } 
  return  E_INVALIDARG;  
 }
   // Helper method to get the COM wrapper for an entity 
 static  IAcadBaseObject* get_com_wrapper
       (AcDbEntity* entity) 
 { 
  AcAxOleLinkManager* manager = AcAxGetOleLinkManager();
  if  (!manager) 
   return  NULL; 
    IUnknown* unknown = manager->GetIUnknown(entity); 
  if  (!unknown) 
  { 
   CLSID class_id; 
   if  (Acad::eOk != entity->getClassID(&class_id)) 
    return  NULL; 
     HRESULT res = CoCreateInstance(
    class_id, 
    NULL, 
    CLSCTX_ALL, 
    IID_IUnknown, 
    (LPVOID*) &unknown);
     if  (FAILED(res)) 
    return  NULL; 
     IAcadBaseObject* base = NULL; 
   res = unknown->QueryInterface(
    __uuidof (IAcadBaseObject), 
    (VOID**) &base);
     if  (FAILED(res)) 
    return  NULL; 
     if  (!manager->SetIUnknown(entity, unknown)) 
    return  FALSE; 
        base->SetObjectId(entity->objectId()); 
   base->Release(); 
  } 
    // Caller will release this interface  
  IAcadBaseObject* wrapper = NULL; 
  HRESULT res = unknown->QueryInterface(
   __uuidof (IAcadBaseObject), 
   (VOID**) &wrapper);
    if  (FAILED(res)) 
   return  NULL; 
    return  wrapper; 
 } 
   // Helper method to retrieve the function desc  
 // from the typeinfo and store it in a map  
 static  HRESULT LoadNameCache(ITypeInfo* pTypeInfo)
 {
     TYPEATTR* pta;
     HRESULT hr = pTypeInfo->GetTypeAttr(&pta);
     if  (SUCCEEDED(hr))
     {
   m_nCount = 0;
   m_nMapLen = pta->cFuncs;
   m_pMap = NULL;
     if (m_nMapLen > 0)
    m_pMap =  new  stringdispid[m_nMapLen];
           for  (int  i=0; i<m_nMapLen; i++)
         {
             FUNCDESC* pfd;
             if  (SUCCEEDED(pTypeInfo->GetFuncDesc(i, &pfd)))
             {
                 CComBSTR bstrName;
                 if  (SUCCEEDED(pTypeInfo->GetDocumentation(
            pfd->memid, 
            &bstrName, 
            NULL, 
            NULL, 
            NULL)))
                 {
      if (pfd->invkind == DISPATCH_PROPERTYGET)
      {
       m_pMap[m_nCount].bstr.
        Attach(bstrName.Detach());
       m_pMap[m_nCount].nLen 
        = SysStringLen(m_pMap[i].bstr);
       m_pMap[m_nCount].id = pfd->memid;
       m_nCount++;
      }
                 }
                 pTypeInfo->ReleaseFuncDesc(pfd);
             }
         }
         pTypeInfo->ReleaseTypeAttr(pta);
     }
     return  S_OK;
 }
   // Retreive properties from an entity using the  
 // IDispatch interface of its COM wrapper 
 HRESULT dumPolyProps(AcDbEntity *pEntity) 
 {
     ::CoInitialize(NULL);
    IAcadBaseObject *pAcadObj = get_com_wrapper(pEntity);
    CComQIPtr<ITypeLib> pTypeLib(pAcadObj); 
  CComQIPtr<ITypeInfo> pTypeInfo(pAcadObj); 
    TCHAR full_app_file_name[512] = L"" ; 
  int  nBufferLength = 512;
  TCHAR* filePart;
     DWORD result;
     result = SearchPath(NULL, _T("asdkcompoly.dbx" ), 
   _T(".dbx" ), 512, full_app_file_name, &filePart);
     if  (result && result < (DWORD)nBufferLength)
  {
   HRESULT hr = LoadTypeLib
    (full_app_file_name, &pTypeLib);
     if  (FAILED(hr)) 
    return  hr;
     UINT iCount = pTypeLib->GetTypeInfoCount(); 
   for  (UINT i=0; i < iCount ; i++) 
   {
    hr = pTypeLib->GetTypeInfo(i, &pTypeInfo);
    if  (FAILED(hr))
     return  hr;
      LoadNameCache(pTypeInfo);
      CComQIPtr<IDispatch> pDisp(pAcadObj);
      // Retrieve the properties 
    for (int  index = 0; index < m_nCount; index++)
    {
     OLECHAR *sMember = m_pMap[index].bstr;
     DISPID dispId;
       hr = pDisp->GetIDsOfNames(
      IID_NULL, 
      &sMember, 
      1, 
      LOCALE_SYSTEM_DEFAULT, 
      &dispId);
       if (SUCCEEDED(hr))
     {
      unsigned  int  puArgErr = 0;
        VARIANT VarResult;
      VariantInit(&VarResult); 
        EXCEPINFO pExcepInfo;
              DISPPARAMS pParams;
      memset(&pParams, 0, sizeof (DISPPARAMS)); 
      pParams.cArgs = 0; 
        hr = pDisp->Invoke(
       dispId, 
       IID_NULL, 
       LOCALE_USER_DEFAULT, 
       DISPATCH_PROPERTYGET, 
       &pParams, 
       &VarResult, 
       &pExcepInfo, 
       NULL);
        if (V_VT(&VarResult) 
       == (VT_ARRAY | VT_R8))
      {
       // Convert to ads_point 
       ads_point pt;
         get_PointFromVariant(VarResult, pt);
         _print(_T("%s : %lf %lf %lf\\n" ), 
        sMember, pt[0], pt[1], pt[2]);
      }
      else  if (VarResult.vt == VT_DISPATCH)
      {
       _print(_T("%s : VT_DISPATCH\\n" ), 
        sMember);
       //IDispatchPtr pDispatch  
       //   = VarResult.pdispVal; 
      }
      else 
      {
       hr = VariantChangeType(
            &VarResult, 
            &VarResult, 
            0, 
            VT_BSTR);
       _print(_T("%s : %s\\n" ), 
        sMember, 
        VarResult.bstrVal);
      }
      VariantClear(&VarResult);  
     }
    }
      delete [] m_pMap;
    m_pMap = NULL;
   }
  }
    CoUninitialize();
    return  S_OK;
 }
   // Invoke it from the dumpEntity method 
 void  dumpEntity(AcDbEntity *pEnt)
 {
  if  (_tcscmp(p, _T("AsdkPoly" )) == 0)
   dumPolyProps(pEnt);
    // ... Rest of the code  
 }
  Here is a screenshot of the retrieved property values (Click on it to enlarge) :

