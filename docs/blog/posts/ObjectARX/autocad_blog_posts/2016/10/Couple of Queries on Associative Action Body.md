---
title: "Couple of Queries on Associative Action Body"
date: 2016-10-01
categories:
  - AutoCAD
tags:
  - Selection
description: "It’s been long time since I hit to blogging, I was occupied with some other personal work."
author: Autodesk
---
# Couple of Queries on Associative Action Body

发布日期: 2016-10-01

原始链接: https://adndevblog.typepad.com/autocad/2016/10/couple-of-queries-on-associative-action-body.html

## 文章内容

By Madhukar Moogala
It’s been long time since I hit to blogging, I was occupied with some other personal work.
I have received few queries on Action Body last week, in the best interest of the community I planned to blog it.
How to find out if an object has any associated action bodies ?
There is static method AcDbAssocActionBody::getActionBodiesOnObject(), here is example code of it.
void getParticipantInAction()
{
    ads_name selectionSet;
  if (acedSSGet(nullptr, nullptr, nullptr, nullptr, selectionSet) != RTNORM)
    return;
  SelectionSetFreeer freeer(selectionSet);
  ads_name ent;
  if (!VERIFY(acedSSName(selectionSet, 0, ent) == RTNORM))
    return;
  AcDbObjectId entityId;
  if(!eOkVerify(acdbGetObjectId(entityId, ent))) return;
    AcDbObjectPointer<AcDbEntity> pEntity(entityId, AcDb::kForRead);
  if (!eOkVerify(pEntity.openStatus()))
    return; // This should never happen
    /*. find out if an object has any associated action bodies? */
  AcDbObjectIdArray pReadWriteActionBodyIds;
  AcDbObjectId     pWriteOnlyActionBodyId;
    AcDbAssocActionBody::getActionBodiesOnObject(pEntity, true, true, &pWriteOnlyActionBodyId, &pReadWriteActionBodyIds);
    if (!pWriteOnlyActionBodyId.isNull()) {
    acutPrintf(_T("\n%s"), pWriteOnlyActionBodyId.objectClass()->name());
      }
  if (!pReadWriteActionBodyIds.isEmpty())
  {
    for (int i = 0; i < pReadWriteActionBodyIds.length(); i++)
      acutPrintf(_T("\n%s"),pReadWriteActionBodyIds[i].objectClass()->name());
      }
}
    How can I determine which object(s) was/were changed that caused the action body to be triggered ?
AcDbAssocActionBody::getDependencies() returns dependencies that the action owns. If AcDbAssocDependency::status() is kUpToDateAssocStatus, it means the object the dependency depends on hasn’t changed. If it is something else (see AcDbAssocStatus enum), it means that the object the action depends on changed and the action is scheduled to re-evaluate.
Notice that when the object is changed directly, e.g. by user interaction, the dependency status immediately changes to kChangedDirectlyAssocStatus. The kChangedTransitivelyAssocStatus and kChangedNoDifferenceAssocStatus are only set later, during network re-evaluation, when the system calculates transitive closure of all actions that will need to re-evaluate. At the time AcDbAssocActionBody::evaluateOverride() is called, the status of all dependencies has already been set.
Here is small example code get an idea:
void AddOrRemoveCallBack()
{
  if (isAdded)
  {
    AcDbAssocManager::addGlobalEvaluationCallback(&customEvaluationCallback::instance(), 0);
    isAdded = false;
  }
  else
  {
    AcDbAssocManager::removeGlobalEvaluationCallback(&customEvaluationCallback::instance());
    isAdded = true;
  }
  }
class customEvaluationCallback: public AcDbAssocEvaluationCallback
{
  public:
  virtual void beginActionEvaluation(AcDbAssocAction* pAction) {};
    virtual void endActionEvaluation(AcDbAssocAction* pAction) {};
      virtual void setActionEvaluationErrorStatus(AcDbAssocAction*    pAction,
    Acad::ErrorStatus   errorStatus,
    const AcDbObjectId& objectId,
    AcDbObject*         pObject,
    void*               pErrorInfo) {};
      virtual void
    beginActionEvaluationUsingObject(AcDbAssocAction*    pAction,
                                     const AcDbObjectId& objectId,
                                     bool                objectIsGoingToBeUsed,
                                     bool                objectIsGoingToBeModified,
                                     AcDbObject*&        pSubstituteObject)
  {
      acutPrintf(_T("\n Action That is not in Sync and Object that is going to modified: \t%s,\t%s"), objectId.objectClass()->name(), HandleStr(objectId));
    AcDbObjectIdArray dependencyIds;
    AcDbObjectPointer<AcDbAssocActionBody> pBody(pAction->actionBody(), AcDb::kForRead);
    if (!eOkVerify(pBody.openStatus()))
      return;
    pBody->getDependencies(true, true, dependencyIds);
    for (int i = 0; i < dependencyIds.length(); i++)
    {
      AcDbObjectPointer<AcDbAssocDependency> pDeps(dependencyIds[i], AcDb::kForRead);
      if (!eOkVerify(pDeps.openStatus()))
        return;
      AcDbAssocStatus status = pDeps->status();
      if (status != kIsUpToDateAssocStatus)
      {
          acutPrintf(_T("\n Dependent Object That is not in Sync: \t%s,\t%s"), pDeps->dependentOnObject().objectClass()->name(), HandleStr(pDeps->dependentOnObject()));
      }
      else
        continue;
      }
  }
    virtual void endActionEvaluationUsingObject(AcDbAssocAction*    pAction,
    const AcDbObjectId& objectId,
    AcDbObject*         pObject) {};
        virtual bool cancelActionEvaluation() { return false; }
  /*To avoid creating instance */
  static customEvaluationCallback& instance();
};
  customEvaluationCallback& customEvaluationCallback::instance()
{
    static customEvaluationCallback mSelf;
    return mSelf;
}
  Custom Commands to call above routines:
acedRegCmds->addCommand(L"ASSOCFILLETSAMPLE", L"GPA", L"GPA", ACRX_CMD_MODAL, getParticipantInAction);
acedRegCmds->addCommand(L"ASSOCFILLETSAMPLE", L"AOR", L"AOR", ACRX_CMD_MODAL, AddOrRemoveCallBack);
Here is working gif:
via GIPHY

## 评论

**内容**: octordle said...
I find this blog awesome for all member, especially newbie as me
Reply
09/19/2022 at 06:40 PM

---
