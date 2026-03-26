---
title: "Get view border and reference path of Inventor"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - API
  - DWG
  - Database
description: "In the layout of a DWG, we placed an Inventor model by the command VIEWBASE. How i can read and resolve the Inventor file to other files. I found a..."
author: Autodesk
---
# Get view border and reference path of Inventor

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/get-view-border-and-reference-path-of-inventor.html

## 文章内容

By Xiaodong Liang
Issue
In the layout of a DWG, we placed an Inventor model by the command VIEWBASE. How i can read and resolve the Inventor file to other files. I found an object AcDbViewBorder which has the property inventorFileReference. But I did not know how to get AcDbViewBorder.
Solution
There’s no API to get AcDbViewBorder,but  you can scan through paper space as it can only exists in paper space. Please note: as many other Model Documentation APIs, they’re read-only. So currently you cannot move or re-organize the associated files.
  static void MyGroupMyCommand () {
    // Put your command code here
       AcDbDatabase *pDb
      = acdbHostApplicationServices()->workingDatabase();
       // Open block table record of paper space
   AcDbBlockTable *pBlockTable;
   Acad::ErrorStatus eStatus =
       pDb->getBlockTable(pBlockTable, AcDb::kForRead);
     // Find the Paper space block and open it for read.
   AcDbBlockTableRecord *pBlockTableRecord;
   eStatus = pBlockTable->getAt(ACDB_PAPER_SPACE,
               pBlockTableRecord, AcDb::kForRead);
     AcDbBlockTableRecordIterator* pBTRIter = NULL;
   pBlockTableRecord->newIterator(pBTRIter);
   while (!pBTRIter->done())
   {
          //Open each entity of the drawing for read
          AcDbEntity* pEnt = NULL;
          eStatus =
              pBTRIter->getEntity(pEnt, AcDb::kForRead);  
            //Find AcDbViewBorder Entity
          if (pEnt != NULL &&
             pEnt->isKindOf(AcDbViewBorder::desc()))
          {                                
                 //get viewborder object
                 AcDbViewBorder *pAcDbViewBorder =
                         (AcDbViewBorder*)pEnt;  
                 AcString invStr=
             pAcDbViewBorder->inventorFileReference();                   
          }
            if(eStatus == Acad::eOk)
            pEnt->close();
            pBTRIter->step();
   }
     delete pBTRIter;
   pBlockTable->close();
  }

