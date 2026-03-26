---
title: "How to use Long transaction to mimic -refedit"
date: 2012-04-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - Block
  - C++
  - CUI
  - Database
description: "The command ‘–refedit’ or ‘refedit’provides the ability to edit the block references in-place. It allows you to switch among the nested block refer..."
author: Autodesk
---
# How to use Long transaction to mimic -refedit

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/-mimic-the-workflow-of-refedit-by-long-transaction.html

## 文章内容

By Xiaodong Liang
The command ‘–refedit’ or ‘refedit’provides the ability to edit the block references in-place. It allows you to switch among the nested block references. Then AutoCAD accepts the currently highlighted reference for in-place reference editing. The customization applications send the command ‘-refedit’ to accessing the edit mode for the user’s convenience
Actually, we could mimic -refedit’with long transactions. The classes and functions of long transactions provide a scheme for applications to check out entities for editing and check them back in to their original location. This operation replaces the original objects with the edited ones. It is pretty useful to manage which block we want to edit in-place.
The code below assumes a big block reference has a small block reference. It provides two commands：testcheckout asks to pick the entities of the small reference, then accept big reference for in-place reference editing. It is just a demo without much error checking.
There are more introductions in the ARX help document. The SDK\samples\database\longtrans_dg is also one demo.
//global variables for the two commands checkout and checkin
// ID of long transaction
AcDbObjectId long_trans_id;
//errorMap of long transaction
AcDbIdMapping error_map;
    /////////////////////////////////////////////////////////
    //  command: testcheckout
    //
    //  pick the entities of the small block reference
    //  accept the big block reference for in-place editing
    ///////////////////////////////////////////////////////
    static void ADNSample_testcheckout(void)
    {
          //  This is a fix demo, make sure to pick
        //  the enities of the small block reference
          ads_name ename;
        ads_point ptResult;
        ads_matrix adsmat;
        struct resbuf *info;
          AcDbObjectId ownerId;
          int rt =
            acedNEntSelP(_T("\nselect an entity of small block:"),
                          ename,ptResult, false ,adsmat, &info);
        if( rt!= RTNORM)
        {
            acutPrintf(_T("\nFailure in acedNEntSelP"));
            return;
        }
        if(info == NULL)
        {
            acutPrintf(_T("\n info is NULL"));
            return;
        }         
          //  The selected entity may reside in a nested references.        
        //  in this demo case: big reference and small reference
          // array stores all ids of references
        AcDbObjectIdArray owner_Entity_idArray;
          struct resbuf *rbIter = info;
        ads_name tempName;
        AcDbObjectId objId;         
        while (rbIter != NULL) {
                tempName[0] = rbIter->resval.rlname[0];
                tempName[1] = rbIter->resval.rlname[1];
                acdbGetObjectId(objId, tempName);
                owner_Entity_idArray.append(objId);
                  rbIter = rbIter->rbnext;
        }
        acutRelRb(info);
           //  In this demo, the second is the big reference
         AcDbObjectId big_ref_id = owner_Entity_idArray[1];
          //  iterate the owner entities.
        AcDbObjectIdArray  parentBlkEntArr;
        AcDbObjectId big_ref_rec_id;
          AcDbObject *pObj = NULL;
         //  open big reference        
        Acad::ErrorStatus es = acdbOpenObject(pObj,big_ref_id,AcDb::kForRead);
          if(Acad::eOk == es)
        {
            if(pObj->isKindOf(AcDbBlockReference::desc()))
            {                
                //  get block definition id of the big reference
                big_ref_rec_id =
                    ((AcDbBlockReference*)pObj)->blockTableRecord();
              }
            pObj->close();
        }    
            //  prepare the objects to check out.
        //  note: the objects of checkout are
        //  the entities of the block definition
           //open the block definiton of the big block reference
        es = acdbOpenObject(pObj,big_ref_rec_id,AcDb::kForWrite);
        if(es != Acad::eOk)
            return;
          AcDbBlockTableRecord *big_ref_rec =
              (AcDbBlockTableRecord*)pObj;
          //  message shows the block  name which is
        //  to be in-place edited
        const ACHAR *ref_rec_name = NULL;
        big_ref_rec->getName(ref_rec_name);
        TCHAR msg[256] = {0};
        _tcscat( msg,L"the block to be set to check out: ");
        _tcscat( msg, ref_rec_name );
        MessageBox(NULL,msg,msg,0);       
            AcDbObjectIdArray objIdArray;    
        AcDbBlockTableRecordIterator *pIter;
        big_ref_rec->newIterator(pIter);
        //  get the entities in the block definition
        for (pIter->start(); !pIter->done(); pIter->step())
        {
                AcDbEntity *pEntity;
                pIter->getEntity(pEntity, AcDb::kForRead);        
                objIdArray.append(pEntity->objectId());        
                pEntity->close();
        }
        delete pIter;
        big_ref_rec->close();
            //  get id of model space 
        AcDbBlockTable *pThisBlockTable;
        acdbHostApplicationServices()->workingDatabase()
        ->getSymbolTable(pThisBlockTable, AcDb::kForRead);
          AcDbBlockTableRecord *pThisMsBtr;
        pThisBlockTable->getAt(ACDB_MODEL_SPACE,
                    pThisMsBtr, AcDb::kForWrite);
        pThisBlockTable->close();
          AcDbObjectId model_space_id = pThisMsBtr->objectId();
        pThisMsBtr->close();
          //  check out
        acapLongTransactionManagerPtr()->checkOut(long_trans_id,
                            objIdArray, model_space_id, error_map);
            //  now you will see the big reference is
        //  being editing in-place
        //  you can edit the block manually
      }
      ///////////////////////////////////////////////
    //  command: testcheckin
    //
    //  check in the long transaction to submit
    //  the editing results
    //  
    ////////////////////////////////////////////
    static void ADNSample_testcheckin(void)
    {        
          // check in
        acapLongTransactionManagerPtr()->checkIn(
                    long_trans_id, error_map);
      }

