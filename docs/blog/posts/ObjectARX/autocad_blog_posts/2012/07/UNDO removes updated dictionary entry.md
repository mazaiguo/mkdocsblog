---
title: "UNDO removes updated dictionary entry"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
description: "I have the following command which either adds a new Xrecord to the Named Objects Dictionary or updates the value of the existing one."
author: Autodesk
---
# UNDO removes updated dictionary entry

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/undo-removes-updated-dictionary-entry.html

## 文章内容

By Adam Nagy
I have the following command which either adds a new Xrecord to the Named Objects Dictionary or updates the value of the existing one.
The problem is that if I run this command twice (the second time the entry already exists and so we just update its value) and then run UNDO, then instead of reverting the NOD entry's value back, it will remove it.
using System;
using Autodesk.AutoCAD.Runtime;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.EditorInput;
  namespace CsMgdAcad1
{
  public class AEN1Commands
  {
    [CommandMethod("UpdateXrecord")]
    static public void UpdateXrecord()
    {
      const string kMyData = "MYDATA";
        Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
        Database db = HostApplicationServices.WorkingDatabase;
      using (Transaction tr =
        db.TransactionManager.StartTransaction())
      {
        DBDictionary nod =
          (DBDictionary)tr.GetObject(
            db.NamedObjectsDictionaryId, OpenMode.ForRead);
          if (nod.Contains(kMyData))
        {
          // Update data
          Xrecord xrec =
            (Xrecord)tr.GetObject(
              nod.GetAt(kMyData), OpenMode.ForRead);
            int val = (int)xrec.Data.AsArray()[0].Value;
          Xrecord newXrec = new Xrecord();
          newXrec.Data = new ResultBuffer(
            new TypedValue[]
            {
              new TypedValue((int)LispDataType.Int32, val + 1)
            });
          nod.UpgradeOpen();
          nod.SetAt(kMyData, newXrec);
          tr.AddNewlyCreatedDBObject(newXrec, true);
          ed.WriteMessage(
            "Updated data with " + (val + 1).ToString());
        }
        else
        {
          // Initialize data
          Xrecord xrec = new Xrecord();
          xrec.Data = new ResultBuffer(
            new TypedValue[]
            {
              new TypedValue((int)LispDataType.Int32, 1)
            });
          nod.UpgradeOpen();
          nod.SetAt(kMyData, xrec);
          ed.WriteMessage("Initialized data with 1");
        }
          tr.Commit();
      }
    }
  }
}
Solution
There are two ways to solve the issue:
a) When you are updating the dictionary entry, then keep using the existing Xrecord and simpy update its data:
Xrecord xrec =
  (Xrecord)tr.GetObject(nod.GetAt(kMyData), OpenMode.ForWrite);
int val = (int)xrec.Data.AsArray()[0].Value;
xrec.Data = new ResultBuffer(
  new TypedValue[]
  {
    new TypedValue((int)LispDataType.Int32, val + 1)
  });
ed.WriteMessage("Updated data with " + (val + 1).ToString());
b) When you are updating the dictionary entry, then before updating it with the new Xrecord, remove the existing entry:
Xrecord xrec =
  (Xrecord)tr.GetObject(nod.GetAt(kMyData), OpenMode.ForRead);
int val = (int)xrec.Data.AsArray()[0].Value;
Xrecord newXrec = new Xrecord();
newXrec.Data = new ResultBuffer(
  new TypedValue[]
  {
    new TypedValue((int)LispDataType.Int32, val + 1)
  });
nod.UpgradeOpen();
// First remove existing entry
nod.Remove(kMyData);
nod.SetAt(kMyData, newXrec);
tr.AddNewlyCreatedDBObject(newXrec, true);
ed.WriteMessage("Updated data with " + (val + 1).ToString());

