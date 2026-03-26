---
title: "Associative Framework: How to retrieve all constraints in database or applied to a specific entity?"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Database
description: "The following examples illustrate how to dive into the Associative Framework in order to retrieve existing constraints. In a database, constraints ..."
author: Autodesk
---
# Associative Framework: How to retrieve all constraints in database or applied to a specific entity?

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/associative-framework-how-to-retrieve-all-constraints-in-database-or-applied-to-a-specific-entity.html

## 文章内容

By Philippe Leefsma
The following examples illustrate how to dive into the Associative Framework in order to retrieve existing constraints. In a database, constraints are contained inside an AcDbAssoc2dConstraintGroup. So the most direct way to list all constraints is to iterate through each group and retrieve its owned constraints
This first example illustrates that principle:
////////////////////////////////////////////////////////////////////////////////////
// Use: AcDbDatabase* pDb = acdbHostApplicationServices()->workingDatabase();
//  AcDbObjectId spaceId = pDb->currentSpaceId();
//  es = dumpConstraints(spaceId);
////////////////////////////////////////////////////////////////////////////////////
Acad::ErrorStatus dumpConstraints(const AcDbObjectId& spaceId)
{
 Acad::ErrorStatus es;
   AcDbObjectId networkId = AcDbAssocNetwork::getInstanceFromObject(spaceId, true);
   if (networkId.isNull())
 {
  return Acad::eNullObjectId;
 }
   AcDbObjectPointer pNetwork(networkId, kForRead);
   if (pNetwork.openStatus() != Acad::eOk)
 {
  return Acad::eNullObjectId;
 }
   const AcDbObjectIdArray& actionsInNetwork = pNetwork->getActions();
   for (int nCount = 0; nCount < actionsInNetwork.length(); ++nCount)
 {
    const AcDbObjectId& idAction = actionsInNetwork[nCount];
    if (idAction == AcDbObjectId::kNull)
   continue;
    if ( actionsInNetwork[nCount].objectClass() == NULL ||
    !actionsInNetwork[nCount].objectClass()->isDerivedFrom(
                AcDbAssoc2dConstraintGroup::desc()))
   continue;
    AcDbObjectPointer pAction(idAction, kForRead);
    if (pAction.openStatus() != Acad::eOk)
   continue;
    const AcDbAssoc2dConstraintGroup* const pConstGrp =
   static_cast(pAction.object());
    if (!pConstGrp)
   continue;
    acutPrintf(L"\n");
    AcArray apConstraints;
  if((es = pConstGrp->getConstraints(apConstraints)) != Acad::eOk)
  {
   acutPrintf(L"\nFailed to get constraints for group...");
   continue;
  }
    for(int i = 0; i < apConstraints.length(); ++i)
  {
   acutPrintf(L"\n - Constraint: %s", apConstraints[i]->isA()->name());
  }
 }
}
-
-
If you want to list all constraints applied to a specific entity, things are a bit more tricky:
Acad::ErrorStatus getConstraintsOnGeometry(
    const AcConstrainedGeometry* pConsGeom)
{
   Acad::ErrorStatus es;
   acutPrintf(L"\nConstrained Geometry: %s", pConsGeom->isA()->name());
   if(pConsGeom->isKindOf(AcConstrainedCurve::desc()))
 {
  AcConstrainedCurve* pConsCurve = AcConstrainedCurve::cast(pConsGeom);
    AcArray apImplicitPoints;
  pConsCurve->getConstrainedImplicitPoints(apImplicitPoints);
    for(int k = 0; k < apImplicitPoints.length(); ++k)
  {
     acutPrintf(L"\n", k);
     AcArray apConstraints;
   if((es = apImplicitPoints[k]->getConnectedConstraints(apConstraints))
       != Acad::eOk)
   {
    acutPrintf(L"\nFailed to get connected constraints...");
    continue;
   }
     for(int l = 0; l < apConstraints.length(); ++l)
   {
    acutPrintf(L"\n - Constraint: %s", apConstraints[l]->isA()->name());
   }
  }
 }
   if(pConsGeom->isKindOf(AcConstrainedPoint::desc()))
 {
    AcConstrainedPoint* pConsPoint = AcConstrainedPoint::cast(pConsGeom);
    AcArray apConstraints;
  if((es = pConsPoint->getConnectedConstraints(apConstraints)) != Acad::eOk)
  {
   acutPrintf(L"\nFailed to get connected constraints...");
   return es;
  }
    for(int l = 0; l < apConstraints.length(); ++l)
  {
   acutPrintf(L"\n - Constraint: %s", apConstraints[l]->isA()->name());
  }
 }
   if(pConsGeom->isKindOf(AcConstrainedRigidSet::desc()))
 {
    AcConstrainedRigidSet* pConsSet = AcConstrainedRigidSet::cast(pConsGeom);
    AcArray apConstraints;
  if((es = pConsSet->getConnectedConstraints(apConstraints)) != Acad::eOk)
  {
   acutPrintf(L"\nFailed to get connected constraints...");
   return es;
  }
    for(int l = 0; l < apConstraints.length(); ++l)
  {
   acutPrintf(L"\n - Constraint: %s", apConstraints[l]->isA()->name());
  }
    for(int k = 0; k < pConsSet->numOfConstrainedGeoms(); ++k)
  {
     AcConstrainedGeometry* pConsGeomAtIdx = pConsSet->getConstrainedGeomAt(k);
     //Recursive call...
   if((es = getConstraintsOnGeometry(pConsGeomAtIdx)) != Acad::eOk)
   {
    return es;
   }
  }
 }
   return es;
  }
    Acad::ErrorStatus getConstraintsOnEntity(const AcDbObjectId& entityId)
{
   Acad::ErrorStatus es;
   AcDbObjectPointer  pEntity(entityId, AcDb::kForRead);
   if((es = pEntity.openStatus()) != Acad::eOk)
  return es;
   AcDbObjectIdArray actionIds;
 if((es = AcDbAssocAction::getActionsDependentOnObject(
         pEntity, true, true, actionIds))!= Acad::eOk)
  return es;
   AcDbObjectIdArray dependencyIds;
 if((es = AcDbAssocDependency::getDependenciesOnObject(
         pEntity, true, true, dependencyIds))!= Acad::eOk)
  return es;
   for(int i = 0; i < actionIds.length(); ++i)
 {
  AcDbObjectPointer constraintGroup(actionIds[i], AcDb::kForRead);
  if(constraintGroup.openStatus() != Acad::eOk)
   continue;
    for(int j = 0; j < dependencyIds.length(); ++j)
  {
   AcDbObjectPointer geomDependency(dependencyIds[j], AcDb::kForRead);
   if(geomDependency.openStatus() != Acad::eOk)
    continue;
      AcConstrainedGeometry* pConsGeom = NULL;
   if((es = constraintGroup->getConstrainedGeometry(
           geomDependency, pConsGeom)) != Acad::eOk)
   {
    acutPrintf(L"\nFailed to get constrained geometry...");
    continue;
   }
   getConstraintsOnGeometry(pConsGeom);
  }
 }
   return es;
  }
  static void ADSConstraintModeling_ListEntConstr(void)
{
 Acad::ErrorStatus es;
 AcDbObjectId id;
 ads_name name;
 ads_point pt;
 if(acedEntSel(L"\nSelect Entity: ", name, pt) != RTNORM)
 {
  return;
 }
   acdbGetObjectId(id, name);
 es = getConstraintsOnEntity(id);
}

