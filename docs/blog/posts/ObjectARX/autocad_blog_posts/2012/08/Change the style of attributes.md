---
title: "Change the style of attributes"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Block
  - Unicode
description: "From each AcDbBlockReference it is possible to create an attribute iterator (using AcDbBlockReference::attributeIterator()) and then step through t..."
author: Autodesk
---
# Change the style of attributes

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/change-the-style-of-attributes.html

## 文章内容

By Augusto Goncalves
From each AcDbBlockReference it is possible to create an attribute iterator (using AcDbBlockReference::attributeIterator()) and then step through the attributes in the INSERT.
AcDbAttribute is derived from AcDbText, so we can use AcDbText::setTextStyle() to set the next style using the id of the text style.
In this example STANDARD's object ID is used. You shouldn't have to explode/reblock the INSERTs, just remember to close() it.
Also be aware that for constant attributes you have to change the text style in the block definition not in the block reference. The code below demonstrates this.
ads_name ename ;
ads_point pt ;
Acad::ErrorStatus es;
acedEntSel (_T("Select a Block Reference: "), ename, pt) ;
AcDbObjectId id ;
acdbGetObjectId (id, ename) ;
AcDbBlockReference *pBlockReference ;
acdbOpenAcDbObject ((AcDbObject *&)pBlockReference, id,
          AcDb::kForRead);
//Get the ObjectId of the STANDARD style
AcDbTextStyleTable * pTextStyleTable;
AcDbObjectId standardStyleId;
acdbCurDwg()->getTextStyleTable ( pTextStyleTable, AcDb::kForRead );
pTextStyleTable->getAt ( _T("STANDARD"), standardStyleId );
pTextStyleTable->close();
//----- Change nested attributes
AcDbObjectIterator *pIter ;
pIter =pBlockReference->attributeIterator () ;
while ( !pIter->done () ) {
  AcDbObjectId attributeId =pIter->objectId () ;
  // open the attribute
  AcDbAttribute *pAttribute;
  es = pBlockReference->openAttribute(pAttribute,
    attributeId,AcDb::kForWrite);
  assert(es == Acad::eOk);
  // changing the style
  pAttribute->setTextStyle( standardStyleId ) ;
  pAttribute->close();
  pIter->step () ;
}   
delete pIter ;
//----- change constant attributes
id =pBlockReference->blockTableRecord () ;
AcDbBlockTableRecord *pRec ;
acdbOpenAcDbObject ((AcDbObject *&)pRec, id, AcDb::kForRead) ;
if ( pRec->hasAttributeDefinitions () == Adesk::kTrue ) {
  AcDbBlockTableRecordIterator *pIter2 ;
  pRec->newIterator (pIter2) ;
  while ( !pIter2->done () ) {
    AcDbEntity *pEnt ;
    pIter2->getEntity (pEnt, AcDb::kForRead) ;
    if ( pEnt->isKindOf (AcDbAttributeDefinition::desc ()) ){
      AcDbAttributeDefinition *pDef=
        (AcDbAttributeDefinition *)pEnt ;
      if ( pDef->isConstant () == Adesk::kTrue ) {
        pDef->upgradeOpen();
        pDef->setTextStyle( standardStyleId ) ;
      }            }            pEnt->close () ;
      pIter2->step () ;
  }        delete pIter2 ;
}    pRec->close () ;
pBlockReference->close () ;

