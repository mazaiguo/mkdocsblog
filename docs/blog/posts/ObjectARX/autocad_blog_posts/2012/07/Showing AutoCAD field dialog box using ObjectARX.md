---
title: "Showing AutoCAD field dialog box using ObjectARX"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - ObjectARX
description: "You can show the AutoCAD field dialog box in your objectARX code using “AcFdUiInvokeFieldDialog” API. This API will show the dialog and return the ..."
author: Autodesk
---
# Showing AutoCAD field dialog box using ObjectARX

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/showing-autocad-field-dialog-box-using-objectarx.html

## 文章内容

By Virupaksha Aithal
You can show the AutoCAD field dialog box in your objectARX code using “AcFdUiInvokeFieldDialog” API. This API will show the dialog and return the user choice field object through its first parameter. Refer below code which shows the usage of API.
void addFieldWithDialog()
{
    AcGePoint3d pnt1;
       // pick start point
    if(acedGetPoint(NULL, L"\nPick Insertion point ",
                                        asDblArray(pnt1)) != RTNORM)
    {
        return;
    }
      AcDbDatabase *pDb =
      acdbHostApplicationServices()->workingDatabase();
      AcDbField *pField = NULL;
    Acad::ErrorStatus es;
      //show the dialog box..
    if(AcFdUiInvokeFieldDialog(pField, FALSE, pDb) == IDOK)
    {
        //open the model space for write
        AcDbObjectId modelId;
        modelId = acdbSymUtil()->blockModelSpaceId(pDb);
          AcDbBlockTableRecord *pBlockTableRecord;
        es = acdbOpenAcDbObject((AcDbObject*&)pBlockTableRecord,
                                        modelId, AcDb::kForWrite);
        //add a Mtext;
        AcDbMText *pMText = new AcDbMText();
        pMText->setLocation(pnt1);
        // Add to Db
        AcDbObjectId objectId;
        pBlockTableRecord->appendAcDbEntity(objectId, pMText);
          AcDbObjectId fieldId;
        //add a field
        es = pMText->setField(_T("TEXT"), pField, fieldId);
        es = pField->evaluate(AcDbField::kDemand, pDb); 
          pField->close();
        pMText->close();
        pBlockTableRecord->close();
      }
}

