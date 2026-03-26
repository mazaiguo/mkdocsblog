---
title: "Plant SDK: Get ObjectID by PnPID"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Is it possible to get the objectID by its PnPID or RowID?"
author: Autodesk
---
# Plant SDK: Get ObjectID by PnPID

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/plant-sdk-get-objectid-by-pnpid.html

## 文章内容

By Marat Mirgaleev
Issue
Is it possible to get the objectID by its PnPID or RowID?
Solution
Yes. It is a two steps process, because there is a one-to-many possibility.
PnPID and RowID are the same thing.
  1. DataLinksManager.FindAcPpObjectIds(rowId) --> collection of PpObjectId
  2. DataLinksManager.MakeAcDbObjectId(ppObjId) --> converts PpObjectId to ObjectId
There are various flavors of those functions. The main point to get across is that multiple AcDbObjectIds may be linked to a single RowID.
Here is a sample:
// Conversions of IDs back and forth.
//------------------------------------------------------------------
[CommandMethod("TestIds")]
public static void TestIds()
{
  // Prepare to the work: Let's get some entity's ObjectId
  Database db =
    Application.DocumentManager.MdiActiveDocument.Database;
  DataLinksManager dlm = DataLinksManager.GetManager(db);
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
  ObjectId entId = ed.GetEntity("Pick a P&ID item: ").ObjectId;
    // Now get the PnPID (i.e. PpObjectId)
  //   from the selected entity's ObjectId
  PpObjectId pnpId = dlm.MakeAcPpObjectId(entId);
    // Now let's do an opposite action - find ObjectId(s) of the entity
  int rowId1 = dlm.FindAcPpRowId(entId); // You can use ObjectId
  int rowId2 = dlm.FindAcPpRowId(pnpId); //          or PpObjectId
  // rowId1 and rowId2 are always equal
    PpObjectIdArray ids = dlm.FindAcPpObjectIds(rowId1);
  // NOTE: It returns a COLLECTION of AcPpObjectId!
  //     I.e., multiple AcDbObjectIds may be linked to a single RowID
    // Now find the ObjectID for each PpObjectId
  foreach (PpObjectId ppid in ids)
  {
    ObjectId oid = dlm.MakeAcDbObjectId(ppid);
    ed.WriteMessage("\n oid=" + oid.ToString());
  }
} // TestIds()

## 评论

**内容**: Martin Buss said...
Can you tell me what is the background of that there can be more than one objects found for a single pnpID ? Because e.g. in the p&id drawing, there will be a rowid created for every single part that I place there.
And from the PnIDCreateSline example in the Helper class I can see the following method, which clearly assumes that there is just one objectId associated with a rowID.
 public static ObjectId ConvertRowIdToObjectId(int iRowId)
        {
            // Fetch ObjectId of part.
            //
            var res = Helper.ActiveDataLinksManager.FindAcPpObjectIds(iRowId);
            var pnidId = res.First.Value;
            ObjectId pnidObjectId = Helper.ActiveDataLinksManager.MakeAcDbObjectId(pnidId);
            return pnidObjectId;
        }
Reply
09/08/2015 at 07:19 AM

---
