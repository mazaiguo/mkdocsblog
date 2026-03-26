---
title: "Associative Framework: How to delete constraints applied to a specific entity?"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Using the Associative framework is not a straightforward task. Some of the components, such as constraints applied to one entity can be buried insi..."
author: Autodesk
---
# Associative Framework: How to delete constraints applied to a specific entity?

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/associative-framework-how-to-delete-constraints-applied-to-a-specific-entity.html

## 文章内容

By Philippe Leefsma
Using the Associative framework is not a straightforward task. Some of the components, such as constraints applied to one entity can be buried inside the framework.
The following examples illustrates how to delete all constraints applied to a specific entity and also deleting only some specific constraint types.
  Here is how to delete all constraints applied to a given entity. There are several ways to get this done, but if you want to get rid of all constraints on an entity at once, the most direct way is as follow:
Acad::ErrorStatus deleteAllConstraintsOnEntity(const AcDbObjectId& entityId)
{
        Acad::ErrorStatus es;
          AcDbObjectPointer  pEntity(entityId, AcDb::kForWrite);
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
             AcDbObjectPointer constraintGroup(actionIds[i], AcDb::kForWrite);
               if(constraintGroup.openStatus() != Acad::eOk)
                 continue;
                             for(int j = 0; j < dependencyIds.length(); ++j)
             {
                if((es = constraintGroup->deleteConstrainedGeometry(
                    dependencyIds[j])) != Acad::eOk)
                {
                        acutPrintf(
                         L"\nFailed to delete constrained geometry...");
                }
             }
        }
          return es;     
}
-
The second example illustrates how to delete fix constraints applied to a line. In that case we need to access the constrained points of the constrained curve, because this is on them that the fix constraint is applied:
  Acad::ErrorStatus deleteConstraintsOnEntity(
        const AcDbObjectId& entityId,
        const AcRxClass* constraintDesc)
{
        Acad::ErrorStatus es;
          AcDbObjectPointer  pEntity(entityId, AcDb::kForWrite);
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
                AcDbObjectPointer constraintGroup(
                    actionIds[i], AcDb::kForWrite);
                  if(constraintGroup.openStatus() != Acad::eOk)
                        continue;
                                for(int j = 0; j < dependencyIds.length(); ++j)
                {
                        AcDbObjectPointer geomDependency(
                            dependencyIds[j], AcDb::kForRead);
                          if(geomDependency.openStatus() != Acad::eOk)
                                continue;
                                                AcConstrainedGeometry* pConsGeom = NULL;
                        if((es = constraintGroup->getConstrainedGeometry(
                                geomDependency, pConsGeom)) != Acad::eOk)
                        {
                                acutPrintf(
                                 L"\nFailed to get constrained geometry...");
                                continue;
                        }
                          if(pConsGeom->isKindOf(AcConstrainedCurve::desc()))
                        {
                                AcConstrainedCurve* pConsCurve =
                                    AcConstrainedCurve::cast(pConsGeom);
                                  AcArray apImplicitPoints;
                                pConsCurve->getConstrainedImplicitPoints(
                                    apImplicitPoints);
                                  for(int k= 0; k<apImplicitPoints.length(); ++k)
                                {
                                   AcArray apConstraints;
                                   if((es = apImplicitPoints[k]->
                                      getConnectedConstraints(
                                        apConstraints)) != Acad::eOk)
                                        {
                                           acutPrintf(
                                    L"\nFailed to get connected constraints...");
                                                continue;
                                        }
                                      for(int l=0;l<apConstraints.length(); ++l){
                                                                      if(apConstraints[l]->isA()==constraintDesc)
                                    {
                                      if((es=constraintGroup->deleteConstraint(
                                        apConstraints[l])) != Acad::eOk)
                                        {
                                         acutPrintf(
                                          L"\nFailed to delete constraint...");
                                        }
                                    }
                                 }
                            }
                        }
                }
        }
          return es;     
}
  static void ADSConstraintModeling_DeleteEntConstr(void)
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
        //es = deleteAllConstraintsOnEntity((id);
        es = deleteConstraintsOnEntity(id, AcFixedConstraint ::desc());
}

## 评论

**内容**: Matthias said...
Hi Philippe,
any chance to extend your awesome ADNAssocConstraintAPI with that functions?
Regards Matthias (sorry for being anonymous, I couldn't sign in)
Reply
11/12/2013 at 01:30 AM

---
**内容**: Philippe said...
Hi Matthias, hope you are doing well, I will take a look at that once AU is over, too much things at the moment...
Cheers,
Philippe.
Reply
11/13/2013 at 12:06 AM

---
