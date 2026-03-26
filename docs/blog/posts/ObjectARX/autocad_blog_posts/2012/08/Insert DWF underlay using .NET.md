---
title: "Insert DWF underlay using .NET"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Database
description: "DWF underlays are represented by the DwfDefinition and DwfReference classes in the AutoCAD .NET API. Basically it is required to open the NOD (Name..."
author: Autodesk
---
# Insert DWF underlay using .NET

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/insert-dwf-underlay-using-net.html

## 文章内容

By Augusto Goncalves
DWF underlays are represented by the DwfDefinition and DwfReference classes in the AutoCAD .NET API. Basically it is required to open the NOD (Named Object Dictionary) and get the DWF Definitions to create a new, so it can be used by the DWF Reference.
[CommandMethod("dwfInsert")]
static public void CommandInsertDWF()
{
  // acess the database
  Database db = Application.DocumentManager.
    MdiActiveDocument.Database;
    // start the transaction
  using (Transaction trans = db.TransactionManager.
    StartTransaction())
  {
    // get the NOD
    DBDictionary nod = trans.GetObject(
      db.NamedObjectsDictionaryId,
      OpenMode.ForWrite) as DBDictionary;
      // get the key for DWF Definition
    string defDictKey =
      UnderlayDefinition.GetDictionaryKey(
      typeof(DwfDefinition));
      // if the dictionary is not there, create
    if (!nod.Contains(defDictKey))
    {
      using (DBDictionary dict = new DBDictionary())
      {
        nod.SetAt(defDictKey, dict);
        trans.AddNewlyCreatedDBObject(dict, true);
      }
    }
      // open the dictionary
    ObjectId idDwfDef;
    DBDictionary dwfDict = trans.GetObject(
      nod.GetAt(defDictKey),
      OpenMode.ForWrite) as DBDictionary;
      // create a new definition
    using (DwfDefinition dwfDef = new DwfDefinition())
    {
      dwfDef.SourceFileName = "d:\\kitchen.dwf";
      idDwfDef = dwfDict.SetAt("kitchen", dwfDef);
      trans.AddNewlyCreatedDBObject(dwfDef, true);
    }
      // append to the model space
    BlockTable bt = trans.GetObject(
      db.BlockTableId, OpenMode.ForRead) as BlockTable;
    BlockTableRecord btr = trans.GetObject(
      bt[BlockTableRecord.ModelSpace],
      OpenMode.ForWrite) as BlockTableRecord;
    using (DwfReference dwf = new DwfReference())
    {
      dwf.DefinitionId = idDwfDef;
      btr.AppendEntity(dwf);
      trans.AddNewlyCreatedDBObject(dwf, true);
    }
    trans.Commit();
  }
}

