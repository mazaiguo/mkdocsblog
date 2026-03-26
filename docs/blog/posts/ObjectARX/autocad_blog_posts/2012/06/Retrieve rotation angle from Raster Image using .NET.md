---
title: "Retrieve rotation angle from Raster Image using .NET"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Database
description: "Here is a code snippet which demonstrates how to find out the Rotation angle of an inserted image in a drawing file"
author: Autodesk
---
# Retrieve rotation angle from Raster Image using .NET

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/retrieve-rotation-angle-from-raster-image-using-net.html

## 文章内容

By Virupaksha Aithal
Here is a code snippet which demonstrates how to find out the Rotation angle of an inserted image in a drawing file
    <CommandMethod("RotationTest")> _
    Public Sub RotationTest()
            Dim doc As Document = _
                        Application.DocumentManager.MdiActiveDocument
            Dim db As Database = _
                        doc.Database
              Dim ed As Editor = doc.Editor
              Dim prompEntOpt As PromptEntityOptions _
                             = New PromptEntityOptions(vbCrLf + _
                                        "Choose a Raster Image: ")
            prompEntOpt.SetRejectMessage(vbCrLf + _
                                      "Select only Image reference")
            prompEntOpt.AddAllowedClass(GetType(RasterImage), True)
              Dim prompEntRes As PromptEntityResult = _
                                            ed.GetEntity(prompEntOpt)
              If Not (prompEntRes.Status = PromptStatus.OK) Then
                ed.WriteMessage(vbCrLf + "Error in picking entity!")
                Return
            End If
              Dim tm As Transaction = _
                          db.TransactionManager.StartTransaction()
              Using tm
                Dim image As RasterImage
                image = tm.GetObject(prompEntRes.ObjectId, _
                                                OpenMode.ForRead)
                Dim cs As CoordinateSystem3d = image.Orientation
                  Dim origin As Point3d = cs.Origin
                Dim vec As Vector3d = cs.Xaxis
                Dim xaxis As New Vector3d(1, 0, 0)
                Dim angle As Double = vec.GetAngleTo(xaxis)
                ' converting Radian to degree
                angle = angle * (180 / Math.PI)
                Dim str As String = angle.ToString()
                ed.WriteMessage(str)
                tm.Commit()
            End Using
          End Sub

