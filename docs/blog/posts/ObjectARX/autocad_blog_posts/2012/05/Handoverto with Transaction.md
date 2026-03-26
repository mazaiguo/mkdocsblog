---
title: "Handoverto with Transaction"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Unicode
description: "If you try to handover the object id of a Transaction resident object with a new object, you will receive an error eInvalidContext. In fact, you ca..."
author: Autodesk
---
# Handoverto with Transaction

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/handoverto-with-transaction.html

## 文章内容

By Xiaodong Liang
If you try to handover the object id of a Transaction resident object with a new object, you will receive an error eInvalidContext. In fact, you cannot call the function handOverTo() on Transaction resident objects. This means that you have to switch to common way to open the object (acdbOpenObject).  This also applies to .NET.
bool test()
{
     ads_name ename;
     ads_point ptResult;
     ads_matrix adsmat;
     struct resbuf *info;
   // select one entity
     int rt = acedNEntSelP(_T("\nselect an entity:"),
         ename,
         ptResult,
         false ,
         adsmat,
         &info);
     if( rt!= RTNORM)
     {
         acutPrintf(_T("\nFailure in acedNEntSelP"));
        return false;
      }
        AcDbObjectId old__ent_id;
      acdbGetObjectId(old__ent_id,ename);
         AcDbCircle* newCircle =
          new AcDbCircle(
          AcGePoint3d(0,0,0),
          AcGeVector3d(0,0,1),
          10);
        // correct usage
       AcDbObject *pObj;
      Acad::ErrorStatus es1 =
          acdbOpenObject(pObj,old__ent_id,AcDb::kForWrite);
         if (pObj == NULL)
         return false;
        Acad::ErrorStatus es =
          pObj->handOverTo(newCircle);
     if (es ==
         Acad::eObjectToBeDeleted)
     {
         newCircle->close();
        delete pObj;
        return true;
     }
     else
    {
         pObj->close();
       return false;
     } 
      // wrong usage: with Transaction
      /* AcTransaction *pTrans =
          actrTransactionManager->startTransaction();
      AcDbObject *pObj;
      pTrans->getObject(pObj,
          old__ent_id,
          AcDb::kForWrite);
        if (pObj == NULL)
         return false;
        // will get eInvalidContext
      Acad::ErrorStatus es =
          pObj->handOverTo(newCircle);
     if (es ==
         Acad::eObjectToBeDeleted)
     {
        delete pObj;
        actrTransactionManager->endTransaction();
        return true;
     }
     else
    {
       actrTransactionManager->abortTransaction();
       return false;
     }
     */
}

