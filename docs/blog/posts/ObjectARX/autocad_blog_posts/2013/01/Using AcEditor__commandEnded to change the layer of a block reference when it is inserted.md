---
title: "Using AcEditor::commandEnded to change the layer of a block reference when it is inserted"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Block
  - Layer
  - Selection
description: "When a BlockReference is created with the INSERT command, I would like to change the layer it is on. Is there a way to do this?"
author: Autodesk
---
# Using AcEditor::commandEnded to change the layer of a block reference when it is inserted

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/using-aceditorcommandended-to-change-the-layer-of-a-block-reference-when-it-is-inserted.html

## 文章内容

By Philippe Leefsma
Q:
When a BlockReference is created with the INSERT command, I would like to change the layer it is on. Is there a way to do this?
A:
One approach to consider is to use AcEditor::commandEnded: If the command was INSERT, then a selection set is used to get the last entity added to the drawing. A transaction is used to open the entity and change the layer. The attached example does this.
Here is the pertinent code:
  void ASDKwbEdReactor::commandEnded(
const ACHAR * cmdStr)
{
     if(_tcscmp(cmdStr,_T("INSERT")) == 0)
     {
          if (!acdbHostApplicationServices()
              ->workingDatabase())
                return;
             // Get entities just operated on
           ads_name sset;
           int err = acedSSGet(_T("L"),
           NULL, NULL, NULL, sset);
             if (err != RTNORM)
           {
              acutPrintf(
                _T("\nError acquiring last entity"));
                return;
           }
             actrTransactionManager->startTransaction();
             long length;
           acedSSLength(sset, &length);
             ads_name en;
           AcDbObjectId eId;
           AcDbEntity *pEnt;
             for (long i=0; i < length; i++)
           {
                acedSSName(sset, i, en);
                  Acad::ErrorStatus es =
                    acdbGetObjectId(eId, en);
                  if (es != Acad::eOk)
                {
                  acutPrintf(
                   _T("\nacdbGetObjectId failed: ")
                   _T("Entity <%lx,%lx>, error %s."),
               en[0], en[1],
                   acadErrorStatusText(es));
                       acedSSFree(sset);
                     return;
                }
                 es = actrTransactionManager->getObject(
                                    (AcDbObject*&)pEnt,
                    eId, AcDb::kForWrite);
                  if (es == Acad::eOk)
                {
                  // This maybe a redundant test as
                  // INSERT was the command
                     if ( pEnt->isA() ==
                         AcDbBlockReference::desc() )
                     {
                           // You need to have an
                           // existing TEST layer
                           pEnt->setLayer(_T("TEST"));
                     }
                }
                else
                {
                     acutPrintf(
                       _T("\ngetObject failed: %s."),
                       acadErrorStatusText(es));
                       actrTransactionManager->
                        abortTransaction();
                     acedSSFree(sset);
                     return;
                }
           }
             actrTransactionManager->endTransaction();
           acedSSFree(sset);
     }
}
  EdReactorDemo.zip

