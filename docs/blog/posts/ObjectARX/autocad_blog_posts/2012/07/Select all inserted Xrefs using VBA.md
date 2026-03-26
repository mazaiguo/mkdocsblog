---
title: "Select all inserted Xrefs using VBA"
date: 2012-07-01
categories:
  - AutoCAD VBA
tags:
  - Block
  - Selection
  - VBA
  - XREF
description: "What approach can be used to select all Xrefs that are inserted in a drawing using VBA?"
author: Autodesk
---
# Select all inserted Xrefs using VBA

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/select-all-inserted-xrefs-using-vba.html

## 文章内容

By Philippe Leefsma
Q:
What approach can be used to select all Xrefs that are inserted in a drawing using VBA?
A:
The best approach would be to:
1. Iterate through the block definitions to determine if a block is an Xref.
2. Make a list of all such Xref names.
3. Then use a selection set filter with these names to select all those INSERTs.
NOTE: Please introduce necessary error handling.
Sub GetXrefInserts()
    Dim ssBlocks As AcadSelectionSet
    Dim ssTemp As AcadSelectionSet
    Dim col As New Collection
    Dim obj() As Object
    
    Dim GroupCodeArray(0 To 3) As Integer
    Dim GroupValueArray(0 To 3) As Variant
    
    Dim blkdef As AcadBlock
    
    For Each blkdef In ThisDrawing.Blocks
        If blkdef.IsXRef = True Then
            col.Add blkdef.Name
        End If
    Next
    
    Set ssBlocks = ThisDrawing.SelectionSets.Add("ss")
    
    Dim i As Integer
    For i = 1 To col.Count
        Set ssTemp = ThisDrawing.SelectionSets.Add("temp")
        
        GroupCodeArray(0) = -4
        GroupValueArray(0) = "<AND"
        'Entity Type
        GroupCodeArray(1) = 0
        GroupValueArray(1) = "INSERT"
        'Block name
        GroupCodeArray(2) = 2
        GroupValueArray(2) = col.Item(i)
        
        GroupCodeArray(3) = -4
        GroupValueArray(3) = "AND>"
        
        Call ssTemp.Select(acSelectionSetAll, , , GroupCodeArray, GroupValueArray)
        
        Dim cnt As Integer
        cnt = ssTemp.Count
        If cnt > 0 Then
            ReDim obj(0 To cnt - 1) As Object
        End If
        
        Dim k As Integer
        For k = 0 To cnt - 1
            Set obj(k) = ssTemp(k)
        Next
        
        ssBlocks.AddItems obj
        ssTemp.Delete
    
    Next
    
    If ssBlocks.Count <> 0 Then
        MsgBox ssBlocks.Count
    End If
    
    ssBlocks.Delete
End Sub

