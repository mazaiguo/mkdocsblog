---
title: "Adding an xref to a drawing (and converting attachments to overlays)"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - Plugin
  - XREF
description: "Its easy to add an xref to a drawing, but it was only in AutoCAD 2012 that we exposed a function to convert an xref attachment to an overlay. The f..."
author: Autodesk
---
# Adding an xref to a drawing (and converting attachments to overlays)

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/use-the-converter-class-to-format-distances-and-angles.html

## 文章内容

By Stephen Preston
Its easy to add an xref to a drawing, but it was only in AutoCAD 2012 that we exposed a function to convert an xref attachment to an overlay. The following VB.NET code snippet shows two functions. The first inserts an xref, the second iterates through all BlockTableRecords in the drawing converting all attachment xrefs to overlays.
    <CommandMethod("addAnXref")> _
    Public Sub addAnXref()
      Dim doc As Document = Application.DocumentManager.MdiActiveDocument
      Dim db As Database = doc.Database
      Using trans As Transaction = db.TransactionManager.StartTransaction()
        ' Attach the Xref
        Dim xrefObj As ObjectId =
                      db.AttachXref("C:\temp\TestXef.dwg", "test2")
        Dim br As New BlockReference(New Point3d(0, 0, 0), xrefObj)
        ' Add the xref to model space
        Dim bt As BlockTable =
            trans.GetObject(db.BlockTableId, OpenMode.ForRead)
        Dim modelSpace As BlockTableRecord =
          trans.GetObject(bt(BlockTableRecord.ModelSpace), OpenMode.ForWrite)
        modelSpace.AppendEntity(br)
        trans.AddNewlyCreatedDBObject(br, True)
        trans.Commit()
      End Using
    End Sub
      <CommandMethod("changeToOverlay")> _
    Public Sub changeToOverlay()
      Dim doc As Document =
                        Application.DocumentManager.MdiActiveDocument
      Dim db As Database = doc.Database
      Using trans As Transaction =
                            db.TransactionManager.StartTransaction()
        Dim bt As BlockTable =
                trans.GetObject(db.BlockTableId, OpenMode.ForRead)
        For Each btrId As ObjectId In bt
          Dim btr As BlockTableRecord =
                            trans.GetObject(btrId, OpenMode.ForRead)
          If btr.IsFromExternalReference Then
            btr.UpgradeOpen()
            btr.IsFromOverlayReference = True
          End If
        Next
        trans.Commit()
      End Using
    End Sub
Its also worth noting these comments in the ObjectARX SDK documentation (that aren’t reproduced in the documentation for the .NET class:
This function will set this AcDbBlockTableRecord to be an overlay if bIsOverlay is true; otherwise, it will set it to be in insert type xref. This just sets the BlockTableRecord's overlay flag.
This function will only work on a AcDbBlockTableRecord that is an xref, and that is NOT a nested xref.
In order to accurately determine if this BlockTableRecord represents a nested xref, this BlockTableRecord must have been closed since the last BlockReference that references it was created. This is necessary so that the BlockTableRecord's list of referencing BlockReferences is up to date.
In fact, its always a good idea to review the (C++) ObjectARX documentation when reading about a new function. The C++ information will often give you some useful hints for your .NET code.

