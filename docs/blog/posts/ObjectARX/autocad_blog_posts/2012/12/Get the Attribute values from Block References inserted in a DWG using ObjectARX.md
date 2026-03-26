---
title: "Get the Attribute values from Block References inserted in a DWG using ObjectARX"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - DWG
  - ObjectARX
description: "Here’s how to obtain the attribute values of all blocks inserted into Model Space DWG file using ObjectARX…"
author: Autodesk
---
# Get the Attribute values from Block References inserted in a DWG using ObjectARX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/get-the-attribute-values-from-block-references-inserted-in-a-dwg-using-objectarx.html

## 文章内容

by Fenton Webb
Here’s how to obtain the attribute values of all blocks inserted into Model Space DWG file using ObjectARX…
#include <dbobjptr.h>
void PrintBlockAttributes()
{
  // get the current database
  AcDbDatabase* pDb = acdbHostApplicationServices()->workingDatabase();
  assert(pDb);
   // in this sample we will only process block references in model space;
  // it is also possible to have block references in paper space
  // but I will leave it up to you to update the code to do so
  AcDbBlockTableRecordPointer pModelSpace(ACDB_MODEL_SPACE, pDb, AcDb::kForRead);
  assert(pModelSpace.openStatus() == Acad::eOk);
   // request an iterator for the entities in the block table record
  AcDbBlockTableRecordIterator *pIterator;
  pModelSpace->newIterator(pIterator);
   // iterate through each entity
  for( ; !pIterator->done(); pIterator->step()) 
  {
    AcDbObjectId id;
    pIterator->getEntityId(id);
    // we are only interested in block references;
    // ignore anything else
    AcDbObjectPointer<AcDbBlockReference> pBlockReference(id, AcDb::kForRead);
    if (pBlockReference.openStatus() != Acad::eOk)
      continue;
     // lets request the block reference for an attribute iterator
    AcDbObjectIterator *pAttributeIterator = NULL;
    pAttributeIterator = pBlockReference->attributeIterator();
     // iterate through each attribute and print its value
    for( ; !pAttributeIterator->done(); pAttributeIterator->step())
    {
      AcDbObjectId attributeId = pAttributeIterator->objectId();
      // open the attribute
      AcDbAttribute *pAttribute;
      Acad::ErrorStatus es = pBlockReference->openAttribute(pAttribute, attributeId, AcDb::kForRead);
      // finally; we are at a point where we have access tothe
      // value of the attribute -- for now, simply display it
       // AcDbAttribute is derived from AcDbText where the tag
      // value is stored
      ACHAR *pTag = pAttribute->tag();
      assert(pTag != NULL);
       ACHAR *pValue = pAttribute->textString();
      assert(pValue != NULL);
       // display
      acutPrintf(L"Tag: %s = Value: %s\n", pTag, pValue);
       // we no longer need this attribute so lets close it
      // and clean up the memory
      pAttribute->close();
      delete [] pTag;
      delete [] pValue;
    }
     // it is the programmer's responsibility to delete the
    // attribute iterator
    delete pAttributeIterator;
  }
   // it is the programmer's responsibility to delete the
  // block table record iterator
  delete pIterator;
}

