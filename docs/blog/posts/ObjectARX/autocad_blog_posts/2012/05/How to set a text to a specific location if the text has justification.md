---
title: "How to set a text to a specific location if the text has justification"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Unicode
description: "We got a question to place text in a specific location with justification ‘MC’. But  the text is NOT placed at the location, though the justificati..."
author: Autodesk
---
# How to set a text to a specific location if the text has justification

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-set-a-text-to-a-specific-location-if-the-text-has-justification.html

## 文章内容

By Xiaodong Liang
We got a question to place text in a specific location with justification ‘MC’. But  the text is NOT placed at the location, though the justification in set correctly.   
If you want to set the text to by modifying its alignment point, please just use
oTextEnt.AlignmentPoint = newPoint      
If  you want to set the text by modifying its position when the text has justification, please refer to the following code.
Sub TextPosition()
     Dim doc As Document = Autodesk.AutoCAD. _
        ApplicationServices.Application. _
        DocumentManager.MdiActiveDocument
     Dim ed as Editor = doc.Editor
   Dim selection As PromptSelectionResult = ed.GetSelection()
      Dim tm = Autodesk.AutoCAD.ApplicationServices.Application. _
        DocumentManager.MdiActiveDocument.TransactionManager
      Dim objectID As ObjectId
      Dim ta As Transaction = tm.StartTransaction()
      Try
        For Each objectID In selection.Value.GetObjectIds()
            Dim  ent As Entity= tm.GetObject( _
                objectID, OpenMode.ForWrite)
            If TypeOf ent is DBText then
               Dim oText As DBText = ent
               Dim textPosition = oText.Position
               Dim transMatrix As Matrix3d  = _
                   Matrix3d.Identity
               Dim newPosition As New Point3d(10, 10, 10)
               Dim transVec As Vector3d =  _
                   newPosition -
                   textPosition
               ' tranform so that the whole text
               ' including position and alighment point are
               ' relocated.
               transMatrix = _
                   transMatrix.Displacement(transVec)
              oText.TransformBy(transMatrix)
            End If                           
       Next     
        ta.Commit()
    Catch ex As System.Exception
        MsgBox(ex.Message)
    Finally
        ta.Dispose()
    End Try
  End Sub

## 评论

**内容**: r2d2 said...
Great post.
Tweaked it slightly to get a set of text aligned to 5 based coordinates. code:
....
'modified and added code 2013-08-07
Dim Xround, Yround, Zround As String
Xround = Math.Round(Val(textPosition.X) / 5) * 5
Yround = Math.Round(Val(textPosition.Y) / 5) * 5
Zround = Math.Round(Val(textPosition.Z) / 5) * 5
Dim newPosition As New Point3d(Xround, Yround, Zround)
....
Reply
08/07/2013 at 02:06 PM

---
