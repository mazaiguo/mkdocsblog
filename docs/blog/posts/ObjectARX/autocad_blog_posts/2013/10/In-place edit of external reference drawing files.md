---
title: "In-place edit of external reference drawing files"
date: 2013-10-01
categories:
  - AutoCAD
tags:
  - DWG
  - Database
  - XREF
description: "Below code shows the procedure to edit of external reference drawing file. for this purposes, code uses “XrefFileLock” class which handles the mana..."
author: Autodesk
---
# In-place edit of external reference drawing files

发布日期: 2013-10-01

原始链接: https://adndevblog.typepad.com/autocad/2013/10/in-place-edit-of-external-reference-drawing-files.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to edit of external reference drawing file. for this purposes, code uses “XrefFileLock” class which handles the management of Xref file locking.
[CommandMethod("editexref")]
static public void editexref()
{
      Document doc = Application.DocumentManager.MdiActiveDocument;
    Database database = doc.Database;
    XrefGraph mXRefTree = database.GetHostDwgXrefGraph(false);
      Database xrefDatatbase = null;
    XrefGraphNode xgn = null;
      for (int i = 0; i < mXRefTree.HostDrawing.NumOut; i++)
    {
        xgn = mXRefTree.HostDrawing.Out(i) as XrefGraphNode;
          //find the name of xref to edit
        if (string.Compare(xgn.Name, "TEST", true) == 0)
        {
            xrefDatatbase = xgn.Database;
            break;
        }
    }
      if (xrefDatatbase == null)
        return;
      //edit the app
    int nCtlType =
            XrefFileLock.GetXloadCtlType(xrefDatatbase.XrefBlockId);
    using (XrefFileLock Filelock =
                    XrefFileLock.LockFile(xrefDatatbase.XrefBlockId))
    {
        xrefDatatbase.RestoreOriginalXrefSymbols();
          //add a line
        Line line =
            new Line(new Point3d(0, 0, 0), new Point3d(10, 10, 0));
          using (Transaction tr =
                xrefDatatbase.TransactionManager.StartTransaction())
        {
            BlockTable bt =
                (BlockTable)tr.GetObject(xrefDatatbase.BlockTableId,
                                                    OpenMode.ForRead);
            BlockTableRecord ms = (BlockTableRecord)tr.GetObject(
                                    bt[BlockTableRecord.ModelSpace],
                                                  OpenMode.ForWrite);
              ms.AppendEntity(line);
            tr.AddNewlyCreatedDBObject(line, true);
            tr.Commit();
          }
        xrefDatatbase.RestoreForwardingXrefSymbols();
    }
  }

