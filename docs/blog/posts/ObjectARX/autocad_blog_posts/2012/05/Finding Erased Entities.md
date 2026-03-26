---
title: "Finding Erased Entities"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "When iterating the block table record using the “AcDbBlockTableRecordIterator”, it is possible to avoid skipping the erased entities. You must spec..."
author: Autodesk
---
# Finding Erased Entities

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/finding-erased-entities.html

## 文章内容

By Balaji Ramamoorthy
When iterating the block table record using the “AcDbBlockTableRecordIterator”, it is possible to avoid skipping the erased entities. You must specify “false” for last parameter in the newIterator() method of AcDbBlockTableRecord class (which is incidentally optional and is set to true i.e. skip the erased entities).
The sample code below lists all the entities that were erased in the ModelSpace. The comments included in the code mark the changes needed.
Acad::ErrorStatus es;
AcDbDatabase *pDb
    = acdbHostApplicationServices()->workingDatabase();
AcDbBlockTableRecordPointer pBTR
                    (
                        acdbSymUtil()->blockModelSpaceId(pDb),
                        AcDb::kForWrite
                    );
  //the last parameter should be false to get erased entities
AcDbBlockTableRecordIterator *pIter;
bool skipDeleted = false;
pBTR->newIterator(pIter, true, skipDeleted);
  int erasedEntityCount = 0;
AcDbEntity *pEnt;
while(!pIter->done())
{
    // if you specify true for last parameter then you will not
    // get eWasErased notification, but this also means you
    // will not be able to open the erased object
    es = pIter->getEntity(pEnt, AcDb::kForWrite, skipDeleted);
      if (es == Acad::eWasErased)
    {
        erasedEntityCount++;
        acutPrintf   
            (
                ACRX_T("\neWasErased, Entity number - %d"),
                erasedEntityCount
            );
    }
    else
    {
        pEnt->close();
    }
      // the last parameter should be false
    // to get the erased entities
    pIter->step(true, skipDeleted);
}
  acutPrintf    (
                ACRX_T("\nTotal number of erased entities: %i"),
                erasedEntityCount
            );
delete pIter;

