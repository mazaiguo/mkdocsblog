---
title: "VBA: How to setup selectionset filters for a block or layer?"
date: 2012-07-01
categories:
  - AutoCAD VBA
tags:
  - Block
  - Layer
  - Selection
  - VBA
description: "How do I use a selection set filter to select a block with a particular name"
author: Autodesk
---
# VBA: How to setup selectionset filters for a block or layer?

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/vba-how-to-setup-selectionset-filters-for-a-block-or-layer.html

## 文章内容

By Philippe Leefsma
Q:
How do I use a selection set filter to select a block with a particular name
that is on a particular layer ?
A:
The following sample code allows you to select blocks based on this criteria:
1. selectALayer() - create a selectionset with entities on "layer1"
2. selectABlock() - create a selectionset with a block insert "testBlock"
3. selectABlockOnALayer() - create a selectionset with a block insert "testBlock" on "layer1"

Sub selectALayer()
   Dim sset As AcadSelectionSet
   Set sset = ThisDrawing.SelectionSets.Add("TestSet1")
  
   Dim filterType As Variant
   Dim filterData As Variant
   Dim p1(0 To 2) As Double
   Dim p2(0 To 2) As Double
  
   Dim grpCode(0) As Integer
   grpCode(0) = 8
   filterType = grpCode
   Dim grpValue(0) As Variant
   grpValue(0) = "Layer1"
   filterData = grpValue
   
   sset.Select acSelectionSetAll, p1, p2, filterType, filterData
  
   Debug.Print "Entities: " & str(sset.count)
  
   sset.Delete
  
End Sub
Sub selectABlock()
   Dim sset As AcadSelectionSet
   Set sset = ThisDrawing.SelectionSets.Add("TestSet2")
  
   Dim filterType As Variant
   Dim filterData As Variant
   Dim p1(0 To 2) As Double
   Dim p2(0 To 2) As Double
  
   Dim grpCode(0) As Integer
   grpCode(0) = 2
   filterType = grpCode
   Dim grpValue(0) As Variant
   grpValue(0) = "testBlock"
   filterData = grpValue
   
   sset.Select acSelectionSetAll, p1, p2, filterType, filterData
  
   Debug.Print "Entities: " & str(sset.count)
  
   sset.Delete
  
End Sub
Sub selectABlockOnALayer()
   Dim sset As AcadSelectionSet
   Set sset = ThisDrawing.SelectionSets.Add("TestSet3")
  
   Dim filterType As Variant
   Dim filterData As Variant
   Dim p1(0 To 2) As Double
   Dim p2(0 To 2) As Double
  
   Dim grpCode(0 To 1) As Integer
   grpCode(0) = 8
   grpCode(1) = 2
   filterType = grpCode
  
   Dim grpValue(0 To 1) As Variant
   grpValue(0) = "layer1"
   grpValue(1) = "testBlock"
   filterData = grpValue
  
   sset.Select acSelectionSetAll, p1, p2, filterType, filterData
  
   Debug.Print "Entities: " & str(sset.count)
  
   sset.Delete
  
End Sub

## 评论

**内容**: Ricardo said...
Excellent! just a reminder: p1 and p2 are optional and are not required when using select all.
sset.Select acSelectionSetAll, , ,filterType, filterData
Reply
02/15/2013 at 04:25 AM

---
**内容**: Pedro said...
Hi,
I have a question about the second example. What do I do if I wish to insert more that one type of block to the selection?
I have tried
grpValue(0) = "testBlock1" & "testBlock2" & "testBlock3"
but to no avail.
Any help would be deeply apreciated,
kind regards
Reply
08/20/2019 at 09:56 AM

---
**内容**: Pedro said in reply to Pedro...
For anyone interested, I found out. The correct line is:
grpValue(0) = "testBlock1,testBlock2,testBlock3"
Reply
08/21/2019 at 09:10 AM

---
**内容**: Oscar Fernandez said in reply to Pedro...
to filter many entities with the same code see this url:
https://knowledge.autodesk.com/es/search-result/caas/CloudHelp/cloudhelp/2018/ESP/AutoCAD-ActiveX/files/GUID-A1A6DB80-A730-45D1-B035-331F549E9667-htm.html
Reply
11/18/2019 at 01:11 AM

---
**内容**: Oscar Fernandez said...
The best way to know the value that you need to filter any entitie. is use autolisp order in command bar.
Command:(entget (ssname (ssget) 0))
it allow select one entitie and present you all his Codes and values from the entitie.
in case of block reference present:
((-1 . ) (0 . "INSERT") (330 . ) (5 . "6C77E") (100 . "AcDbEntity") (67 . 0) (410 . "Model") (8 . "ARQ-ALUMBRA") (100 . "AcDbBlockReference") (2 . "FP") (10 581408.0 4.79624e+06 0.0) (41 . 1.5) (42 . 1.5) (43 . 1.5) (50 . 5.58545) (70 . 0) (71 . 0) (44 . 0.0) (45 . 0.0) (210 0.0 0.0 1.0))
then (0 . "INSERT"):
for block filter :
IntCod (n) = 0
VarValue (n) = "INSERT"

Reply
11/18/2019 at 01:06 AM

---
