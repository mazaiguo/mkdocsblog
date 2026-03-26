---
title: "Forming a selection set of entities and access their picked points"
date: 2012-12-01
categories:
  - AutoCAD VBA
tags:
  - AutoCAD
  - Dimension
  - Plugin
  - Selection
  - VBA
description: "How do I access the coordinates of the point picked on each of the selection set entities? I am using the 'SelectionOnScreen' VBA method, which pro..."
author: Autodesk
---
# Forming a selection set of entities and access their picked points

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/forming-a-selection-set-of-entities-and-access-their-picked-points.html

## 文章内容

By Daniel Du
Issue
How do I access the coordinates of the point picked on each of the selection set entities? I am using the 'SelectionOnScreen' VBA method, which prompts the user to select objects in AutoCAD, then returns a set containing these objects. I want to also access the coordinates of the point picked on each of the selection set entities.
Solution
A SelectOnScreen selection cannot be used to ascertain the pickpoint of selected entities. Instead, you need to perform the construction of the selection set in two stages. First, prompt the user to choose an entity. This action has the advantage of reporting not only a chosen entity, but also the selected point.
The GetEntity method off the utility object obtains both picked point and entity.
Secondly, if the selection is valid (no random keystrokes or selection of a non-entity point), then try adding the entity to a selection set. As long as the entity is not already present in the set, the selection set will expand and the corresponding pick point can then be appended to an array.
Then when you get a valid entity selection, you should store the entity reference into the selection set, and the picked point into an array.
The code below demonstrates how it should be done in a VBA macro.
  Public Sub getSelPt()
   Dim selPts() As Variant, Pt As Variant
   Dim msgOut As String
  
   Dim selEntity As AcadEntity
   Dim sset As AcadSelectionSet, ArraySize As Integer
 
   ' Creates an empty selection set.
   Set sset = ThisDrawing.SelectionSets.Add("mySelSet")
   oldSize = 0: newSize = 0
   Err.Clear
   ArraySize = 1
  
  
   On Error GoTo makeSetHndlr
    ' Keep prompting for entity selection until bad pick or escape
    While True
        ' Fake entity selection
        ThisDrawing.Utility.GetEntity selEntity, Pt, "Pick an entity (enter to stop)"
   
        ' Do the real entity selection by using the point returned from the API call above
        sset.SelectAtPoint Pt
        newSize = sset.Count
       
        ' If the selection growled, then store the picked point into the array
        If newSize > oldSize Then
        ReDim Preserve selPts(1 To ArraySize)
        selPts(ArraySize) = Pt
       
        selEntity.Highlight True
       
        oldSize = newSize
        ArraySize = ArraySize + 1
        End If
    Wend
  
makeSetHndlr:
   Err.Clear
   msgOut = "DONE: " & sset.Count & " unique entities in selset"
   For Each selPt In selPts
    msgOut = msgOut & Chr(13) & "at " & Format(selPt(0), ".###") & " , " & Format(selPt(1), ".###")
   Next selPt
   MsgBox msgOut
End Sub
  For .net API, you can use PromptEntityResult.PickedPoint.
Hope this helps.

## 评论

**内容**: Daniel said...
Excellent thanks, just what I was looking for
Reply
09/17/2017 at 11:29 AM

---
