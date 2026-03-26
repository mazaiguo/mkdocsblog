---
title: "Creating an extruded solid using an arbitrary polygon as its base"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Solid
description: "Solids in AutoCAD can be created using primitive shapes such as Box, Cone etc or by performing operations such as Extrude, Sweep etc."
author: Autodesk
---
# Creating an extruded solid using an arbitrary polygon as its base

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/creating-an-extruded-solid-using-an-arbitrary-polygon-as-its-base.html

## 文章内容

By Balaji Ramamoorthy
Solids in AutoCAD can be created using primitive shapes such as Box, Cone etc or by performing operations such as Extrude, Sweep etc.
Here is a sample code to demonstrate the creation of a solid by extruding a region.
<CommandMethod("CreateSolid")> _
Public Sub CreateSolidMethod()
    Dim db As Database =
        Application.DocumentManager.MdiActiveDocument.Database
      'start a transaction
    Using tr As Transaction =
                        db.TransactionManager.StartTransaction()
          ' create 5 lines to make the region from
        Dim l1, l2, l3, l4, l5 As Line
        l1 = New Line(
                        New Point3d(0, 0, 0),
                        New Point3d(4, 0, 0)
                     )
          l2 = New Line(
                        New Point3d(4, 0, 0),
                        New Point3d(4, 6, 0)
                     )
          l3 = New Line(
                        New Point3d(4, 6, 0),
                        New Point3d(0, 6, 0)
                     )
          l4 = New Line(
                        New Point3d(0, 6, 0),
                        New Point3d(-2, 3, 0)
                     )
          l5 = New Line(
                        New Point3d(-2, 3, 0),
                        New Point3d(0, 0, 0)
                     )
          ' add the lines to the array
        Dim myArray As New DBObjectCollection()
        myArray.Add(l1)
        myArray.Add(l2)
        myArray.Add(l3)
        myArray.Add(l4)
        myArray.Add(l5)
          ' create the region
        Dim myRegion As New Region()
        Dim myRegions As New DBObjectCollection()
        myRegions = myRegion.CreateFromCurves(myArray)
        myRegion = myRegions(0)
          ' create the solid
        Dim my3DSolid As New Solid3d()
        my3DSolid.Extrude(myRegion, 10.0, 0.0)
          Dim bt As BlockTable
                = CType(
                        tr.GetObject(
                                        db.BlockTableId,
                                        OpenMode.ForRead,
                                        False
                                     )
                                     , BlockTable
                        )
        Dim btr As BlockTableRecord
                = CType(
                        tr.GetObject(
                            bt(BlockTableRecord.ModelSpace),
                            OpenMode.ForWrite,
                            False
                            ),
                            BlockTableRecord
                        )
          'add 3DSolid to the model space block table record
        btr.AppendEntity(my3DSolid)
          'Let the transaction know about this object
        tr.AddNewlyCreatedDBObject(my3DSolid, True)
          tr.Commit()
    End Using
End Sub

