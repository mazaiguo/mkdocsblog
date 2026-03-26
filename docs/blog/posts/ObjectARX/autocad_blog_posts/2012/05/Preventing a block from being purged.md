---
title: "Preventing a block from being purged"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Block
  - Layer
description: "We will look at two approaches to prevent a block from getting purged."
author: Autodesk
---
# Preventing a block from being purged

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/preventing-a-block-from-being-purged.html

## 文章内容

By Balaji Ramamoorthy
We will look at two approaches to prevent a block from getting purged.
1) Create a block reference out of the block and assign it to a hidden layer
2) Create a custom object that stores a hard pointer to the block. An instance of the custom object can be stored within your dictionary stored under the named object dictionary.
Here is the code snippet for the first method :
static Acad::ErrorStatus CreateBlock_Method1()
{
    Acad::ErrorStatus es;
    AcDbBlockTable *pBlockTable = NULL;
      AcDbDatabase *pDb
            = acdbHostApplicationServices()->workingDatabase();
      pDb->getBlockTable(pBlockTable, AcDb::kForWrite);
    AcDbBlockTableRecord* pAnonBlock = new AcDbBlockTableRecord();
    pAnonBlock->setName(_T("*U"));
      AcDbObjectId idAnonBlock = AcDbObjectId::kNull;
    pBlockTable->add(idAnonBlock, pAnonBlock);
      AcDbCircle *pCircle = new AcDbCircle(
                                            AcGePoint3d::kOrigin,
                                            AcGeVector3d::kZAxis,
                                            5.0
                                        );
      pAnonBlock->appendAcDbEntity(pCircle);
      pCircle->close();
      pAnonBlock->close();
      // Method : 1
    // Create an anonymous layer and use it for the
    // newly created block reference.
    AcDbObjectId layerId = AcDbObjectId::kNull;
    AcDbLayerTable* lTable;
    es = pDb->getSymbolTable(lTable, AcDb::kForWrite);
      if(Acad::eOk == es && lTable)
    {
        AcDbLayerTableRecord* lTblRec = new AcDbLayerTableRecord;
        lTblRec->setName(ACRX_T("TEST"));
        lTblRec->setIsHidden(true);
        AcCmColor layerColor;
        layerColor.setColorIndex(2);
        lTblRec->setColor(layerColor);
          if (lTable->add(layerId, lTblRec) != Acad::eOk)
            AfxMessageBox(_T("ERROR Creating Layer"));
        else
            lTblRec->close();
          lTable->close();
    }
      // Create a block reference and set to the hidden layer
    AcDbBlockReference *pBlkRef
            = new AcDbBlockReference(
                                        AcGePoint3d::kOrigin,
                                        idAnonBlock
                                    );
    pBlkRef->setLayer(layerId, true, true);
      AcDbBlockTableRecord *pModelSpace;
    pBlockTable->getAt(
                        ACDB_MODEL_SPACE,
                        pModelSpace,
                        AcDb::kForWrite
                      );
      pModelSpace->appendAcDbEntity(pBlkRef);
      pBlkRef->close();
    pModelSpace->close();
    pBlockTable->close();
      return Acad::eOk;
}
Here is the code snippet for the second method :
// Step : 1
// Create a basic custom object using the ARX wizard
    // Step : 2
// In your custom object header file, add an id that will
// hold the ObjectId of the block that we are trying to
// prevent getting purged.
public:
    // Id of the object to prevent purge
    AcDbObjectId _Id;
    // Step : 3
// Ensure that the objectId of the block is filed.
// For this make the following changes to the
// dwgInFields and dwgOutFields methods.
Acad::ErrorStatus AdsMyCustomObj::dwgOutFields
                                    (AcDbDwgFiler *pFiler) const
{
    // ...
    //----- Output params
    pFiler->writeHardPointerId(_Id);
      return (pFiler->filerStatus ()) ;
}
  Acad::ErrorStatus AdsMyCustomObj::dwgInFields
                                        (AcDbDwgFiler *pFiler)
{
    // ...
    //----- Read params
    AcDbHardPointerId hardPointerId;
    pFiler->readHardPointerId(&hardPointerId);
    _Id = hardPointerId;
      return (pFiler->filerStatus ()) ;
}
    // Step : 4
// Here is the method that creates a block table record
// and stores its id in the custom object instance.
// The custom object instance is stored in a custom dictionary
// under the named object dictionary.
static Acad::ErrorStatus CreateBlock_Method2( )
{
    Acad::ErrorStatus es;
    AcDbBlockTable *pBlockTable = NULL;
      AcDbDatabase *pDb
            = acdbHostApplicationServices()->workingDatabase();
      pDb->getBlockTable(pBlockTable, AcDb::kForWrite);
    AcDbBlockTableRecord* pAnonBlock = new AcDbBlockTableRecord();
    pAnonBlock->setName(_T("*U"));
      AcDbObjectId idAnonBlock = AcDbObjectId::kNull;
    pBlockTable->add(idAnonBlock, pAnonBlock);
      AcDbCircle *pCircle = new AcDbCircle(
                                            AcGePoint3d::kOrigin,
                                            AcGeVector3d::kZAxis,
                                            5.0
                                        );
      pAnonBlock->appendAcDbEntity(pCircle);
    pCircle->close();
    pAnonBlock->close();
      // Method : 2
    // Custom object in the NOD to store the hard pointer
    // to the block
    AcDbObjectPointer<AcDbDictionary> pNOD(
                                            pDb->namedObjectsDictionaryId(),
                                            AcDb::kForWrite
                                          );
    AcDbDictionary *pMyDict = NULL;
      AcDbObject *pMyDictObject = NULL;
    if(pNOD->getAt(
                    ACRX_T("MYOBJDICT"),
                    pMyDictObject,
                    AcDb::kForWrite
                  ) == Acad::eOk)
    {
        pMyDict = AcDbDictionary::cast(pMyDictObject);
    }
    else
    {
        pMyDict = new AcDbDictionary();
        AcDbObjectId DictObjectId = AcDbObjectId::kNull;
        pNOD->setAt(ACRX_T("MYOBJDICT"), pMyDict, DictObjectId);
    }
      AcDbObjectId customObjectId;
    AdsMyCustomObj *pCustObj = new AdsMyCustomObj();
    pCustObj->_Id = idAnonBlock;
    pMyDict->setAt (_T("DETAILS"), pCustObj, customObjectId);
    pCustObj->close ();
      pMyDict->close();
    pNOD->close();
      pBlockTable->close();
    return Acad::eOk;
}

