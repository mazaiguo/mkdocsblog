---
title: "Adding new file location using Sheetset API"
date: 2015-05-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - Plugin
description: "Here is a code snippet to add a new file location and to set it as the new sheet location using the Sheetset API :"
author: Autodesk
---
# Adding new file location using Sheetset API

发布日期: 2015-05-01

原始链接: https://adndevblog.typepad.com/autocad/2015/05/adding-new-file-location-using-sheetset-api.html

## 文章内容

By Balaji Ramamoorthy
Here is a code snippet to add a new file location and to set it as the new sheet location using the Sheetset API :
 AcSmSheetSetMgr manager = new  AcSmSheetSetMgr();
   AcSmDatabase sheetDb = 
         manager.FindOpenDatabase(@"D:\\Temp\\MySheetset.dst" );
 sheetDb.LockDb(sheetDb);
   // New sheet location 
 AcSmResources resources 
             = sheetDb.GetSheetSet().GetResources();
 AcSmFileReference fileRef = new  AcSmFileReference();
 fileRef.InitNew(resources);
 fileRef.SetFileName(@"D:\\Temp\\SampleDrawings" );
 sheetDb.GetSheetSet().SetNewSheetLocation(fileRef);
   // Add New location 
 AcSmFileReference fileRef1 = new  AcSmFileReference();
 fileRef1.InitNew(sheetDb);
 fileRef1.SetFileName(@"D:\\Temp\\SampleDrawings" );
 resources.Add(fileRef1);
   sheetDb.UnlockDb(sheetDb);
  After you run the code, the model views from all the drawings in the path should get listed under Model Views as shown in this screenshot :

