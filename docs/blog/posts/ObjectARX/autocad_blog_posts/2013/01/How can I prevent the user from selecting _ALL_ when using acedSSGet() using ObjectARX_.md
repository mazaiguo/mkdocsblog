---
title: "How can I prevent the user from selecting "ALL" when using acedSSGet() using ObjectARX?"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Selection
description: "Consider this: You would like to stop the user from selection ALL when using acedSSGet()? This because acedSSGet selects all of the entities in all..."
author: Autodesk
---
# How can I prevent the user from selecting "ALL" when using acedSSGet() using ObjectARX?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-can-i-prevent-the-user-from-selecting-all-when-using-acedssget-using-objectarx.html

## 文章内容

By Gopinath Taget
Consider this: You would like to stop the user from selection ALL when using acedSSGet()? This because acedSSGet selects all of the entities in all of the spaces and this is not your intent. You only want it selects ALL the entities from the current space. So how can you go about doing this?
In AutoCAD there is no way to stop the acedSSGet() from allowing the user to use the "All" option; this is as designed. The best way to do what you want is to simply check the selection set after the acedSSGet() and make sure that each entity is owned by the current space... Please check the code below:
// this function allows the user to
// type "all", but only the entities
// in the current space are selected
void asdkSelectALL()
{
ads_name ss;
 // get the selectionset
 int res = acedSSGet (NULL, NULL, NULL, NULL, ss);
 // if ok
 if (res == RTNORM)
{
  // get the length of the selection set
  long length = 0l;
  acedSSLength (ss, &length);
  // see what we have
  acutPrintf(L"\nBefore ss length = %ld", length);
  // now loop round and find out which ones are in Paper space
  for (long i=0l; i<length; ++i)
  {
   ads_name ename;
   // extract the ename
   if (acedSSName (ss, i, ename) != RTNORM)
    continue;
   AcDbObjectId objId;
   // convert the ename to an object id
   acdbGetObjectId (objId, ename);
   // open the entity for read
   AcDbObjectPointer<AcDbEntity>ent (objId, AcDb::kForRead);
   // if ok
   if (ent.openStatus () == Acad::eOk)
   {
    // get the owner object for this entity
    AcDbObjectId ownerId = ent->ownerId();
    // get the current dwg database
    AcDbDatabase *dwg =
     acdbHostApplicationServices()->workingDatabase();
    // if the entity owner id is not the
    // same as the current space id
    if (dwg->currentSpaceId() != ownerId &&
     dwg->viewportTableId() != ownerId &&
     dwg->paperSpaceVportId() != ownerId)
    {
     // remove the entity from the selection set
     acedSSDel (ename, ss);
    }
   }
  }
  acedSSLength (ss, &length);
  // see what we have
  acutPrintf(L"\nAfter ss length = %ld", length);
  // test code
  acedCommand (RTSTR, "._SELECT", RTPICKS,
   ss, RTSTR, "", RTNONE);
  // free the selection set after use
  acedSSFree (ss);
}
}
  Alternatively, you can implement an AcEdSSGetFilter to filter out whatever selections you want but that is the topic for another blog post .

