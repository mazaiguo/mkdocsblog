---
title: "Remove a boundary from a hatch"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Hatch
description: "The class AcDbHatch provides methods for getting the boundaries and for removing boundaries. Each boundary is a so-called loop. With AcDbHatch you ..."
author: Autodesk
---
# Remove a boundary from a hatch

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/remove-a-boundary-from-a-hatch.html

## 文章内容

By Augusto Goncalves
The class AcDbHatch provides methods for getting the boundaries and for removing boundaries. Each boundary is a so-called loop. With AcDbHatch you can iterate all loops. Then you can get all entities belonging to a single loop. All you have to do is to compare the handles of the loop entities with the handle of the boundary object which should be removed from the hatch object. If one of the entities of the loop has the handle you are looking for you can use AcDbHatch::removeLoopAt() to remove the loop from the hatch.
The following function will do this. The parameter handleRemove is the handle of an entity belonging to a loop which should be removed.
void removeHandleFromHatch(const ACHAR* handleRemove)
{
  // Create an AcDbHandle object from the input handle
  AcDbHandle removeHandle(handleRemove);
  //
  //  Get the hatch
  //
  ads_point dummy;
  ads_name ename;
  if (RTNORM != ads_entsel(L"\nSelect a hatch: ", ename, dummy)) 
    return; AcDbObjectId hatchId;
  AcDbHatch *pHatch;
  if (Acad::eOk != acdbGetObjectId(hatchId, ename))
  { 
    ads_printf(L"\nCannot get objectId from hatch entity."); 
    return;
  }
  if (Acad::eOk != acdbOpenObject(pHatch, hatchId, AcDb::kForRead))
  {  
    ads_printf(L"\nCannot open hatch");
    return;
  }
  //
  // Analyze hatch
  //
  int loops = pHatch->numLoops();   // number of loops
  ads_printf(L"\nNumber of loops: %i", loops);
  // Get all loops
  AcDbObjectIdArray loopIds;
  for (int i = 0; i < loops; ++i)
  {
    // Get the object ID's of all entities
    // belonging to this loop 
    pHatch->getAssocObjIdsAt(i, loopIds);
    // Get all objects from this loop 
    int numOfObjects = loopIds.logicalLength();
    AcDbEntity *pEnt;   AcDbHandle handle; 
    for (int j = 0; j < numOfObjects; ++j)
    { 
      if (Acad::eOk != acdbOpenObject(pEnt, loopIds[j],
        AcDb::kForRead))
      {  
        ads_printf(L"\nCannot get object from loop %i.", i); 
        continue; 
      }    
      // Get handle of current loop entity 
      // and compare it with the input handle 
      pEnt->getAcDbHandle(handle); 
      pEnt->close();
      // no longer needed 
      if (handle == removeHandle)
      { 
        ads_printf(L"\nBoundary entity found.");
        // Remove loop from hatch entity
        pHatch->upgradeOpen();  
        pHatch->removeLoopAt(i); 
        pHatch->downgradeOpen();
        break;    
      }  
    } 
    loopIds.setLogicalLength(0);
  }
  // Close hatch
  pHatch->close();
}

