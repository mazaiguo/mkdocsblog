---
title: "Constant and Non-Constant Block Attributes"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
description: "When iterating attributes of a specific block reference, you may not find all of them as expected. The reason for this is because an AcDbBlockTable..."
author: Autodesk
---
# Constant and Non-Constant Block Attributes

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/constant-and-non-constant-block-attributes.html

## 文章内容

By Balaji Ramamoorthy
When iterating attributes of a specific block reference, you may not find all of them as expected. The reason for this is because an AcDbBlockTableRecord owns all attribute definitions, and an AcDbBlockReference (the insert of a block) owns all the non-constant attributes. If a block definition defines some constant attributes, AutoCAD will not create attributes in the AcDbBlockReference for them. By iterating the AcDbBlockReference object, you can find only the non-constant attributes, if you also want the constant attributes, you must iterate the AcDbBlockTableRecord as well.
The following sample code demonstrates this:
ads_name ename ;
ads_point pt ;
acedEntSel (L"Select a Block Reference: ", ename, pt) ;
  AcDbObjectId id ;
acdbGetObjectId (id, ename) ;
  AcDbBlockReference *pRef ;
acdbOpenAcDbObject ((AcDbObject *&)pRef, id, AcDb::kForRead) ;
  //----- List Non-Const attributes
AcDbObjectIterator  *pIter ;
pIter = pRef->attributeIterator () ;
int cnt =0 ;
while ( !pIter->done () )
{
    cnt++ ;
    AcDbObjectId ida =pIter->objectId () ;
    acutPrintf (L"\nAttribute %d - ObjectId %ld", cnt, ida) ;
    pIter->step();
}
delete pIter ;
acutPrintf (L"\n%d Non-Const Attribute(s) Found!", cnt) ;
  //----- List Constant attributes
cnt =0 ;
id =pRef->blockTableRecord () ;
AcDbBlockTableRecord *pRec ;
acdbOpenAcDbObject ((AcDbObject *&)pRec, id, AcDb::kForRead) ;
if ( pRec->hasAttributeDefinitions () == Adesk::kTrue )
{
    AcDbBlockTableRecordIterator *pIter2 ;
    pRec->newIterator (pIter2) ;
    while ( !pIter2->done () )
    {
        AcDbEntity *pEnt ;
        pIter2->getEntity (pEnt, AcDb::kForRead) ;
        if ( pEnt->isKindOf (AcDbAttributeDefinition::desc ()) )
        {
            AcDbAttributeDefinition *pDef=(AcDbAttributeDefinition *)pEnt ;
            if ( pDef->isConstant () == Adesk::kTrue )
            {
                cnt++;
                acutPrintf (L"\nConstant Attribute %d - ObjectId %ld)", cnt, pDef->objectId()) ;
            }
        }
        pEnt->close () ;
        pIter2->step () ;
    }
    delete pIter2 ;
}
acutPrintf (L"\n%d Constant Attribute(s) Found!", cnt) ;
  pRec->close () ;
pRef->close () ;

