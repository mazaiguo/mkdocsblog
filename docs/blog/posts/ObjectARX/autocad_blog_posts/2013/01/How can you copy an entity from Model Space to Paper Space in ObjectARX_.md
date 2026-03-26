---
title: "How can you copy an entity from Model Space to Paper Space in ObjectARX?"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - ObjectARX
  - Selection
description: "To copy entities from Model Space to Paper Space in ObjectARX is actually quite straightforward. You can utilize the services of deepCloneObject() ..."
author: Autodesk
---
# How can you copy an entity from Model Space to Paper Space in ObjectARX?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-can-you-copy-an-entity-from-model-space-to-paper-space-in-objectarx.html

## 文章内容

By Gopinath Taget
To copy entities from Model Space to Paper Space in ObjectARX is actually quite straightforward. You can utilize the services of deepCloneObject() function to copy your select entities from Model Space into Paper Space. This is useful in situations where for example an older drawing contains a title block and you want to copy that title block into Paper Space. The following code defines command called "MS2PS". Simply select entities you want to copy over using a "window" style of selection:
// This is command 'MS2PS'
void ms2ps()
{
ads_point pt1, pt2;
ads_name ssEnts;
ads_name ent;
 long lenSS;
AcDbObjectId entId;
AcDbObjectIdArray arEntIds;
Acad::ErrorStatus es;
AcDbBlockTable* pBT;
AcDbObjectId idPS;
AcDbIdMapping idMap;
AcDbDatabase* pCurDb;
  pCurDb = acdbHostApplicationServices()->workingDatabase();
  acedGetPoint(NULL, L"\nSelect first point", pt1);
acedGetCorner(pt1, L"\nPick second corner point", pt2);
 // Select the entities that fall within the window.
acedSSGet(L"W", &pt1, &pt2, NULL, ssEnts);
   // Get the length of the selection set
acedSSLength(ssEnts, &lenSS);
 // convert the entities to ObjectId's and place
 // them in an objectid array.
 for(long i = 0; i < lenSS; i++)
{
  acedSSName(ssEnts, i, ent);
  acdbGetObjectId(entId, ent);
  arEntIds.append(entId);
}
 // Get the BlockTable
es = pCurDb->getBlockTable(pBT, AcDb::kForRead);
 // Get the Paper Space ObjectId
es = pBT->getAt(ACDB_PAPER_SPACE, idPS);
pBT->close();
   // Are there entities to copy to Paper Space?
 if(arEntIds.length() > 0)
{
  es = pCurDb->deepCloneObjects(arEntIds, idPS, idMap);
}
}

