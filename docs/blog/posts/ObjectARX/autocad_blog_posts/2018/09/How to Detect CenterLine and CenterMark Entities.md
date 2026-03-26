---
title: "How to Detect CenterLine and CenterMark Entities"
date: 2018-09-01
categories:
  - AutoCAD COM
tags:
  - API
  - AutoCAD
  - Block
  - COM
description: "CenterLine and CenterMark are two new entities based on AcDbBlockReferenes introduced in AutoCAD 2017, they are basically unnamed blockreference ca..."
author: Autodesk
---
# How to Detect CenterLine and CenterMark Entities

发布日期: 2018-09-01

原始链接: https://adndevblog.typepad.com/autocad/2018/09/how-to-detect-centerline-and-centermark-entities.html

## 文章内容

By Madhukar Moogala

CenterLine and CenterMark are two new entities based on AcDbBlockReferenes introduced in AutoCAD 2017, they are basically unnamed blockreference catering different purpose.
For more information on these two entities – CenterLine & CenterMark
In this post we will look at how to identifying if the underlying entities is a CenterLine or CenterMark objects, unfortunately there isn’t a public API to get to know what is the type of the Entity.
However through using Non-Com property system we can figure out if the entity is whether a CenterLine or CenterMark.

void testIt() {
       
       ads_name ename;
       ads_point pt;
       AcDbObjectId objId = AcDbObjectId::kNull;
       AcDbEntity* pEnt = nullptr;
       if (RTNORM != acedEntSel(_T(""), ename, pt)) return; 
       if (!eOkVerify(acdbGetObjectId(objId, ename))) return;
       if (!eOkVerify(acdbOpenAcDbEntity(pEnt, objId, AcDb::kForRead))) return;
       isCenterLineOrNot(pEnt);
       
}
Utils
void getAttInfo(const AcRxAttribute * att,
const AcRxObject * member, 
AcString & attInfo)
{
       if (att->isA() == AcRxCOMAttribute::desc())
       {
             AcRxCOMAttribute * a = AcRxCOMAttribute::cast(att);
             attInfo.format(_T("\n%s - %s"), att->isA()->name(), a->name());
       }
       else if (att->isA() == AcRxUiPlacementAttribute::desc())
       {
             AcRxUiPlacementAttribute* a = AcRxUiPlacementAttribute::cast(att);
             attInfo.format(
                    _T("\n%s - %s - %f"),
                    att->isA()->name(),
                    a->getCategory(member),
                    a->getWeight(member));
       }
       else
       {
             if (att->isA() != nullptr)
             {
                    attInfo.format(_T("\n%s"),
      att->isA()->name());
             }
       }
}
 
void printValues(AcRxObject * entity, 
const AcRxMember * member, 
Adesk::Boolean& isCenterLine)
{
       Acad::ErrorStatus err = Acad::eOk;
 
       AcString strValue;
       AcRxProperty * prop = AcRxProperty::cast(member);
       if (prop != NULL)
       {
             AcRxValue value;
 
             if ((err = prop->getValue(entity, value)) == Acad::eOk)
             {
                    ACHAR * szValue = NULL;
 
                    int buffSize = value.toString(NULL, 0);
                    if (buffSize > 0)
                    {
                           buffSize++;
                           szValue = new ACHAR[buffSize];
                           value.toString(szValue, buffSize);
                    }
 
                    
                    strValue.format(_T("%s = %s"),
      value.type().name(),
      (szValue == NULL) ? _T("none") : szValue);
 
                    if (szValue)
                           delete szValue;
             }
             else
             {
                    strValue.format(_T("Error Code = %d"), err);
             }
       }
 
       AcString str;
       str.format(_T("\n%s - %s [%s]"), member->isA()->name(),
    member->name(), strValue.kACharPtr());
       AcString memberName;
       memberName.format(_T("%s"), member->name());
       if (0 == memberName.collateNoCase(_T("IsCenterLine")))
       {
             AcString isTrue(strValue.kACharPtr());
             if (isTrue.find(_T("1")) > 0) {
                    isCenterLine = Adesk::kTrue;
             }
 
       }
       acutPrintf(str);
 
       const AcRxAttributeCollection & atts = member->attributes();
 
       for (int i = 0; i < atts.count(); i++)
       {
             const AcRxAttribute * att = atts.getAt(i);
             AcString attInfo;
             getAttInfo(att, member, attInfo);
             acutPrintf(attInfo);
       }
       
       if (member->children() != NULL)
       {
             for (int i = 0; i < member->children()->length(); i++)
             {
                    const AcRxMember * subMember = 
                    member->children()->at(i);
                    printValues(entity, subMember, isCenterLine);
             }
       }
}
Adesk::Boolean isCenterLineOrNot(AcDbEntity* pEnt)
{
       AcRxMemberIterator * iter = 
       AcRxMemberQueryEngine::theEngine()->newMemberIterator(pEnt);
       Adesk::Boolean isCenterLine = Adesk::kFalse;
       for (; !iter->done(); iter->next())
       {
             printValues(pEnt, iter->current(), isCenterLine);
       }
       return isCenterLine;
}
Update:
Thanks to Engineering Colleague Huyau Liu for this tip
enum CenterType
{
 CenterMark = 0,
 CenterLine
};
AcString SmartCenters[] = { L"CenterMark", L"CenterLine" };

Acad::ErrorStatus getTypeOfSmartCenterObject(const AcDbObjectId& blockRefObjId , CenterType& type)
{
 AcDbSmartObjectPointer pCenter(blockRefObjId, AcDb::kForRead, true);
 if (pCenter.openStatus() != Acad::eOk)
  return Acad::eNullEntityPointer;

 AcDbObjectIdArray actionIds;
 Acad::ErrorStatus err = AcDbAssocAction::getActionsDependentOnObject(pCenter, false, true, actionIds);
 if (!eOkVerify(err))
  return err;

 for (int i = 0; i < actionIds.length(); i++)
 {
  AcDbObjectId actionBody = AcDbAssocAction::actionBody(actionIds[i]);
  auto objClass = actionBody.objectClass();
  AcString objClassName = objClass->name();

  if (objClassName == L"AcDbCenterMarkActionBody") {
   type = CenterType::CenterMark; 
   return Acad::eOk;
  }
  else if (objClassName == L"AcDbCenterLineActionBody") {
   type = CenterType::CenterLine;
   return Acad::eOk;
  }
  else;
 }

 return Acad::eNotApplicable;

}
  CenterType type;
  if (eOkVerify(getTypeOfSmartCenterObject(objId, type)))
  {
   acutPrintf(_T("CenterType : %s"), SmartCenters[type].kACharPtr());
  }  
.NET Port courtesy Alexander Rivilis, Thank you :)
public void TestCenter()
{
Document doc = Application.DocumentManager.MdiActiveDocument;
if (doc == null) return;
Editor ed = doc.Editor;
Database db = doc.Database;
PromptEntityOptions prOpt = new PromptEntityOptions("Select block: ");
prOpt.SetRejectMessage("Not a block!");
prOpt.AddAllowedClass(typeof(BlockReference), true);
PromptEntityResult prRes = ed.GetEntity(prOpt);
if (prRes.Status != PromptStatus.OK) return;
using (Transaction tr = doc.TransactionManager.StartTransaction())
{
    var br = 
    tr.GetObject(prRes.ObjectId, OpenMode.ForRead) as BlockReference;
    try
    {
        var idCols = AssocAction.GetActionsDependentOnObject(br, false, true);
        if (idCols.Count > 0)
        {
            foreach (ObjectId id in idCols)
            {
                ObjectId idAct = AssocAction.GetActionBody(id);
                if (idAct.ObjectClass.Name == "AcDbCenterMarkActionBody")
                {
                    ed.WriteMessage("\nIt is CenterMark");
                    break;
                }
                if (idAct.ObjectClass.Name == "AcDbCenterLineActionBody")
                { 
                    ed.WriteMessage("\nIt is CenterLine");
                    break;
                }
            }
        }
    }
    catch { };
    tr.Commit();
}

}

## 评论

**内容**: Alexander Rivlis said...
Thanks for sharing this code! And personal thanks to Huyau Liu!
Reply
09/11/2018 at 04:03 AM

---
