---
title: "Xline to Line and LTSCALE override"
date: 2013-07-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "Just a couple of utility functions here."
author: Autodesk
---
# Xline to Line and LTSCALE override

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/xline-to-line-and-ltscale-override.html

## 文章内容

By Adam Nagy
Just a couple of utility functions here.
One converts all the Construction Lines (AcadXline/Xline/AcDbXline - in case someone is searching for a different name :)) to Line entities (AcadLine/Line/AcDbLine). You may need this if you have xline's in a block and you would like to snap to them outside the block. It does not seem possible, whereas line's are snappable even outside the block:
' Application Session Command with localized name
<CommandMethod("AcmUtilityConvertXlines")> _
Public Shared Sub AcmUtilConvertXlines() ' This method can have any name
  Dim doc As Document = acApp.DocumentManager.MdiActiveDocument
    Dim db As Database = doc.Database
    Using tr As Transaction = db.TransactionManager.StartTransaction()
      ' Just something crude to start with
    Dim length As Double
    length = db.Extmin.DistanceTo(db.Extmax) * 2
      Dim bt As BlockTable
    bt = tr.GetObject(db.BlockTableId, OpenMode.ForRead)
      For Each blockId In bt
      Dim block As BlockTableRecord
      block = tr.GetObject(blockId, OpenMode.ForRead)
        Dim modified As Boolean = False
        For Each entId In block
        If entId.ObjectClass = Xline.GetClass(GetType(Xline)) Then
          If Not modified Then
            block.UpgradeOpen()
            modified = True
          End If
            Dim xl As Xline = tr.GetObject(entId, OpenMode.ForWrite)
            Using l As New Line
            l.StartPoint = xl.BasePoint.Add(xl.UnitDir.MultiplyBy(-length))
            l.EndPoint = xl.BasePoint.Add(xl.UnitDir.MultiplyBy(length))
            l.Layer = xl.Layer
            l.Color = xl.Color
            block.AppendEntity(l)
            tr.AddNewlyCreatedDBObject(l, True)
          End Using
            xl.Erase()
        End If
      Next
        ' If the block got modified then let's update its references
      If modified Then
        For Each brId As ObjectId In block.GetBlockReferenceIds(True, True)
          Dim br As BlockReference
          br = tr.GetObject(brId, OpenMode.ForWrite)
          br.RecordGraphicsModified(True)
        Next
      End If
    Next
      tr.Commit()
  End Using
End Sub
The  other overrides the LTSCALE value before using the HATCH command and then sets it back afterwards. You may need this if you have dashed lines closing an area you want to hatch - the hatch preview looks OK but the created hatch might extend beyond the selected area. This can be prevented by using a smaller LTSCALE value:
Shared ltscale As Double
  ' Application Session Command with localized name
<CommandMethod("AcmUtilityHatch")> _
Public Shared Sub AcmUtilHatch() ' This method can have any name
  Dim doc As Document = acApp.DocumentManager.MdiActiveDocument
    ltscale = doc.Database.Ltscale
  doc.Database.Ltscale = 0.01
  doc.Editor.Regen()
    doc.SendStringToExecute("_.HATCH ", False, False, False)
    AddHandler doc.CommandEnded, AddressOf doc_CommandEnded
  AddHandler doc.CommandCancelled, AddressOf doc_CommandEnded
  AddHandler doc.CommandFailed, AddressOf doc_CommandEnded
End Sub
  Public Shared Sub doc_CommandEnded(sender As Object, e As Autodesk.AutoCAD.ApplicationServices.CommandEventArgs)
  If e.GlobalCommandName = "HATCH" Then
    Dim doc As Document = sender
    RemoveHandler doc.CommandEnded, AddressOf doc_CommandEnded
    RemoveHandler doc.CommandCancelled, AddressOf doc_CommandEnded
    RemoveHandler doc.CommandFailed, AddressOf doc_CommandEnded
      doc.Database.Ltscale = ltscale
    doc.Editor.Regen()
  End If
End Sub
There might be nicer solutions to the problem. This is just a quick solution: Download AcmUtility
The attachment also contains the compiled project for AutoCAD 2013/2014 and the bundle that can be simply placed in the appropriate folder on the system so that it will be loaded automatically into AutoCAD: http://docs.autodesk.com/ACD/2013/ENU/index.html?url=files/GUID-5E50A846-C80B-4FFD-8DD3-C20B22098008.htm,topicNumber=d30e503195

