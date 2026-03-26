---
title: "Identifying layer property overrides for a viewport"
date: 2015-06-01
categories:
  - AutoCAD
tags:
  - Database
  - Layer
description: "Here is a sample code to identify the layers that have their properties overridden for a viewport and to list the property overrides. The "AcDbLaye..."
author: Autodesk
---
# Identifying layer property overrides for a viewport

发布日期: 2015-06-01

原始链接: https://adndevblog.typepad.com/autocad/2015/06/identifying-layer-property-overrides-for-a-viewport.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to identify the layers that have their properties overridden for a viewport and to list the property overrides. The "AcDbLayerTableRecord::hasAnyOverrides" should quickly let us know if there are any overrides for any of the viewports. If it does exist, we can get to the details using "AcDbLayerTableRecord::hasOverrides" and provide the ObjectId of the viewport for which we want to know the overrides.
 Acad::ErrorStatus es;
   AcDbDatabase *pDb 
  = acdbHostApplicationServices()->workingDatabase();
 ads_point pt;
 ads_name ename;
 if  ( RTNORM != 
  acedEntSel(ACRX_T("Select a viewport :" ), 
  ename, pt))
  return ;
   AcDbObjectId vpid = AcDbObjectId::kNull;
 if  ( Acad::eOk != acdbGetObjectId(vpid, ename ))
  return ;
   AcDbObjectId layerId = AcDbObjectId::kNull;
 AcDbLayerTable* pLayerTable;
 pDb->getSymbolTable(pLayerTable, AcDb::kForRead);
   AcDbLayerTableIterator *pIter = NULL;
 AcDbLayerTableRecord *pLTR = NULL;
   pLayerTable->newIterator(pIter);
 for  (;! pIter->done(); pIter->step()) 
 {
  es = pIter->getRecord(pLTR, AcDb::kForRead);
  if (! pLTR->hasAnyOverrides())
  {
   pLTR->close();
   continue ;
  }
    if (! pLTR->hasOverrides(vpid))
  {
   pLTR->close();
   continue ;
  }
    TCHAR *lname;
  pLTR->getName(lname);
  acutPrintf(L"\\n Layer : %s has the following overrides :" ,
   lname);
    bool  isOverriddenForVP = Adesk::kFalse;
  AcCmColor clr = pLTR->color(vpid, isOverriddenForVP);
  if (isOverriddenForVP)
  {
   acutPrintf(L"\\n Color override" );
  }
         isOverriddenForVP = Adesk::kFalse;
  AcDbObjectId ltypeId 
   = pLTR->linetypeObjectId(
   vpid, isOverriddenForVP);
  if (isOverriddenForVP)
  {
   acutPrintf(L"\\n Linetype override" );
  }
    isOverriddenForVP = Adesk::kFalse;
  AcDb::LineWeight lw 
   = pLTR->lineWeight
   (vpid, isOverriddenForVP);
  if (isOverriddenForVP)
  {
   acutPrintf(L"\\n Lineweight override" );
  }
         isOverriddenForVP = Adesk::kFalse;
  ACHAR *psName = pLTR->plotStyleName
   (vpid, isOverriddenForVP);
  if (isOverriddenForVP)
  {
   acutPrintf(L"\\n Plotstyle override" );
  }
     pLTR->close();
 }
     delete  pIter;
 pLayerTable->close();

## 评论

**内容**: Paul Li said...
Can you provide a visual lisp example after identifying the layer name where there's a vport override, how to identify the color # set on the vport layer override?
Reply
10/10/2021 at 03:12 PM

---
