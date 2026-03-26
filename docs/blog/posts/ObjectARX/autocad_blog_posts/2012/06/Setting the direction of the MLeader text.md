---
title: "Setting the direction of the MLeader text"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Unicode
description: "To ensure that the direction of the MLeader text appears just the way it appears with the AutoCAD MLeader command, it is necessary to set the direc..."
author: Autodesk
---
# Setting the direction of the MLeader text

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/setting-the-direction-of-the-mleader-text.html

## 文章内容

By Balaji Ramamoorthy
To ensure that the direction of the MLeader text appears just the way it appears with the AutoCAD MLeader command, it is necessary to set the direction of the MLeader text. Here is a sample code to set the text direction based on the inclination of the leader line. The “SetDogLeg” method can be used for this.
Here is a sample code :
Dim activeDoc As Document _
               = Application.DocumentManager.MdiActiveDocument
  Dim db As Database = activeDoc.Database
Dim ed As Editor = activeDoc.Editor
  Dim ppr1 As PromptPointResult = ed.GetPoint( _
                 vbLf & "Specify leader  arrowhead location")
  If ppr1.Status <> PromptStatus.OK Then
    Return
End If
  Dim startPoint As Point3d = ppr1.Value
Dim ppo As New PromptPointOptions(vbLf & "Specify leader landing location")
            ppo.BasePoint = startPoint
            ppo.UseBasePoint = True
Dim ppr2 As PromptPointResult = ed.GetPoint(ppo)
If ppr2.Status <> PromptStatus.OK Then
    Return
End If
  Dim endPoint As Point3d = ppr2.Value
Dim blockText As String = "Autodesk"
  Using tr As Transaction = db.TransactionManager.StartTransaction()
  Dim bt As BlockTable = DirectCast( _
tr.GetObject( _
                db.BlockTableId, _
                OpenMode.ForRead _
            ), BlockTable)
  Dim btr As BlockTableRecord = DirectCast( _
tr.GetObject( _
                db.CurrentSpaceId, _
                OpenMode.ForRead _
            ), BlockTableRecord)
  Dim ml As New MLeader()
            ml.SetDatabaseDefaults()
  ' Creates a new leader cluster
Dim leaderNumber As Integer = ml.AddLeader()
  ' Add a leader line to the cluster
Dim leaderLineNum As Integer = ml.AddLeaderLine(leaderNumber)
ml.AddFirstVertex(leaderLineNum, startPoint)
ml.AddLastVertex(leaderLineNum, endPoint)
  Dim mt As New MText()
mt.Contents = blockText
  Dim direction As Double = 1.0
If (endPoint - startPoint).DotProduct(Vector3d.XAxis) < 0.0 Then
    direction = -1.0
End If
  ml.SetDogleg( leaderNumber, Vector3d.XAxis.MultiplyBy(direction))
ml.MText = mt
  btr.UpgradeOpen()
btr.AppendEntity(ml)
  tr.AddNewlyCreatedDBObject(ml, True)
tr.Commit()
  End Using

