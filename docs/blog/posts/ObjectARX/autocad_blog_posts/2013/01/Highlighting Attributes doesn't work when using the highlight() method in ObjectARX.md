---
title: "Highlighting Attributes doesn't work when using the highlight() method in ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - ObjectARX
description: "When I call pAttribute->highlight(); it returns Acad::eOk but the attribute is not highlighted on screen."
author: Autodesk
---
# Highlighting Attributes doesn't work when using the highlight() method in ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/highlighting-attributes-doesnt-work-when-using-the-highlight-method-in-objectarx.html

## 文章内容

By Fenton Webb
Issue
When I call pAttribute->highlight(); it returns Acad::eOk but the attribute is not highlighted on screen.
I have also tried opening the block reference and highlighting the attribute via:
AcDbFullSubentPath subPath;
subPath.objectIds().append(pAttribute->id());
blkRef->highlight(subPath);
this method highlights the block reference and all attributes.
Is there any way to highlight only the attribute?
Solution
There is a defect which prevents the AcDbAttribute::highlight() from working correctly.
Here is a workaround...
//////////////////////////////////////////////////////////////////////////////
// This is command 'TEST, by Fenton Webb [Mar/11/2002], DevTech, Autodesk
void asdktest()
{
 ads_name ename;
 ads_point pt;
 // pick an entity to check
 int res = acedEntSel (_T("\nPick a block with attributes : "), ename, pt);
 // if the user didn't cancel
 if (res == RTNORM)
 {
  AcDbObjectId objId;
  // convert the ename to an object id
  acdbGetObjectId (objId, ename);
  // open the entity for read
  AcDbObjectPointer<AcDbBlockReference>blockRef (objId, AcDb::kForRead);
  // if ok
  if (blockRef.openStatus () == Acad::eOk)
  {
   // create an attribute iterator so we can check to see if any attribute asre attached
   AcDbObjectIterator *pAttributeIterator = blockRef->attributeIterator ();
   // if it allocated ok
   if (pAttributeIterator != NULL)
   {                    
    AcDbObjectId   ObjId;
    AcDbAttribute *pAttribute = NULL;          
    // now loop through them
    for (int count=0; !pAttributeIterator->done(); pAttributeIterator->step(), ++count)
    {
     // get the object id of the attribute
     acdbGetAdsName(ename, pAttributeIterator->objectId());
     
     // highlight every other one
     if (!(count % 2))
     {
      // try and highlight it
      acedRedraw (ename, 3);
     }
    }
    // delete the iterator
    delete pAttributeIterator;
   }
  }
  else
  {
   AfxMessageBox(_T("This is not a block reference"));
  }
 }
}

