---
title: "Get the information of a nested entity in an XREFed drawing and its associated groups"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Database
  - XREF
description: "The following piece of code does this. Please be informed of the following key points:"
author: Autodesk
---
# Get the information of a nested entity in an XREFed drawing and its associated groups

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/get-the-information-of-a-nested-entity-in-an-xrefed-drawing-and-its-associated-groups.html

## 文章内容

By Gopinath Taget
The following piece of code does this. Please be informed of the following key points:
1. Please use acedNEntSelP() function to select the nested entity instead of acedEntSel().
2. We use obj->database()->getFilename(fname) to get the XREF drawing name.
3. Group object is a persistent reactor attached to its members. We can get all reactors with obj->reactors() function.
void BZH_readxref()
{
 //  Get the information of a nested entity
 // in an XREF drawing,
 //  Output the group information associated
 // with the entity if applicable.
 int result ;
ads_name ent;
ads_point ptres;
 int pickflag;
ads_matrix xformres;
 struct resbuf* refstkres;
  pickflag=0;
result = acedNEntSelP(
  _T("\nSelect a nested entity: "), \
  ent, ptres, pickflag, xformres,
  &refstkres);
   if (result==RTNORM) {
  AcDbObjectId objId;
  AcDbObject* obj;
  Acad::ErrorStatus es;
  CString str;
  acdbGetObjectId(objId, ent);
  es = acdbOpenAcDbObject(
   obj, objId, AcDb::kForRead);
  assert(es == Acad::eOk);
  acutPrintf(
   _T("\n\nClass Name: %s"), obj->isA()->name());
  acutPrintf(_T("\nEntity Name: %lx"), ent[0]);
    AcDbHandle handle;
  ACHAR tempStr[256];
  obj->getAcDbHandle(handle);
  handle.getIntoAsciiBuffer(tempStr);
  str = tempStr;
  acutPrintf(_T("\nHandle: %s"), str);
    const ACHAR* fname;
  es = obj->database()->getFilename(fname);
  acutPrintf(_T("\nDatabase: %s"), fname);
    void* pSomething;
  AcDbVoidPtrArray* reactors = obj->reactors();
  if (reactors != NULL) {
   for (int i=0; i<reactors->length(); i++) {
    pSomething = reactors->at(i);
    if (acdbIsPersistentReactor(pSomething)) {
     AcDbObject* pTempObj;
     es = acdbOpenObject(
      pTempObj,
      acdbPersistentReactorObjectId(pSomething),
      AcDb::kForRead);
     AcDbGroup* pGroup;
     pGroup  = AcDbGroup::cast (pTempObj);
     if( pGroup == NULL )
      continue;
     else {
      pGroup->getAcDbHandle(handle);
      handle.getIntoAsciiBuffer(tempStr);
      str = tempStr;
      acutPrintf(_T("\nGroup handle: %s"), str);
     }
    }
   }
  }
  obj->close();
}
 else
  acutPrintf(_T("\nacedNEntSelP error!"));
   return;
}

