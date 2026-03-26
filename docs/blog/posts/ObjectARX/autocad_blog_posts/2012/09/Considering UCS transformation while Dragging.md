---
title: "Considering UCS transformation while Dragging"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - Dimension
  - UCS
  - Unicode
description: "When I am dragging to place my entity in WCS the entity appears correctly aligned. But when UCS is different from the WCS, the entity is not aligne..."
author: Autodesk
---
# Considering UCS transformation while Dragging

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/considering-ucs-transformation-while-dragging.html

## 文章内容

By Balaji Ramamoorthy
Issue
When I am dragging to place my entity in WCS the entity appears correctly aligned. But when UCS is different from the WCS, the entity is not aligned correctly. How can I consider UCS while dragging the entity ?
Solution
In the drag callback method, the matrix to transform the entity is returned. This matrix needs to be computed considering the original and the displaced points both of which correspond to the same coordinate system.
Here is a sample code that places a text entity by dragging. The points are transformed to the same coordinate system before using them to compute the transformation matrix.
Private mtLoc As Point3d = Point3d.Origin
  <CommandMethod("CreateText")> _
Public Sub CreateText()
    '' Get the current document and database
    Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
    Dim acCurDb As Database = acDoc.Database
    '' Start a transaction
    Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
        '' Open the Block table for read
        Dim acBlkTbl As BlockTable = TryCast(acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead), BlockTable)
        '' Open the Block table record Model space for write
        Dim acBlkTblRec As BlockTableRecord = Nothing
        acBlkTblRec = TryCast(acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), OpenMode.ForWrite), BlockTableRecord)
        '' Create a single-line text object
        Dim acText As New DBText()
          ' create the text here with nested transaction
        Using tr1 As Transaction = acCurDb.TransactionManager.StartTransaction()
            acText.SetDatabaseDefaults()
            acText.Position = New Point3d(0, 0, 0)
            acText.Height = 0.5
            acText.TextString = "Autodesk"
            acText.Rotation = 0.0
              Dim mtId As ObjectId = Nothing
            mtId = acBlkTblRec.AppendEntity(acText)
              tr1.AddNewlyCreatedDBObject(acText, True)
              tr1.Commit()
        End Using
          ' Transform the text to align with the UCS
        acText.TransformBy(Application.DocumentManager.MdiActiveDocument.Editor.CurrentUserCoordinateSystem)
          ' UCS origin in WCS
        mtLoc = Application.DocumentManager.MdiActiveDocument.Editor.CurrentUserCoordinateSystem.CoordinateSystem3d.Origin
          ' Select the last entity added (our MText)
        Dim myPSR As PromptSelectionResult = acDoc.Editor.SelectLast()
          Dim myPDO As New PromptDragOptions(myPSR.Value, vbLf & "Pick point for text: ", New DragCallback(AddressOf MyDragCallback))
          '' Get the point
        Dim myPPR As PromptPointResult = acDoc.Editor.Drag(myPDO)
          Dim mat As Matrix3d = Matrix3d.Displacement(mtLoc.GetVectorTo(myPPR.Value.TransformBy(Application.DocumentManager.MdiActiveDocument.Editor.CurrentUserCoordinateSystem)))
          acText.TransformBy(mat)
          '' Save the changes and dispose of the transaction
        acTrans.Commit()
    End Using
End Sub
  Private Function MyDragCallback(ByVal ptUCS As Point3d, ByRef mat As Matrix3d) As SamplerStatus
    ' If no change has been made, say so
    If (mtLoc = ptUCS) Then
        Return SamplerStatus.NoChange
    Else
        Dim ptWCS As Point3d = ptUCS.TransformBy(Application.DocumentManager.MdiActiveDocument.Editor.CurrentUserCoordinateSystem)
          '' Both mtLoc and ptWCS are now in WCS.
        mat = Matrix3d.Displacement(mtLoc.GetVectorTo(ptWCS))
    End If
    Return SamplerStatus.OK
End Function

