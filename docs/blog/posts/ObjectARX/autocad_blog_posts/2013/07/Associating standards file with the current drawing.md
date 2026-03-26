---
title: "Associating standards file with the current drawing"
date: 2013-07-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - Plugin
description: "Adding a standards file to the current drawing is not possible using the Standards API. A way to work around this limitation is to add a XRecord to..."
author: Autodesk
---
# Associating standards file with the current drawing

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/associating-standards-file-with-the-current-drawing.html

## 文章内容

By Balaji Ramamoorthy
Adding a standards file to the current drawing is not possible using the Standards API. A way to work around this limitation is to add a XRecord to the "AcStStandard" dictionary under the Named Object Dictionary.
Here is a sample code snippet that prompts for the DWS file path and add it to the current drawing. 
Database db = Application.DocumentManager.MdiActiveDocument.Database;
Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
  // Ask for the dws file path to add
PromptStringOptions pso
                = new PromptStringOptions("DWS File Path : ");
PromptResult pr = ed.GetString(pso);
if (pr.Status != PromptStatus.OK)
    return;
String dwsPath = pr.StringResult;
  using (Transaction tr = db.TransactionManager.StartTransaction())
{
    //Get the named object dictionary
    DBDictionary nod = tr.GetObject
                    (
                        db.NamedObjectsDictionaryId,
                        OpenMode.ForRead
                    ) as DBDictionary;
      // Find the "AcStStandard" dictionary
    DBDictionary standardsDict = null;
    if (!nod.Contains("AcStStandard"))
    {// Create it if not found
        nod.UpgradeOpen();
        standardsDict = new DBDictionary();
        nod.SetAt("AcStStandard", standardsDict);
        tr.AddNewlyCreatedDBObject(standardsDict, true);
    }
    else
    {
        // Get it if it already exists
        standardsDict = tr.GetObject
                    (
                        nod.GetAt("AcStStandard"),
                        OpenMode.ForWrite
                    ) as DBDictionary;
    }
      // Find the dictionary name that we will add
    int recordCount = 0;
    foreach(DBDictionaryEntry dictEntry in standardsDict)
    {
        recordCount++;
    }
      // Create a Xrecord with the dws file path set
    // to the DXF code : 1
    TypedValue tv = new TypedValue((int)1, dwsPath);
    Xrecord record = new Xrecord();
    using (ResultBuffer rb = new ResultBuffer(tv))
    {
        record.Data = rb;
    }
      // Add the Xrecord to the dictionary
    standardsDict.SetAt(recordCount.ToString(), record);
    tr.AddNewlyCreatedDBObject(record, true);
      // Done
    tr.Commit();
}

