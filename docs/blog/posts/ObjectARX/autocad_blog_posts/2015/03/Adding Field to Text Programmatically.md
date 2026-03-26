---
title: "Adding Field to Text Programmatically"
date: 2015-03-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - Plugin
  - Unicode
description: "We will see in this blog how can we set the contents of a AcDbText entity to a field linking to contents of another AcDbText."
author: Autodesk
---
# Adding Field to Text Programmatically

发布日期: 2015-03-01

原始链接: https://adndevblog.typepad.com/autocad/2015/03/adding-field-to-text-programmatically.html

## 文章内容

By Madhukar Moogala
We will see in this blog how can we set the contents of a AcDbText entity to a field linking to contents of another AcDbText.
Two APIs to be noted here,
AcFdMakeFieldCode, formats an object property field code using the specified components.
acdbEvaluateFields,evaluates all the fields in the objects in the database, similar to UpdateFields in the UI.
CString sPrompt(_T("\nSelect entity: "));
ads_name  an;
ads_point ap;
int nReturn = acedEntSel(sPrompt, an, ap);
// Canceled or nothing selected
if (nReturn == RTCAN)
{
return;
}
  // Convert ads name to object id
AcDbObjectId id;
acdbGetObjectId(id, an);
  AcTransaction* pTrans = acdbTransactionManager->startTransaction();
if (NULL == pTrans)
{
return;
}
  AcDbText* pExistingText = NULL;
Acad::ErrorStatus es = acdbTransactionManager->getObject((AcDbObject*&)pExistingText, id, AcDb::kForRead);
if (!eOkVerify(es))
{
acdbTransactionManager->abortTransaction();
acedPrompt(_T("\nNot a text"));
return;
}
  AcDbText* pText = new AcDbText();
pText->setPosition(
AcGePoint3d(pExistingText->position().x,
pExistingText->position().y+20.00,
pExistingText->position().z));
ads_name objName;
acdbGetAdsName(objName, id);
    ACHAR* strField;
AcFdMakeFieldCode(id,(AcDbEvalNodeId)0,
                    _T("TextString"),
                    AcFdEval::kObjFieldNone,
                    _T(""),
                    (AcHyperlink*)NULL,
                    (ACHAR*&)strField);
pText->setTextString(strField);
  AcDbBlockTableRecord* pModelSpace = NULL;
es = acdbTransactionManager->getObject((AcDbObject*&)pModelSpace,
acdbSymUtil()->blockModelSpaceId(
acdbHostApplicationServices()->workingDatabase()),
AcDb::kForWrite);
  if (!eOkVerify(es))
{
acdbTransactionManager->abortTransaction();
acedPrompt(_T("\nCannot open model space."));
return;
}
  AcDbObjectId outId;
es = pModelSpace->appendAcDbEntity(outId, pText);
if (!eOkVerify(es))
{
acdbTransactionManager->abortTransaction();
acedPrompt(_T("\nCannot append new entity."));
return;
}
pText->close();
/*Update Fields*/
es = acdbEvaluateFields(outId,
AcDbField::kRegen,
NULL,
acdbHostApplicationServices()->workingDatabase(),
AcFd::kEvalRecursive);
if(!eOkVerify(es))
{
CString esText = acadErrorStatusText(es);
esText = esText + _T(": Failed to Evalute");
acedAlert(esText);
}
/*Clean Up*/
acutDelString(strField);
acdbTransactionManager->endTransaction();

## 评论

**内容**: petcon said...
%<\AcObjProp Object(%<\_ObjId 8796087803088>%).Parameter(0).TextString>%
after AcFdMakeFieldCode，strField becomes to %<\AcObjProp Object(%<\_ObjId 8796087803088>%).Parameter(0).TextString>%
i think there is error about .Parameter(0). i think the correct strField is %<\AcObjProp Object(%<\_ObjId 8796087803088>%).TextString>%
Reply
07/19/2022 at 09:35 PM

---
