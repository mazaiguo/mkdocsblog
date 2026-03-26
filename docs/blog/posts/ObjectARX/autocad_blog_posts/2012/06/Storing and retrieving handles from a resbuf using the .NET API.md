---
title: "Storing and retrieving handles from a resbuf using the .NET API"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - DXF
  - Database
description: "Here is some (fairly contrived) code to demonstrate one way to store a handle in a result buffer and then retrieve it later. If you’re storing data..."
author: Autodesk
---
# Storing and retrieving handles from a resbuf using the .NET API

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/storing-and-retrieving-handles-from-a-resbuf-using-the-net-api.html

## 文章内容

By Stephen Preston
Here is some (fairly contrived) code to demonstrate one way to store a handle in a result buffer and then retrieve it later. If you’re storing data in an Xrecord, then you wouldn’t normally store the Handle - you’d use a HardPointerId or SoftPointerId instead. You’re more likely to store Handles in Xdata. Xdata doesn’t allow you to store DXF codes below 1000, which excludes hard and soft pointers. The benefit of using hard/soft pointers is that deep clone translation of linked entities is taken care of for you.
  Document doc = Application.DocumentManager.MdiActiveDocument;
  Database db = doc.Database;
  Editor ed = doc.Editor; 
  //Use an arbitrary ObjectId as an example
  ObjectId id = db.NamedObjectsDictionaryId;
  ed.WriteMessage("\nObjectId of NOD = " + id.ToString());
  //Add the Handle to a resbuf
  ResultBuffer buf =
    new ResultBuffer(new TypedValue((int)DxfCode.Handle, id.Handle));
  //Retrieve the Handle and use it to construct an ObjectId
  TypedValue[] arr = buf.AsArray();
  long val = Convert.ToInt64(arr[0].Value.ToString(), 16);
  Handle hCG = new Handle(val);
  ObjectId newId = db.GetObjectId(false, hCG, 0);
  ed.WriteMessage("\nObjectId using the handle = " + id.ToString());

