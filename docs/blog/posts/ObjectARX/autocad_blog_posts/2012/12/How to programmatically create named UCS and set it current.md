---
title: "How to programmatically create named UCS and set it current"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - UCS
description: "The following piece of code demonstrates creation of named UCS and setting it as current. A couple of important functions to remember:"
author: Autodesk
---
# How to programmatically create named UCS and set it current

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-programmatically-create-named-ucs-and-set-it-current.html

## 文章内容

By Gopinath Taget
The following piece of code demonstrates creation of named UCS and setting it as current. A couple of important functions to remember:
1.acedVports2VportTableRecords() - This function should be called before we access the vport table.
2.acedVportTableRecords2Vports() - This function should be called at the end to force the changes to vport table.
The above two functions are necessary to force AutoCAD to update the viewports with the current settings.
// - asdkucsarx._test command (do not rename)
 static void asdkucsarx_test(void)
{
  Acad::ErrorStatus es;
  AcDbUCSTableRecord *myUCS = new AcDbUCSTableRecord;
    //define your own ucs
  AcGePoint3d  origin_point(0,0,0);
  AcGeVector3d UCSXaxis(0,1,0);
  AcGeVector3d UCSYaxis(1,0,0);
    myUCS->setOrigin(origin_point);
  myUCS->setXAxis(UCSXaxis);
  myUCS->setYAxis(UCSYaxis);
    es=myUCS->setName( _T("MyUCS"));
  if (es != Acad::eOk)
  {
   acutPrintf(_T("\nFailed to set name"));
   return;
  }
    AcDbObjectId UCSId;
  AcDbSymbolTable *pUCSTable;
    if (acdbHostApplicationServices()->workingDatabase()->
   getUCSTable(pUCSTable,AcDb::kForWrite)==Acad::eOk)
  {
   es=pUCSTable->add(UCSId,myUCS);
   es=pUCSTable->close();
   es= myUCS->close();
  }
  else
  {
   acutPrintf(_T("\nFailed to get UCS table"));
   return;
  }
    //To set the current UCS, I accessed
  // the active AcDbViewportTableRecord
  // and used setUCS to set the UCS I created as current.
  AcDbViewportTable *pVT;
  es = acedVports2VportTableRecords();
  if (es != Acad::eOk)
  {
   acutPrintf(
   _T("\nFailed to load vport info into vport table records"));
   return;
  }
    es=acdbHostApplicationServices()->
   workingDatabase()->getViewportTable(pVT,AcDb::kForRead);
  if (es != Acad::eOk)
  {
   acutPrintf(_T("\nFailed to get vport table"));
   pVT->close();
   return;
  }
    AcDbViewportTableIterator* pIter = NULL;
    es=pVT->newIterator(pIter);
  if (es != Acad::eOk)
  {
   acutPrintf(_T("\nFailed to get vport table"));
   pVT->close();
   delete pIter;
   return;
  }
    for (pIter->start();!pIter->done();pIter->step())
  {
     AcDbViewportTableRecord* pRec;
   //it should be open for write mode
   es=pIter->getRecord(pRec,AcDb::kForWrite);
   if (es != Acad::eOk)
   {
    acutPrintf(
     _T("\nFailed to get vport table record"));
    pVT->close();
    pRec->close();
    delete pIter;
    return;
   }
     TCHAR* name=NULL;
   es=pRec->getName(name);
   if (es != Acad::eOk)
   {
    acutPrintf(
     _T("\nFailed to get name from vport table"));
    pVT->close();
    pRec->close();
    delete pIter;
    return;
   }
     if (_tcsicmp(name,_T("*ACTIVE"))==0)
   {
    es=pRec->setUcs(UCSId);
   }
     es=pRec->close();    
  }
  es=acedVportTableRecords2Vports(); //force update
    es=pVT->close();
  delete pIter;
  return ;
}

