---
title: "Using WblockCloneObjects Copied ModelSpace Entities Disappear In The Current Drawing"
date: 2015-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Database
description: "This is a known behavior of Database.WblockCloneObjects() if used for the darwings being opened AutoCAD editor. Please follow these steps to work a..."
author: Autodesk
---
# Using WblockCloneObjects Copied ModelSpace Entities Disappear In The Current Drawing

发布日期: 2015-01-01

原始链接: https://adndevblog.typepad.com/autocad/2015/01/using-wblockcloneobjects-copied-modelspace-entities-disappear-in-the-current-drawing.html

## 文章内容

By Madhukar Moogala
This is a known behavior of Database.WblockCloneObjects() if used for the darwings being opened AutoCAD editor. Please follow these steps to work around this behavior.
Make the destination drawing as the current document 
Call TransactionManager.QueueForGraphicsFlush() to queue for a graphic flush 
Please note that you need to set the destination document as the current document to use TransactionManager.QueueForGraphicsFlush() otherwise you will get an expectation. Also please lock/unlock the document appropriately.
Here is the code snippet for showing these steps, I recently answered a similar query.
Test Case 1:
Download the drawing, save it in your C:\Temp folder, and running command WBCloneToCurrent, you will see dynamic block reference is created in current drawing.
[CommandMethod("WBCLONEToCurrent")]
public void WBCLONEToCurrent()
{
DocumentCollection dm = Application.DocumentManager;
Editor ed = dm.MdiActiveDocument.Editor;
Database destDb = dm.MdiActiveDocument.Database;
Database sourceDb = new Database(false, true);
string sourceFileName;
try
{
/*Download drawing from link*/
/*Copy dynamicblock to your temp folder*/
sourceFileName = "C:\\Temp\\\DynamicBlock.dwg";
sourceDb.ReadDwgFile(sourceFileName, System.IO.FileShare.Read, true, "");
ObjectIdCollection blockIds = new ObjectIdCollection();
Autodesk.AutoCAD.DatabaseServices.TransactionManager tm = sourceDb.TransactionManager;
using (Transaction myT = tm.StartTransaction())
{
  /*Handle of your Dynamic block reference*/
Handle handle = new Handle(0x215);
ObjectId brefId = ObjectId.Null;
sourceDb.TryGetObjectId(handle,out brefId);
blockIds.Add(brefId);
      }
IdMapping mapping = new IdMapping();
destDb.WblockCloneObjects(blockIds, destDb.CurrentSpaceId,
mapping, DuplicateRecordCloning.Replace, false);
  }
catch (Autodesk.AutoCAD.Runtime.Exception ex)
{
ed.WriteMessage("\nError during copy: " + ex.Message);
}
sourceDb.Dispose();
}
Test case 2 :
Open the DynamicBlock.dwg and a blank drawing in another tab, make DynamicBlock.dwg as current drawing and execute WBClone.
/*When switching documents you need to be in session mode.*/
[CommandMethod("WBCLONE", CommandFlags.Session)]
public void TestWBCLONE() {
DocumentCollection docs = Application.DocumentManager;
Document doc = docs.MdiActiveDocument;
Database db = doc.Database;
Editor Ed = doc.Editor;
Document destDoc = null;
foreach(Document tmpDoc in docs)
{
destDoc = tmpDoc;
}
try {
PromptEntityResult entRes = Ed.GetEntity("Select Bref");
if (entRes.Status != PromptStatus.OK) {
return;
}
ObjectIdCollection objIds = new ObjectIdCollection();
  /*add bref id */
objIds.Add(entRes.ObjectId);
  /*This is the trick  we need to make destination document as active one*/
Database destdb = destDoc.Database;
docs.MdiActiveDocument = destDoc;
using(DocumentLock docLock = destDoc.LockDocument())
{
using(Transaction trans = destdb.TransactionManager.StartTransaction()) {
/*
Please note that you need to set the destination
* document as the current document to use TransactionManager.QueueForGraphicsFlush()
* otherwise you will get an expectation.
* Also please lock/unlock the document appropriately.*/
trans.TransactionManager.QueueForGraphicsFlush();
IdMapping iMap = new IdMapping();
db.WblockCloneObjects(objIds, destdb.CurrentSpaceId, iMap, DuplicateRecordCloning.Ignore, false);
trans.Commit();
}
}
}
catch (System.Exception ex)
{
Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(ex.Message);
}
}

