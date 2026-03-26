---
title: "Creating a Selection Set using COM Interop"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - COM
  - COM Interop
  - Selection
description: "I'm migrating my VBA code to VB.NET and getting an exception in the AcadSelectionSet.Select(). What am I doing wrong?"
author: Autodesk
---
# Creating a Selection Set using COM Interop

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/creating-a-selection-set-using-com-interop.html

## 文章内容

By Marat Mirgaleev
Issue
I'm migrating my VBA code to VB.NET and getting an exception in the AcadSelectionSet.Select(). What am I doing wrong?
Solution
This is a sample how to select all entities on a given layer:
Dim FilterType(0) As Int16 ' IMPORTANT: The type must be Int16,
                           ' otherwise you'll get an exception!
Dim FilterData(0) As Object
Dim objSS As Autodesk.AutoCAD.Interop.AcadSelectionSet = Nothing
  Try
    FilterType(0) = 8
        ' Will select all entities with the given Layer name
    FilterData(0) = "MyLayer"  ' It's the layer name
      Dim acadApp As Autodesk.AutoCAD.Interop.AcadApplication = _
         Autodesk.AutoCAD.ApplicationServices.
         Application.AcadApplication
    objSS = acadApp.Documents.Application.ActiveDocument.
         SelectionSets.Add("MySet")
    objSS.Clear()
    objSS.Select(
        Autodesk.AutoCAD.Interop.Common.AcSelect.acSelectionSetAll, _
        , , FilterType, FilterData)
    objSS.Highlight(True)
      MsgBox(objSS.Count & " entities selected.")
  Catch ex As Exception
    MsgBox(ex.Message)
Finally
    If Not objSS Is Nothing Then
        objSS.Delete()
    End If
End Try

## 评论

**内容**: Jorge Renatto said...
Regards,
Maybe someone can help me solve my problem.
I wonder why this code does not work when working with AutoCAD 2013:
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.Interop
Imports Autodesk.AutoCAD.Interop.Common
Public Class Class1
Public ReadOnly Property ThisDrawing() As AcadDocument
Get
Return Autodesk.AutoCAD.ApplicationServices.Application. _
DocumentManager.MdiActiveDocument.acaddocument
End Get
End Property
Public Sub COMANDO()
Thisdrawing.Utility.Prompt("Hola mundo")
End Sub
End Class

I wonder if the way we work with INTEROP, and INTEROP.COMMON, has changed in AutoCAD 2013, and if so, what would be the new way of working with these references?.
Reply
07/22/2013 at 08:41 AM

---
