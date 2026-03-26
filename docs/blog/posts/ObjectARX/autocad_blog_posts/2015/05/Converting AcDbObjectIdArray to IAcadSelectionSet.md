---
title: "Converting AcDbObjectIdArray to IAcadSelectionSet"
date: 2015-05-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
  - COM
  - Selection
description: "Recently I have received a request from an ADN partner how to pass set of Object Ids to Export COM API, the problem here is working on cross techno..."
author: Autodesk
---
# Converting AcDbObjectIdArray to IAcadSelectionSet

发布日期: 2015-05-01

原始链接: https://adndevblog.typepad.com/autocad/2015/05/converting-acdbobjectidarray-to-iacadselectionset.html

## 文章内容

By Madhukar Moogala
Recently I have received a request from an ADN partner how to pass set of Object Ids to Export COM API, the problem here is working on cross technologies i.e. passing data from C++ to COM
The signature of Export  API in COM is :
Export (        /*[in]*/ BSTR FileName,        /*[in]*/ BSTR Extension,        /*[in]*/ struct IAcadSelectionSet * SelectionSet ) = 0;
It takes a filename, extension and IAcadSelectionSet, now all we have is set of ids.
For better understanding we will pursue an example, the objective of problem is to “Export set of selected objects to BMP format”
  To tackle such requirement our workflow would be:
- From list retrieve ObjectIds, get associated IAcadEntity using Global function AcAxGetIUnknownOfObject.
- Append IAcadEntity to AcadSelectionSet.AddItems
- Use the selectionset in Export API
Sample Code:
void TestExport()
{
    ads_name ss;
    AcDbObjectIdArray* pIdArray = new AcDbObjectIdArray();
    // get the selectionset
    int res = acedSSGet (NULL, NULL, NULL, NULL, ss);
    if (res == RTNORM)
    {
        //get the length of the selection set
        long length = 0l;
        acedSSLength (ss, &length);
 //now loop round
        for (long i=0l; i<length; ++i)
        {
            ads_name ename;
            // extract the ename
            if (acedSSName (ss, i, ename) != RTNORM)
                continue;
            AcDbObjectId objId;
            // convert the ename to an object id
            acdbGetObjectId (objId, ename);
            pIdArray->append(objId);
        }
    }
    /*Export the collection of Objects to BMP format*/
    ExportToFile(pIdArray);
    //free the selection set after use
    acedSSFree (ss);
    delete pIdArray;
}
Utility Functions:
    /*Puts AcadEntity to given selectionset*/
HRESULT addToSelSet(AutoCAD::IAcadSelectionSet* pSelSet, AutoCAD::IAcadEntity* pEntity)
{
HRESULT hr;
  SAFEARRAYBOUND rgsabound[1];
rgsabound[0].lLbound = 0;
rgsabound[0].cElements = 1;
SAFEARRAY* psa = SafeArrayCreateVector(VT_DISPATCH, rgsabound->lLbound, rgsabound->cElements);
if( ! psa )
return E_OUTOFMEMORY;
long i = 0;
LPDISPATCH pDisp = pEntity;
pEntity->Release();
  /*
This function assigns a single element to the array.
*/
/*NOTE: Void pointer<pDisp> to the data to assign to the array.
The variant types VT_DISPATCH, VT_UNKNOWN, and VT_BSTR are pointers, and do not require another level of indirection.*/
hr = SafeArrayPutElement(psa, &i,pDisp);
if( FAILED(hr) )
{
SafeArrayDestroy(psa);
return hr;
}
VARIANT v;
  VariantInit(&v);
v.vt = VT_DISPATCH|VT_ARRAY;
v.parray = psa;
  return pSelSet->AddItems(v);
}
  /*Get me a Selection set or create one if not present*/
AutoCAD::IAcadSelectionSet *GiveMeSelectionSet(AutoCAD::IAcadSelectionSets *pSelSets, BSTR Name)
{
try {
AutoCAD::IAcadSelectionSet *pSet = NULL;
if (pSelSets->Add(Name,&pSet) == S_OK) {
return pSet;
} else if (pSelSets->Item(_variant_t(Name),&pSet) == S_OK) {
return pSet;
} else return NULL;
} catch(...) {
return NULL;
}
return NULL;
}
    void ExportToFile(AcDbObjectIdArray*&  pIdArray)
{
HRESULT hr;
try
{
  AutoCAD::IAcadApplication *pAcad =NULL;
AutoCAD::IAcadDocument *pDoc =NULL;
AutoCAD::IAcadModelSpace *pMSpace = NULL;
AutoCAD::IAcadSelectionSets *pSelSets = NULL;
AutoCAD::IAcadSelectionSet *pSet= NULL;
  hr = NOERROR;
LPUNKNOWN pUnk = NULL;
LPDISPATCH pAcadDisp = acedGetIDispatch(TRUE);
if(pAcadDisp==NULL)
return ;
  hr = pAcadDisp->QueryInterface(AutoCAD::IID_IAcadApplication,(void**)&pAcad);
pAcadDisp->Release();
if (FAILED(hr))
return;
  if (pAcad)
{
  if (pAcad->get_ActiveDocument(&pDoc) == S_OK)
{
  if (pDoc->get_SelectionSets(&pSelSets) == S_OK) {
/*Gets or Creates a set*/
if ((pSet = GiveMeSelectionSet(pSelSets,_bstr_t("TestSet"))) != NULL)
{
    pSet->Clear();
    for (int i = 0; i < pIdArray->length(); i++)
    {
        AcDbObjectId id = pIdArray->at(i);
        //get the COM wrapper associated with the entity
        if(FAILED(hr =AcAxGetIUnknownOfObject(&pUnk, id, pAcadDisp)))
            throw (_com_error(hr));
        //get the AutoCAD::IAcadEntity
        AutoCAD::IAcadEntity *pEnt = NULL;
        if(FAILED(hr= pUnk->QueryInterface(AutoCAD::IID_IAcadEntity, (void **)&pEnt)))
            throw (_com_error(hr));
          /*Add acad entities to Selection set*/
        if (FAILED(hr = addToSelSet(pSet,pEnt)))
            throw(_com_error(hr)) ;
    }
      if (FAILED(hr = pDoc->Export(_bstr_t("c:\\temp\\test"),_bstr_t("BMP"),pSet)))
        throw(_com_error(hr)) ;
    pSet->Release();
}
else
    return ;
pSelSets->Release();
}
pDoc->Release();
}
pAcad->Release();
}
pUnk->Release();
}
catch (...)
{
return ;
}
return ;
}

