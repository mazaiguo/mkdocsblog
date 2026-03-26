---
title: "Get Block that Entities are included in"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Block
description: "You can use the ownerId() method of sub entities in an block reference (INSERT) entity to get the object id of the block table record (block defini..."
author: Autodesk
---
# Get Block that Entities are included in

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/get-block-that-entities-are-included-in.html

## 文章内容

By Barbara Han
You can use the ownerId() method of sub entities in an block reference (INSERT) entity to get the object id of the block table record (block definition) that the INSERT references to, and then get the block’s information, i.e. name. The following code shows how to do this. The function acedNEntSelP() is used to get a sub entity in a INSERT block.
void getBlockNameFromItsSubentity()
{
  Acad::ErrorStatus es;
  ads_name ent;
  ads_point pt;
  ads_matrix xform;
  struct resbuf* pRb = NULL;
  if( acedNEntSelP(L"\nSelect an subentity inside an INSERT: ",
    ent, pt, FALSE, xform, &pRb) != RTNORM )
  {
    acutPrintf(L"\acedNEntSelP failed");
    return;
  }
    AcDbObjectId subEntId;
  AcDbEntity* pSubEnt = NULL;
  if( (es = acdbGetObjectId(subEntId, ent)) != Acad::eOk ||
    (es = acdbOpenAcDbEntity(pSubEnt, subEntId,
    AcDb::kForRead)) !=
    Acad::eOk )
  {
    acutPrintf(L"\nFailure: %s", acadErrorStatusText(es));
    acutRelRb(pRb);
    return;
  }
  acutRelRb(pRb);
    // Output the class name of the sub entity
    acutPrintf(L"\nThe sub entity is of type %s",
    pSubEnt->isA()->name());
    // Get the object id of the owner block
    AcDbObjectId mainId = pSubEnt->ownerId();
  pSubEnt->close();
  pSubEnt = NULL;
    AcDbObject* pOwner = NULL;
  if((es = acdbOpenObject(pOwner, mainId, AcDb::kForRead)) !=
    Acad::eOk )
  {
    acutPrintf(L"\nFailure: %s", acadErrorStatusText(es));
    return;
  }
    // Output the class name of the owner block
    acutPrintf(L"\nThe owner is of type %s",
    pOwner->isA()->name());
    // Output the information of the block definition
    AcDbBlockTableRecord *pBTR = NULL;
  pBTR = AcDbBlockTableRecord::cast(pOwner);
  if( pBTR != NULL )
  {
    const ACHAR* pBlkName;
    pBTR->getName(pBlkName);
    acutPrintf(L"\nBlock name is %s", pBlkName);
  }
    pOwner->close();
  pOwner = NULL;
}
Not only the sub entities, the similar method can also apply to almost all entities, e.g. line segments of 3d polylines, old style 2d polylines, mesh face of 3d meshes, simple entities, and even viewports.

## 评论

**内容**: Oleg said...
Hi, Barbara
I've mentioned, if I selected, say, dimension insde the block instance, this code will return a BlockTableRecord named "*D#" as
its name, it seems to me it is needs to search for an owner further,
maybe recursive will be help to get the real owner?
Regards,
Oleg
Reply
06/10/2012 at 12:50 AM

---
**内容**: Chris said...
Is it possible to get the ObjectId of the BlockReference that contains the selected nested entity?
Reply
09/06/2012 at 02:49 AM

---
