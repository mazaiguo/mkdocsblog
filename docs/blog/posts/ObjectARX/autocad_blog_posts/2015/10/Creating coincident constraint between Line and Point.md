---
title: "Creating coincident constraint between Line and Point"
date: 2015-10-01
categories:
  - AutoCAD
tags:
  - API
description: "The High-Level API wrapper for creating constraints was created by my colleagues Philippe Leefsma and Gopinath Taget which simplifies the creation ..."
author: Autodesk
---
# Creating coincident constraint between Line and Point

发布日期: 2015-10-01

原始链接: https://adndevblog.typepad.com/autocad/2015/10/creating-coincident-constraint-between-line-and-point.html

## 文章内容

By Balaji Ramamoorthy
The High-Level API wrapper for creating constraints was created by my colleagues Philippe Leefsma and Gopinath Taget which simplifies the creation of constraints using the API. In a recent query, a developer reported that the library was not helping create a coincident constraint between a Line and a Point. After debugging through it, what was causing it to fail is that the Constraints library was created in a generic way that did not consider that the Point entity did not have edge sub-entities for it. Also, when creating a coincident constraint between two entities and one of them being a Point entity, the subentity path of the vertex is required to be added to the constraint group before the constrained geometry can be created.
Here are the changes to Constraints library :
 Acad::ErrorStatus AcDbAssoc2dConstraintAPI
   ::createCoincidentConstraint(
  AcDbObjectId& entId1, 
  AcDbObjectId& entId2, 
  AcGePoint3d& ptEnt1, 
  AcGePoint3d& ptEnt2)
 {
  Acad::ErrorStatus es = Acad::eOk;
    if ((es = AcDbAssocManager::initialize()) != Acad::eOk)
   return  es;
    AcDbFullSubentPathArray aPaths;
    AcDbFullSubentPath edgeEntPath1;
  if (entId1.objectClass() != AcDbPoint::desc())
  {
   if ((es = ADNAssocSampleUtils
    ::getClosestEdgeSubEntPath(
    entId1, ptEnt1, 
    edgeEntPath1)) != Acad::eOk)
      return  es;
   aPaths.append(edgeEntPath1); 
  }
     AcDbFullSubentPathArray aVertexPaths;
    AcDbFullSubentPath vertEntPath1;
  AcGePoint3d vertexPos1;
  if ((es = ADNAssocSampleUtils
   ::getClosestVertexInfo
   (entId1, edgeEntPath1, ptEnt1, 
   vertexPos1, vertEntPath1)) != Acad::eOk)
   return  es;
  aVertexPaths.append(vertEntPath1);
    if (entId1.objectClass() == AcDbPoint::desc())
  {
   aPaths.append(vertEntPath1); 
  }
    AcDbFullSubentPath edgeEntPath2;
  if (entId2.objectClass() != AcDbPoint::desc())
  {
   if ((es = ADNAssocSampleUtils
    ::getClosestEdgeSubEntPath
    (entId2, ptEnt2, edgeEntPath2)) != Acad::eOk)
    return  es;
   aPaths.append(edgeEntPath2); 
  }
     AcDbFullSubentPath vertEntPath2;
  AcGePoint3d vertexPos2;
  if ((es = ADNAssocSampleUtils
   ::getClosestVertexInfo
   (entId2, edgeEntPath2, ptEnt2, vertexPos2, 
   vertEntPath2)) != Acad::eOk)
   return  es;
  aVertexPaths.append(vertEntPath2);
    if (entId2.objectClass() == AcDbPoint::desc())
  {
   aPaths.append(vertEntPath2); 
  }
     AcArray<AcConstrainedGeometry*> pConsGeoms;
  if ((es = ADNAssocSampleUtils
   ::addConstrainedGeometry(aPaths, 
   pConsGeoms)) != Acad::eOk)
   return  es;
    es = ADNAssocSampleUtils
   ::addGeomConstraint
   (AcGeomConstraint::kCoincident, aVertexPaths);
     return  es;
 }
     Acad::ErrorStatus ADNAssocSampleUtils
  ::getClosestVertexInfo(
  const  AcDbObjectId& entId, 
  const  AcDbFullSubentPath& edgeSubentPath, 
  const  AcGePoint3d& pt, 
  AcGePoint3d& closestVertexPos,
  AcDbFullSubentPath& closestVertexSubentPath)
 {
  Acad::ErrorStatus es;
    AcDbSmartObjectPointer <AcDbEntity> 
   pEntity(entId, AcDb::kForRead);
    if ((es = pEntity.openStatus()) != Acad::eOk )
   return  es;
    if (pEntity->isKindOf(AcDbBlockReference::desc()))
  {
   return  ADNAssocSampleUtils
    ::getClosestVertexInfoBref(entId, 
    edgeSubentPath, 
    pt, 
    closestVertexPos, 
    closestVertexSubentPath);
  }
    AcDbAssocPersSubentIdPE* const  pAssocPersSubentIdPE = 
   AcDbAssocPersSubentIdPE::cast
   (pEntity->queryX(AcDbAssocPersSubentIdPE::desc()));
    AcArray<AcDbSubentId> vertexSubentIds;
     if  (pEntity->isKindOf(AcDbSpline::desc()))
  {
   AcDbSubentId startVertexSubentId;
   AcDbSubentId endVertexSubentId;
     AcArray<AcDbSubentId> controlPointSubentIds;
   AcArray<AcDbSubentId> fitPointSubentIds;
     if ((es = 
    pAssocPersSubentIdPE->getSplineEdgeVertexSubentities
    (pEntity,
    AcDbSubentId(),
    startVertexSubentId,
    endVertexSubentId,
    controlPointSubentIds,
    fitPointSubentIds)) != Acad::eOk)
    return  es;
       vertexSubentIds.append(startVertexSubentId);
   vertexSubentIds.append(endVertexSubentId);
   vertexSubentIds.append(controlPointSubentIds);
  }
  else  if  (pEntity->isKindOf(AcDbPoint::desc()))
  {
   AcArray<AcDbSubentId> vertexSubentIds;
   es = pAssocPersSubentIdPE->getAllSubentities
    (pEntity, AcDb::kVertexSubentType, vertexSubentIds);
   if  (vertexSubentIds.length() > 0)
   {
    closestVertexSubentPath 
    = AcDbFullSubentPath(entId, vertexSubentIds[0]);
    return  es;
   }
  }
  else 
  { 
   AcDbSubentId startVertexSubentId;
   AcDbSubentId endVertexSubentId;
       if ((es = pAssocPersSubentIdPE->getEdgeVertexSubentities
    (pEntity,
    edgeSubentPath.subentId(),
    startVertexSubentId,
    endVertexSubentId,
    vertexSubentIds)) != Acad::eOk)
    return  es;
     vertexSubentIds.append(startVertexSubentId);
   vertexSubentIds.append(endVertexSubentId);
  }
    double  minDist = -1.0;
    AcDbSubentId closestId;
    for (int  i=0; i<vertexSubentIds.length(); ++i)
  {
   AcGePoint3d vertexPos;
     if  ((es = pAssocPersSubentIdPE->
    getVertexSubentityGeometry(pEntity, 
    vertexSubentIds[i],
    vertexPos)) != eOk)
    return  es;
     double  dist = vertexPos.distanceTo(pt);
     if (minDist < 0 || dist < minDist)
   {
    minDist = dist;
      closestId = vertexSubentIds[i];
      closestVertexPos = vertexPos;
   }
  }
    closestVertexSubentPath 
   = AcDbFullSubentPath(entId, closestId);
    return  es;
 }

## 评论

**内容**: Carl said...
I know this was ~5 years ago, but I think this is what I am looking for. I want to constrain a point to the intersection of two polylines even if the polylines move. How do I utilize this coding to let me constraint a point?
Reply
03/11/2020 at 12:19 PM

---
