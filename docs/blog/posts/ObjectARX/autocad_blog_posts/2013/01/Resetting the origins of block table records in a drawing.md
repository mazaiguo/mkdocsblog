---
title: "Resetting the origins of block table records in a drawing"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Block
description: "The following code demonstrates how to modify a block table record's origin and compensate by moving the insertion point of each of the associated ..."
author: Autodesk
---
# Resetting the origins of block table records in a drawing

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/resetting-the-origins-of-block-table-records-in-a-drawing.html

## 文章内容

By Gopinath Taget
The following code demonstrates how to modify a block table record's origin and compensate by moving the insertion point of each of the associated block references.
Please add the function 'testFunc' as a command.
void ResetAllInstances(AcDbBlockTableRecord * pBlockTableRecord,
AcGeVector3d &translation)
{
 // Note that this function does not
 // implement any error checking.
 // We are assuming that pBlockTableREcord
 // was opened for write by the calling function
   // Iterate through all block references
 // of this block table record.
AcDbBlockReferenceIdIterator * pIterator;
pBlockTableRecord->newBlockReferenceIdIterator(pIterator);
 for (pIterator->start();!pIterator->done();
  pIterator->step())
{
  AcDbBlockReference * pBlockRef;
  pIterator->getBlockReference(pBlockRef,
   AcDb::kForWrite,true);
  // Transform the translation vector from
  // block coordinates to world coordinates.
  AcGeVector3d realTranslation =
   (pBlockRef->blockTransform())*translation;
  // Translate the block reference to
  // counter the effect of the origin change.
  pBlockRef->setPosition(
   pBlockRef->position()+realTranslation);
    pBlockRef->close();
} // Next block reference
 delete pIterator;
}
// This is command 'SGP'
void testFunc()
{
 // Note that error checking is minimal.
ads_name ename ;
ads_point pt ;
 // Ask the user to select an object
 if( acedEntSel (
  L"\nSelect the Block Reference",
  ename, pt) != RTNORM )
  return ;
 // Open it
AcDbObjectId objId;
acdbGetObjectId (objId, ename) ;
AcDbEntity * pEnt;
acdbOpenObject (pEnt, objId, AcDb::kForRead);
 // Check its a block reference
AcDbBlockReference *pRef =
  AcDbBlockReference::cast(pEnt);
 if (pRef == NULL)
{
  pEnt->close();
  return;
}
 // Get the block reference's
 // associated block table record.
AcDbObjectId blockId =pRef->blockTableRecord ();
pRef->close();
AcDbBlockTableRecord *pBlockTableRecord;
acdbOpenObject (pBlockTableRecord,
  blockId, AcDb::kForWrite);
 // Store the BTR's current
 // origin (we'll need it later).
AcGePoint3d origin = pBlockTableRecord->origin();
 // And set its new origin to (0, 0, 0)
pBlockTableRecord->setOrigin(AcGePoint3d(0, 0, 0));
   // Create a translation vector for the change
 // in displacement required to offset the
 // origin change (in the block's coordinate system)
AcGeVector3d translation;
translation.set(-origin[X], -origin[Y], -origin[Z]);
 // Now process all instances of this block
 // reference to compensate for the change in the block origin
ResetAllInstances(pBlockTableRecord, translation);
pBlockTableRecord->close();
}

## 评论

**内容**: Oleg said...
Hi, Gopinath,
thanks for your article and code
Here is translation on C#,
please, let me know if this would works same way:
public static void ResetAllInstances(BlockTableRecord pBlockTableRecord, Vector3d translation)
{
Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;
Database db = doc.Database;
Transaction tr = doc.TransactionManager.StartTransaction();
using (tr)
{
BlockTable bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);
string[] blockNames = GetBlockNamesInDrawing(db);
foreach (string blockName in blockNames)
{
ObjectId blkid = bt[blockName];
BlockTableRecord blkrec = (BlockTableRecord)tr.GetObject(bt[blockName], OpenMode.ForRead);//******************
ObjectIdCollection ids = blkrec.GetBlockReferenceIds(true, false);
// Note that this function does not
// implement any error checking.
// We are assuming that pBlockTableREcord
// was opened for write by the calling function
// Iterate through all block references
// of this block table record.
foreach (ObjectId brefid in ids)
{
BlockReference bref = (BlockReference)tr.GetObject(brefid, OpenMode.ForWrite);
// Transform the translation vector from
// block coordinates to world coordinates.
Vector3d vec = bref.BlockTransform.Translation;
Vector3d newvec = vec + translation;
// Translate the block reference to
// counter the effect of the origin change.
bref.Position = bref.Position.TransformBy(Matrix3d.Displacement(newvec));
}

}
tr.Commit();
}//end using transaction
}
// This is command 'SGP'
[CommandMethod("SGP")]
public static void testFunc()
{
Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;
Database db = doc.Database;
Transaction tr = doc.TransactionManager.StartTransaction();
using (tr)
{
// Note that error checking is minimal.
Entity ent;
// Ask the user to select an object
PromptEntityOptions peo = new PromptEntityOptions("\nSelect the Block Reference >>");
peo.SetRejectMessage("\nSelect Block Reference only >>");
peo.AddAllowedClass(typeof(BlockReference), false);
PromptEntityResult res;
res = ed.GetEntity(peo);
if (res.Status != PromptStatus.OK)
return;
ent = (Entity)tr.GetObject(res.ObjectId, OpenMode.ForRead);
if (ent == null)
return;
BlockReference bref = (BlockReference)ent as BlockReference;
if (bref != null)
{
bref.UpgradeOpen();
// Get the block reference's
// associated block table record.
ObjectId blockId = bref.BlockTableRecord;
BlockTableRecord pBlockTableRecord = (BlockTableRecord)tr.GetObject(blockId, OpenMode.ForWrite);
// Store the BTR's current
// origin (we'll need it later).
Point3d origin = pBlockTableRecord.Origin;
// And set its new origin to (10, 20, 0)
pBlockTableRecord.Origin = new Point3d(10, 20, 0);
// Create a translation vector for the change
// in displacement required to offset the
// origin change (in the block's coordinate system)
Vector3d translation = new Vector3d(-origin.X, -origin.Y, -origin.Z);
// Now process all instances of this block
// reference to compensate for the change in the block origin
ResetAllInstances(pBlockTableRecord, translation);
bref.DowngradeOpen();
}
tr.Commit();
}//end using transaction
}
Reply
01/02/2013 at 09:34 AM

---
**内容**: Gopinath Taget said in reply to Oleg...
Hi Oleg,
Your .NET code is different from the C++ code I provided in a couple of ways. In the testFunc() method, you are setting the block table record origin to a specific value (10, 20, 0) but your translating the block references to (-origin.X, -origin.Y, -origin.Z). This will not give you what you need. You should really be doing this:
Vector3d translation = new Vector3d(10-origin.X, 20-origin.Y, 0-origin.Z);
Also, in the ResetAllInstances call, you are iterating through all the block table records which is wrong and unnecessary. You should use the pBlockTableRecord paremeter passed like I did in the C++ code.
Reply
01/02/2013 at 06:38 PM

---
**内容**: Oleg said in reply to Gopinath Taget...
Many thanks for your explanation
I will do it,
Kind regards,
Oleg
Reply
01/02/2013 at 11:48 PM

---
**内容**: Oleg said...
Hi Gopinath,
Here is amended code,
a bit tricky way to iterate through all subentities,
but seems it's working good on my end:
public static void ResetAllInstances(BlockTableRecord pBlockTableRecord, Vector3d translation)
{
Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;
Database db = doc.Database;
Transaction tr = doc.TransactionManager.StartTransaction();
using (tr)
{
// Note that this function does not
// implement any error checking.
// We are assuming that pBlockTableREcord
// was opened for write by the calling function
// Iterate through all block references
// of this block table record.

BlockTableRecordEnumerator pIterator = pBlockTableRecord.GetEnumerator();
while (pIterator.MoveNext())
{
//make sure you've work with block instance
if (pIterator.Current.ObjectClass.IsDerivedFrom(RXClass.GetClass(typeof(BlockReference))) &&
pIterator.Current.GetType().IsAssignableFrom(typeof(BlockReference)))
{
BlockReference pBlockRef = (BlockReference)tr.GetObject(pIterator.Current, OpenMode.ForWrite);
// Transform the translation vector from
// block coordinates to world coordinates.

Vector3d realTranslation = (pBlockRef.BlockTransform) * translation;
// Translate the block reference to
// counter the effect of the origin change.
pBlockRef.Position = pBlockRef.Position + realTranslation;
}
} // Next block reference
pIterator.Dispose();
tr.Commit();
}//end using transaction

}
// This is command 'SGP'
[CommandMethod("SGP")]
public static void testFunc()
{
Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;
Database db = doc.Database;
Transaction tr = doc.TransactionManager.StartTransaction();
using (tr)
{
// Note that error checking is minimal.
Entity ent;
// Ask the user to select an object
PromptEntityOptions peo = new PromptEntityOptions("\nSelect the Block Reference >>");
peo.SetRejectMessage("\nSelect Block Reference only >>");
peo.AddAllowedClass(typeof(BlockReference), false);
PromptEntityResult res;
res = ed.GetEntity(peo);
if (res.Status != PromptStatus.OK)
return;
ent = (Entity)tr.GetObject(res.ObjectId, OpenMode.ForRead);
if (ent == null)
return;
BlockReference bref = (BlockReference)ent as BlockReference;
if (bref != null)
{
bref.UpgradeOpen();
// Get the block reference's
// associated block table record.
ObjectId blockId = bref.BlockTableRecord;
BlockTableRecord pBlockTableRecord = (BlockTableRecord)tr.GetObject(blockId, OpenMode.ForWrite);
// Store the BTR's current
// origin (we'll need it later).
Point3d origin = pBlockTableRecord.Origin;
// And set its new origin to (10, 20, 0)// dummy point
pBlockTableRecord.Origin = new Point3d(10, 20, 0);
// Create a translation vector for the change
// in displacement required to offset the
// origin change (in the block's coordinate system)
Vector3d translation = new Vector3d(10 - origin.X, 20 - origin.Y, 0 - origin.Z);
// Now process all instances of this block
// reference to compensate for the change in the block origin
ResetAllInstances(pBlockTableRecord, translation);
bref.DowngradeOpen();
}
tr.Commit();
}//end using transaction
ed.Regen();// to update origin changes
}
Kind regards,
Oleg
Reply
01/04/2013 at 12:44 AM

---
**内容**: Gopinath Taget said in reply to Oleg...
Hi Oleg,
I am surprised this code works. pBlockTableRecord.GetEnumerator(); does not return the block references associated with a block table record. You should really be using pBlockTableRecord.GetBlockReferenceIds to find these block references and change their position.
Cheers
Gopinath
Reply
01/16/2013 at 09:06 PM

---
**内容**: Ali said...
ObjectArx reference says; AcDbBlockTableRecord::origin() will always return (0,0,0) for blocks created by AutoCad versions after release 10.
So, only setOrigin() changes origin from (0,0,0) by code.
Origin is not base point as I see in block definition dialog.
How can I get/set base point instead of origin?
Reply
09/30/2015 at 06:15 PM

---
