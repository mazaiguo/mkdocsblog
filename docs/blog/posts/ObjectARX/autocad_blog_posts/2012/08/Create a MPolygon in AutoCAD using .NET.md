---
title: "Create a MPolygon in AutoCAD using .NET"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - Database
  - ObjectARX
description: "MPolygon is a custom object created for AutoCAD Map 3D, but is also available in vanilla AutoCAD from ObjectARX. To use it from .NET, then the proj..."
author: Autodesk
---
# Create a MPolygon in AutoCAD using .NET

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/create-a-mpolygon-in-autocad-using-net.html

## 文章内容

By Augusto Goncalves
MPolygon is a custom object created for AutoCAD Map 3D, but is also available in vanilla AutoCAD from ObjectARX. To use it from .NET, then the project need to reference the AcMPolygonMGD.dll and it is required to load the object enabler AcMPolygonObj19.dbx into AutoCAD prior to using MPolygon functions. Both files can be found in AutoCAD's install folder.
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.Geometry
  Public Class MPolygonCommandClass
  ' to make sure the required DBX is loaded
  ' let's implement the extension application
  ' and load it on Initilize
  Implements IExtensionApplication
    Public Sub Initialize() _
    Implements IExtensionApplication.Initialize
    ' Make sure that AcMPolygonObj19.dbx is loaded for MPolygon
    ' the 19 version number is valid for AutoCAD 2013
    Autodesk.AutoCAD.Runtime. _
      SystemObjects.DynamicLinker.LoadModule( _
        "AcMPolygonObj19.dbx", False, False)
  End Sub
    Public Sub Terminate() _
    Implements IExtensionApplication.Terminate
    ' nothing is required for this sample
  End Sub
    <CommandMethod("CreateMPolygon")> _
  Public Sub CreateMPolygon()
    Dim db As Database = Application. _
      DocumentManager.MdiActiveDocument.Database
    Using transaction As Transaction = _
      db.TransactionManager.StartTransaction()
      Try
        ' open the block tabela and the model space
        Dim bt As BlockTable = transaction.GetObject( _
          db.BlockTableId, OpenMode.ForRead)
        Dim btr As BlockTableRecord = transaction.GetObject( _
          bt(BlockTableRecord.ModelSpace), _
          OpenMode.ForWrite)
          ' start creating the MPolygon
        ' by its loop
        Dim mPolygonLoop As MPolygonLoop
        mPolygonLoop = New MPolygonLoop()
        mPolygonLoop.Add(New BulgeVertex(New Point2d(2, 2), 0))
        mPolygonLoop.Add(New BulgeVertex(New Point2d(2, 1), 0))
        mPolygonLoop.Add(New BulgeVertex(New Point2d(1, 1), 0))
        mPolygonLoop.Add(New BulgeVertex(New Point2d(1, 2), 0))
        mPolygonLoop.Add(New BulgeVertex(New Point2d(2, 2), 0))
          ' finally create the entity and append
        ' the the model space
        Dim mPolygon As MPolygon = New MPolygon()
        mPolygon.AppendMPolygonLoop(mPolygonLoop, False, 0)
        btr.AppendEntity(mPolygon)
        transaction.AddNewlyCreatedDBObject(mPolygon, True)
        transaction.Commit()
      Catch ex As Exception
        Debug.WriteLine(ex.ErrorStatus)
        Debug.WriteLine(ex.Message)
      End Try
    End Using
  End Sub
End Class

## 评论

**内容**: Rolando said...
Thank you Augusto, this information is very useful.
Reply
12/20/2016 at 09:00 AM

---
