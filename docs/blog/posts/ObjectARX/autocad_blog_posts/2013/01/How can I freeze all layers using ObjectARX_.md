---
title: "How can I freeze all layers using ObjectARX?"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Layer
  - ObjectARX
description: "Here is how you can freeze all layers apart from the current one using ObjectARX:"
author: Autodesk
---
# How can I freeze all layers using ObjectARX?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-can-i-freeze-all-layers-using-objectarx.html

## 文章内容

By Gopinath Taget
Here is how you can freeze all layers apart from the current one using ObjectARX:
void adcgfreezeall()
{
AcDbLayerTable*pTable = NULL;
AcDbLayerTableRecord*pRecord = NULL;
Acad::ErrorStatus acEs;
  acEs = acdbHostApplicationServices()->
  workingDatabase()->getLayerTable(pTable, AcDb::kForRead );
   if( acEs != Acad::eOk )
{
  acutPrintf(_T("Cannot open layer table %s"),
   acadErrorStatusText(acEs));
  return;
}
  AcDbObjectId currentId = acdbHostApplicationServices()->
  workingDatabase()->clayer();
AcDbObjectId recordId;
AcDbLayerTableIterator*pIter;
   for( pTable->newIterator(pIter); !pIter->done(); pIter->step() )
{
  acEs = pIter->getRecordId(recordId);
  if( acEs != Acad::eOk )
  {
   acutPrintf(_T("Cannot get layer %s"),
    acadErrorStatusText(acEs));
   continue;
  }
    if( recordId == currentId )
   continue;
    AcDbObject*pObj = NULL;
  acEs = acdbOpenAcDbObject(pObj, recordId, AcDb::kForWrite );
  pRecord = AcDbLayerTableRecord::cast(pObj);
  if( acEs != Acad::eOk || pRecord == NULL)
  {
   acutPrintf(_T("Cannot open layer %s"),
    acadErrorStatusText(acEs));
     if( pObj != NULL )
    pObj->close();
   continue;
  }
    acEs = pRecord->setIsFrozen( Adesk::kTrue );
  pRecord->close();
  if( acEs != Acad::eOk )
  {
   acutPrintf(_T("Cannot set layer to be frozen %s"),
    acadErrorStatusText(acEs));
  }
    pRecord = NULL;
}
 delete pIter;
pTable->close();
}

