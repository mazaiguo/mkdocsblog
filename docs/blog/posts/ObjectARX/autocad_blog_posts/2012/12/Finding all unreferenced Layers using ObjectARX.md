---
title: "Finding all unreferenced Layers using ObjectARX"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Database
  - Layer
  - ObjectARX
description: "How do I find the unreferenced layers in my database?"
author: Autodesk
---
# Finding all unreferenced Layers using ObjectARX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/finding-all-unreferenced-layers-using-objectarx.html

## 文章内容

by Fenton Webb
Issue
How do I find the unreferenced layers in my database?
Solution
The AcDbDatabase::purge() function does this for you…
Simply add all the AcDbObjectId's of AcDbLayerTableRecord's to a AcDbObjectIdArray and then call the AcDbDatabase::purge() function.
The following code segment demonstrates how to do this:
static void layersReferenced ()
{
  // get the working database
  AcDbDatabase *db = acdbHostApplicationServices()->workingDatabase();
  // now open the layer table for read
  AcDbLayerTablePointer layerTable(db, AcDb::kForRead);
  // create a new iterator to loop through all the layers
  AcDbLayerTableIterator *layerTableIterator ;
  layerTable->newIterator (layerTableIterator);
    AcDbObjectId id ;
  AcDbObjectIdArray layersNotReferenced;
  AcDbObjectIdArray layersReferenced;
  // iterate through the all layers and collect their ids
  for (; !layerTableIterator->done (); layerTableIterator->step())
  {
    layerTableIterator->getRecordId (id);
    layersNotReferenced.append (id) ;
    layersReferenced.append (id) ;
  }
  delete layerTableIterator ;
    // this will remove ids with have hard references on them
  // what remains is the ids of the unused layers
  if (db->purge(layersNotReferenced) != Acad::eOk )
  {
    acutPrintf (_T("\nPurge failed!")) ;
    return;
  }
  // print unused layers
  acutPrintf (_T("\nLayers not used")) ;
  for (int i=0 ; i<layersNotReferenced.length(); ++i)
  {
    id = layersNotReferenced[i];
    // open the layer for read
    AcDbLayerTableRecordPointer layerTableRecord(id, AcDb::kForRead);
    // if ok
    if (layerTableRecord.openStatus() == Acad::eOk)
    {
      TCHAR *name ;
      // get and dump the layer name
      layerTableRecord->getName (name) ;
      acutPrintf (_T("\nLayername : %s"), name) ;
    }
  }
    // take the unused layers out from the array of all layers
  for (int i=0; i<layersNotReferenced.length (); ++i)
    layersReferenced.remove (layersNotReferenced [i]) ;
    // print used layers
  acutPrintf (_T("\nLayers used")) ;
  for (int i=0; i<layersReferenced.length(); ++i)
  {
    id = layersNotReferenced[i];
    // open the layer for read
    AcDbLayerTableRecordPointer layerTableRecord(id, AcDb::kForRead);
    // if ok
    if (layerTableRecord.openStatus() == Acad::eOk)
    {
      TCHAR *name ;
      // get and dump the layer name
      layerTableRecord->getName (name) ;
      acutPrintf (_T("\nLayername : %s"), name) ;
    }
  }
}

