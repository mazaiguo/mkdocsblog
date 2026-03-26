---
title: "Use AcDbField::getFieldCode() to get the field codes used in MText"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Unicode
description: "I need to get the Field Codes from MText entities. I tried using AcDbMText::explodeFragments() and AcDbMText::contents() but these functions return..."
author: Autodesk
---
# Use AcDbField::getFieldCode() to get the field codes used in MText

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/use-acdbfieldgetfieldcode-to-get-the-field-codes-used-in-mtext.html

## 文章内容

By Philippe Leefsma
Q:
I need to get the Field Codes from MText entities. I tried using AcDbMText::explodeFragments() and AcDbMText::contents() but these functions return the value of the evaluated text.  Is there a way to get the control codes?
A:
The AcDbObject::getField() function with AcDbField::getFieldCode() provide a means to get the FieldCodes used in MText.
This example iterates through model space and displays the FieldCode of MText entities:
void AdnGetFieldCodes()
{
        AcDbDatabase * pDb =
            acdbHostApplicationServices()->workingDatabase();
        AcDbBlockTable * blkTbl;
           pDb->getBlockTable(blkTbl, AcDb::kForRead);
        AcDbBlockTableRecord * blkTblRec;
        AcDbObjectId * pObjId;
           blkTbl->getAt(ACDB_MODEL_SPACE, blkTblRec, AcDb::kForRead);
        blkTbl->close();
           AcDbBlockTableRecordIterator* pIterator;
        if (blkTblRec->newIterator(pIterator) == Acad::eOk)
        {
                AcDbEntity* pEntity;
                while (!pIterator->done())
                {
                     pIterator->getEntity(pEntity, AcDb::kForRead);
                       if (pEntity->isA() == AcDbMText::desc())
                     {
                         AcDbMText *pt = (AcDbMText *) pEntity;
                         AcDbField * pField;
                         const ACHAR* pFcode = L"TEXT";
                               Acad::ErrorStatus es =
                             pt->getField(pFcode, pField, AcDb::kForRead);
                           if (es != Acad::eOk)
                         {
                             acutPrintf(L"\n%s", acadErrorStatusText(es));
                             pIterator->step();
                             continue;
                         }
                           ACHAR* pszFieldCode;
                         pField->getFieldCode(
                             pszFieldCode,
                             AcDbField::kAddMarkers);
                               acutPrintf(L"\n%s",pszFieldCode);
                         delete pszFieldCode;
                                  pField->close();
                     }
                       pEntity->close();
                     pIterator->step();
                }
        }
          delete pIterator;
        blkTblRec->close();
}

