---
title: "Selecting specific entities from a pickfirst selection set"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Selection
description: "The 'PICKFIRST' system variable, when set to a value of '1' allows the user to preselect entities prior to executing an AutoCAD command. This also ..."
author: Autodesk
---
# Selecting specific entities from a pickfirst selection set

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/selecting-specific-entities-from-a-pickfirst-selection-set.html

## 文章内容

By Gopinath Taget
The 'PICKFIRST' system variable, when set to a value of '1' allows the user to preselect entities prior to executing an AutoCAD command. This also applies to ARX defined commands.
There are two ARX functions that allow capture of pre-selected entities into a selection set. These functions are: acedSSGet() with the "I" option, and the more recent acedSSGetFirst() function. The following code snippet demonstrates. The command name is 'pfss'.
If a user has pre-selected entities and the 'pfss' command is executed, the pre-selected entities are placed into the 'pfSet' selection set. Verify that the length of the selection is greater that '0' and if so, process the 'for' loop. In the 'for', the ObjectId for each entitiy is retrieved and the entity is opened for a 'read' operation. The entity is then tested using the 'isA()' function. You can also test for custom entities, substituting the custom class name here.
The 'cast()' or 'isKindOf()' functions could also be used. Refer to the ObjectARX documentation for a description of these functions. If the entity is an AcDbLine entity (or a custom entity) the variable 'lineEntCount' is incremented. The entity is then closed and the 'for' loop is processed again. The results of the findings are then reported to the user. The function acedSSGetFirst() is illustrated toward the end of the code fragment. This function requires two result buffers pointers, the first result bufffer 'prbGrip' contains entities that are 'gripped' but not selected, and the second result buffer 'prbPick' contains entities that are pre-selected. If no entites were pre-selected, then the 'restype' of the 'prbPick' result buffer will contain the value 'RTNONE', however, if entities were pre-selected the 'restype' field will contain the value 'RTPICKS'. If this is the case, the result buffer resval.rlname field will contain the selection set. Be sure to free the selection sets prior to releasing the result buffers.
void pfss()
{
AcDbEntity *pEnt;
AcDbObjectId entId;
Acad::ErrorStatus es;
 int retCode;
ads_name pfSet; // 'PICKFIRST' Selection Set
ads_name ename; long pfSetLen;
 // 'PICKFIRST' Selection Set Length
 long lineEntCount = 0;
acedSSGet(L"I", NULL, NULL, NULL, pfSet);
acedSSLength(pfSet, &pfSetLen);
 // Verify that the selection set is not empty
 if(pfSetLen > 0)
{
  acutPrintf(L"\nThere are %d entities pre-selected.",
   pfSetLen);
  // Loop through the selection set
  for(long i = 0; i < pfSetLen; i++)
  {
   retCode = acedSSName(pfSet, i, ename);
   if(retCode != RTNORM)
   {
    acutPrintf(
     L"\nError retreiving entity from selection set");
    break;
   }
   es = acdbGetObjectId(entId, ename);
   if(es != Acad::eOk)
   {
    acutPrintf(
     L"\nFailed to get AcDbObjectId of entity.");
    break;
   }
   es = acdbOpenAcDbEntity(pEnt, entId, AcDb::kForRead);
   if(es != Acad::eOk)
   {
    acutPrintf(
     L"\nFailed to open entity for a read operation");
    break;
   }
   // Here we are testing specifically for a AcDbLine entity
   // we could equally test for a custom entity,
   // provided it is part of the hierarchy tree.
   // We could have also used the cast() and isKindOf()
   // methods. See Runtime Type Identification
   // in the ObjectARX documentation
   // for a description of these methods.
   if(pEnt->isA() == AcDbLine::desc())
   {
    // Increment the line counter
    lineEntCount++;
   }
   // Don't forget to close the entity when
   // you are finished with it.
   pEnt->close();
  } // for
  acutPrintf(
  L"\nThere were %d AcDbLine class entities in the selectionset.",
   lineEntCount);
} // Then
 else
{
  acutPrintf(
   L"\nNo entities were pre-selected.");
}
 // Dont forget to free the selection set.
acedSSFree(pfSet);
 // Here we demonstrate how to use the function acedSSGetFirst()
 // to retrieve the pre-selected entities in a selection set.
 // prbGrip is a resbuf that contains a selection
 // set for entities which have grips but are not selected.
 // prbPick is a resbub that contains a selection set in resval.rlname
 // and are the entites that are pre-selected.
 // Grips may or may not be enabled.
 // This is the selection set of interest
 struct resbuf* prbGrip = NULL;
 struct resbuf* prbPick = NULL;
 // Get the selection sets
acedSSGetFirst(&prbGrip, &prbPick);
 long gripLen, pickLen;
acedSSLength(prbPick->resval.rlname, &pickLen);
acedSSLength(prbGrip->resval.rlname, &gripLen);
acutPrintf(
L"\nThere are %d pre-selected entities using the acedSSGetFirst()function.",
pickLen);
 // Don't forget to free the selections sets.
acedSSFree(prbPick->resval.rlname);
acedSSFree(prbGrip->resval.rlname);
 // Also don't forget to release the result buffers
acutRelRb(prbGrip);
acutRelRb(prbPick);
}

