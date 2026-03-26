---
title: "How to mimic the AutoCAD insert command in ARX without acedCommand call"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - Block
  - C++
  - DWG
  - Database
description: "This operation needs to be divided into two different steps. The first step is to have an AcDbBlockTableRecord, which contains the block definition..."
author: Autodesk
---
# How to mimic the AutoCAD insert command in ARX without acedCommand call

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-mimic-the-autocad-insert-command-in-arx-without-acedcommand-call.html

## 文章内容

By Gopinath Taget
This operation needs to be divided into two different steps. The first step is to have an AcDbBlockTableRecord, which contains the block definition. You could either create, edit an existing one, or import it from another drawing file. The following example shows how to import a block definition from an external drawing file:
AcDbDatabase *pDwg =new AcDbDatabase (Adesk::kFalse) ;
  pDwg->readDwgFile (_T("c:\\drawing1.dwg")) ;
  //----- Put it into a block table record of the current database
  AcDbObjectId id ;
  Acad::ErrorStatus es = acdbHostApplicationServices()->
   workingDatabase()->insert(id, _T("drawing1"), pDwg, Adesk::kFalse) ;
  if ( es != Acad::eOk )
   acutPrintf (_T("\nError inserting a block.")) ;
  delete pDwg ;
As soon as you have a block table record in place you can add an AcDbBlockReference with it. The block reference is the INSERT'ed block table record instance that is displayed in the model or paper space. The below example shows how to create a block reference with attributes from a block table record. You can call it following above code like this:
AcGePoint3d point3D(0,0,0);
addBlockWithAttributes(id,point3D);
Here is the code for addBlockWithAttributes:
// NOTE: You will have to update the code to properly set the
// attribute values. The code below sets the value of each
// attribute to "XXX".
static void addBlockWithAttributes (AcDbObjectId blockId,
AcGePoint3d basePoint) {
 //----- Step 1: Allocate a block reference object
AcDbBlockReference *pBlkRef =new AcDbBlockReference ;
 //----- Step 2: Set up the block reference to the newly
 //----- created block definition
pBlkRef->setBlockTableRecord (blockId) ;
 //---- Give it the current UCS normal.
pBlkRef->setPosition (basePoint) ;
pBlkRef->setRotation (0.0) ;
pBlkRef->setNormal (AcGeVector3d (0.0, 0.0, 1.0)) ;
 //----- Step 3: Open current database's Model Space
 //----- blockTableRecord
AcDbBlockTable *pBlockTable ;
acdbHostApplicationServices()->workingDatabase()->
  getBlockTable (pBlockTable, AcDb::kForRead) ;
AcDbBlockTableRecord *pBlockTableRecord ;
pBlockTable->getAt (ACDB_MODEL_SPACE, pBlockTableRecord,
  AcDb::kForWrite) ;
pBlockTable->close () ;
 //----- Append the block reference to the model space
 //----- block table record
AcDbObjectId newEntId ;
pBlockTableRecord->appendAcDbEntity (newEntId, pBlkRef) ;
pBlockTableRecord->close () ;
 //----- Step 4: Open the block definition for read
AcDbBlockTableRecord *pBlockDef ;
acdbOpenObject (pBlockDef, blockId, AcDb::kForRead) ;
AcDbBlockTableRecordIterator *pIterator ;
pBlockDef->newIterator (pIterator) ;
AcDbEntity *pEnt ;
AcDbAttributeDefinition *pAttdef ;
 for ( pIterator->start () ; !pIterator->done() ;
  pIterator->step () ) {
  //----- Get the next entity
  pIterator->getEntity (pEnt, AcDb::kForRead) ;
  //----- Make sure the entity is an attribute definition
  //----- and not a constant
  pAttdef =AcDbAttributeDefinition::cast (pEnt) ;
  if ( pAttdef != NULL && !pAttdef->isConstant () ) {
   //----- We have a non-constant attribute definition
   //----- so build an attribute entity
   AcDbAttribute *pAtt =new AcDbAttribute ;
   pAtt->setPropertiesFrom (pAttdef) ;
   pAtt->setInvisible (pAttdef->isInvisible ()) ;
   //----- Translate attribute by block reference.
   //----- To be really correct, entire block
   //----- reference transform should be applied here.
   basePoint =pAttdef->position () ;
   basePoint +=pBlkRef->position ().asVector () ;
   pAtt->setPosition (basePoint) ;
   pAtt->setHeight (pAttdef->height ()) ;
   pAtt->setRotation (pAttdef->rotation ()) ;
   pAtt->setTag (_T("Tag")) ;
   pAtt->setFieldLength (25) ;
   TCHAR *pStr =pAttdef->tag () ;
   pAtt->setTag (pStr) ;
   delete pStr ;
   pAtt->setFieldLength (pAttdef->fieldLength ()) ;
   //----- Database Column value should be displayed
   //----- INSERT would prompt for this...
   pAtt->setTextString (_T("XXX")) ;
   //----- Set Alignments
   pAtt->setHorizontalMode( pAttdef->horizontalMode ()) ;
   pAtt->setVerticalMode (pAttdef->verticalMode ()) ;
   pAtt->setAlignmentPoint (
    pAttdef->alignmentPoint ()
    + pBlkRef->position ().asVector ()
    ) ;
   //----- Insert the attribute in the DWG
   AcDbObjectId attId ;
   pBlkRef->appendAttribute (attId, pAtt) ;
   pAtt->close () ;
  }    
  pEnt->close () ; //----- Use pEnt... pAttdef might be NULL
}
 delete pIterator ;
pBlockDef->close () ;
pBlkRef->close () ;
}

