---
title: "Determine whether an object is inserted as an XRef"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Block
  - DWG
  - Database
  - XREF
description: "I run a query in a drawing to find entities that are part of an external reference (Xref), and am using AcDbObject::ownerId() to find the ID of the..."
author: Autodesk
---
# Determine whether an object is inserted as an XRef

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/determine-whether-an-object-is-inserted-as-an-xref.html

## 文章内容

By Xiaodong Liang
Issue
I run a query in a drawing to find entities that are part of an external reference (Xref), and am using AcDbObject::ownerId() to find the ID of the object's owner. After opening the owner (an AcDbBlockTableRecord) and calling its isFromExternalReference() function, it always returns False - even for an object that was inserted as part of an external reference. Why?
Solution
The problem is that you are invoking isFromExternalReference() on the wrong object. 
Let us suppose you create AcDbLine (named "Line" in this example) in the model space of a drawing and save it as Test.dwg. Then you create another drawing named New.dwg and insert Test.dwg as an XRef into the model space of the new drawing.
The block table in the database for New.dwg now holds an AcDbBlockTableRecord named "TEST". "TEST" holds an entry for "Line". The model space in New.dwg has an AcDbBlockReference to "TEST".
If you have a pointer to the AcDbBlockTableRecord for "TEST" (pBTR, say), a call to pBTR->isFromExternalReference() will correctly return True. A call to pBTR->ownerId() returns the ObjectID of the block table of New.dwg (for example, "TEST" is an XRef and is owned by the block table of New.dwg).
If you have a pointer to "Line" (pObj), you could find the ObjectId of its owner, using pObj->ownerId(). The AcDbObjectId returned by this call is not the ObjectId of "TEST"; it is the ObjectId of the model space of the database for Test.dwg that was opened when the XRef was inserted. The model space of Test.dwg is not an XRef of Test.dwg, and so it returns False when isFromExternalReference() is called.
Therefore, this is a situation where "TEST" effectively 'owns' "Line", but "Line" does not consider "TEST" to be its 'owner'.
The simplest way to determine whether any given object has been inserted as an XRef is to compare its database (using AcDbObject::database()) to that of the current drawing if it is different, then the object is an XRef.
This example demonstrates this.
static void ASDKTEST_ARX_TestXref(void)
{
  // Get the Block Table Record for the XRef "Test"
  AcDbDatabase * pDb =
      acdbHostApplicationServices()->workingDatabase();
  AcDbBlockTable * pBT;
  pDb->getSymbolTable(pBT, AcDb::kForRead);
  AcDbBlockTableRecord * pTest;
  pBT->getAt(_T("Test"), pTest,AcDb::kForRead);
  pBT->close();
    // See if "Test" is an XRef
  if (pTest->isFromExternalReference())
  {
   acutPrintf(_T("\nTest is an XRef."));
  }
  else
  {
   acutPrintf(_T("\nTest is not an XRef."));
  }
    // Get pointer to 'Line' stored in 'Test' block table record
  // Because 'Line' belongs to "Test",
  // it seems obvious that 'Line''s owner is "Test"
  AcDbBlockTableRecordIterator * pIter;
  pTest->newIterator(pIter);
  AcDbLine * pLine = NULL;
  for( ; ((!pIter->done()) && (pLine == NULL)); pIter->step())
  {
   AcDbEntity * pEnt;
   pIter->getEntity(pEnt, AcDb::kForRead);
   pLine = AcDbLine::cast(pEnt);
   if (pLine != NULL)
   {
    break;
   }
   else
   {
    pEnt->close();
   }
  }
  pTest->close();
  delete pIter;
      // Query line's owner to see if it is an XRef
  //  Now we find that 'Line' is not owned by "Test"
  if (pLine != NULL)
  {
   AcDbObjectId objId = pLine->ownerId();
   AcDbObject * pObj;
   acdbOpenObject(pObj, objId, AcDb::kForRead);
   AcDbBlockTableRecord * pBTR;
   pBTR = AcDbBlockTableRecord::cast(pObj);
   if (pBTR !=NULL)
   {
    // If you compare the addresses of pBTR and pTest
    // you will see that  they are not the same object.
    if ( pBTR->isFromExternalReference() )
    {
     acutPrintf(_T("\nLine's owner is an XRef."));
    }
    else
    {
     acutPrintf(_T("\nLine's owner is not an XRef."));
    }
   }
   pLine->close();
   pObj->close();
  }
}

## 评论

**内容**: Jeffrey Suffet said...
Hello - Can you demonstrate using the .NET Managed API?
Reply
02/09/2015 at 10:11 AM

---
