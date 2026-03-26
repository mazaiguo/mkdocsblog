---
title: "Reloading linetype from file"
date: 2015-03-01
categories:
  - AutoCAD
tags:
  - Database
description: "The "AcDbDatabase::loadLineTypeFile" can load linetypes from a linetype file. If the linetype with the same name already exists in the database, th..."
author: Autodesk
---
# Reloading linetype from file

发布日期: 2015-03-01

原始链接: https://adndevblog.typepad.com/autocad/2015/03/reloading-linetype-from-file.html

## 文章内容

By Virupaksha Aithal
The "AcDbDatabase::loadLineTypeFile" can load linetypes from a linetype file. If the linetype with the same name already exists in the database, then the loadLineTypeFile method can return an error code. A way to force the reloading of linetype is to load the linetype in another database and clone the linetype back to the host database to replace it. Here is a code snippet to do that :
 Acad::ErrorStatus es;
   AcDbDatabase *pDb = 
     acdbHostApplicationServices()->workingDatabase();
 TCHAR szLtFile[MAX_PATH];
 if  ( RTNORM != 
     acedFindFile(_T("TrimCADLinetypes.LIN"), szLtFile) ) 
 {
  acutPrintf(ACRX_T("\\nLinetype file not  found !"));
  return ;
 }
   AcDbLinetypeTable *pLtTable = NULL;
 es = pDb->getLinetypeTable(pLtTable,AcDb::kForRead);
 ACHAR *szLtype = ACRX_T("FLATDOTS");
 bool isLinetypeLoaded = pLtTable->has(szLtype);
 es = pLtTable->close();
   if (isLinetypeLoaded)
 {
  // Already loaded, try  reloading the linetype
  AcDbDatabase *pTempDatabase 
                     = new  AcDbDatabase(true, false );
  es = pTempDatabase->loadLineTypeFile
                                  (szLtype, szLtFile);
  if (Acad::eOk == es)
  {
   AcDbLinetypeTable *pTempLtTable;
   AcDbLinetypeTableRecord *pTempLtRec=NULL;
     es = pTempDatabase->getLinetypeTable(
                   pTempLtTable,AcDb::kForRead);
   AcDbObjectId ltRecId = AcDbObjectId::kNull;
   es = pTempLtTable->getAt(szLtype, ltRecId);
   pTempLtTable->close();
     AcDbObjectIdArray objIdArray;
   objIdArray.append(ltRecId);
     AcDbIdMapping idMap;
   es = pDb->wblockCloneObjects(
               objIdArray, 
               pDb->linetypeTableId(), 
                     idMap, 
                     AcDb::kDrcReplace);
   if (Acad::eOk == es)
   {
    acutPrintf(
        ACRX_T("\\nLinetype reloaded !"));
   }
   else 
   {
    acutPrintf(
             ACRX_T("\\nSorry, could not  reload Linetype !"));
   }
  }
  else 
  {
   acutPrintf(
         ACRX_T("\\nError loading linetype from  file !"));
  }
  delete pTempDatabase;
 }
 else  
 {// Not  loaded, try  loading the linetype
  if  ( Acad::eOk == 
      pDb->loadLineTypeFile(szLtype, szLtFile)) 
  {
   acutPrintf(
       ACRX_T("\\nLinetype loaded from  file !"));
  }
  else 
  {
   acutPrintf(
       ACRX_T("\\nError loading linetype from  file !"));
  }
 }

