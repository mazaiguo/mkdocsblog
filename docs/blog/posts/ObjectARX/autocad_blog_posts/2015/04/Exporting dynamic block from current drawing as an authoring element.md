---
title: "Exporting dynamic block from current drawing as an authoring element"
date: 2015-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - DWG
  - Database
description: "Dynamic blocks from a drawing can be wblocked to a new drawing, as an authoring element. This helps archive the dynamic blocks and reuse them when ..."
author: Autodesk
---
# Exporting dynamic block from current drawing as an authoring element

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/exporting-dynamic-block-from-current-drawing-as-an-authoring-element.html

## 文章内容

By Balaji Ramamoorthy
Dynamic blocks from a drawing can be wblocked to a new drawing, as an authoring element. This helps archive the dynamic blocks and reuse them when required. The new drawing can be inserted to get the dynamic block into any other drawing. In AutoCAD UI, an authoring element can be created by using the WBLOCK command and selecting a dynamic block from the list of available ones from the current drawing. The same can also be done using code as shown in the following code snippet :
 // Wblock a dynamic block as an AuthoringElement 
 Acad::ErrorStatus es;
   AcApDocument *pActiveDoc 
  = acDocManager->mdiActiveDocument();
 AcDbDatabase *pCurDb = pActiveDoc->database();
   AcDbBlockTable* pCurentDwgBlockTable;
 es = pCurDb->getBlockTable(
  pCurentDwgBlockTable, kForRead);
 if  ( es == eOk) 
 {
  AcDbBlockTableRecord* pRecord;
    // Assuming "Test" dynamic block 
  // being present in the current drawing 
  es = pCurentDwgBlockTable->getAt(
   ACRX_T("Test" ), 
   pRecord, 
   kForRead, false );
  if  (es != eOk) 
  {
   pCurentDwgBlockTable->close();
   return ;
  }
    AcDbObjectId btrId = pRecord->objectId();
  pRecord->close();
  pCurentDwgBlockTable->close();
    // Create the destination database 
  AcDbDatabase *pNewDb = NULL;
  es = pCurDb->wblock(pNewDb, btrId);
  if (es == Acad::eOk)
  {
   es = pNewDb->saveAs(
    _T("D://Temp//TestBlock.dwg" ));
   delete  pNewDb;
  }
 }

