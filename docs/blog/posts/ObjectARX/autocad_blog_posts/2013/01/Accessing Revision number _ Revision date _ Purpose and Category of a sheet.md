---
title: "Accessing Revision number / Revision date / Purpose and Category of a sheet"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Unlike the other sheet properties that are accessed using the IAcSmSheet interface, the Revision number, Revision date, Purpose and Category are pr..."
author: Autodesk
---
# Accessing Revision number / Revision date / Purpose and Category of a sheet

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/accessing-revision-number-revision-date-purpose-and-category-of-a-sheet.html

## 文章内容

By Balaji Ramamoorthy
Unlike the other sheet properties that are accessed using the IAcSmSheet interface, the Revision number, Revision date, Purpose and Category are properties defined in the IAcSmSheet2 interface.
Here is a sample code snippet to access those properties :
Imports ACSMCOMPONENTS19Lib
  <CommandMethod("DispSheetDetails")> _
 Public Sub DispSheetDetails()
    Dim dstFile As String
    dstFile = "C:\Temp\MySheetSet.dst"
      Dim mgr As AcSmSheetSetMgr = New AcSmSheetSetMgr()
    Dim db As AcSmDatabase = New AcSmDatabase()
    db = mgr.OpenDatabase(dstFile, False)
      Dim ss As AcSmSheetSet = db.GetSheetSet()
    Dim EnumSheets As IAcSmEnumComponent = ss.GetSheetEnumerator()
      Dim smComponent As IAcSmComponent
    Dim sheet As IAcSmSheet
    Dim sheet2 As IAcSmSheet2
      ' Get the first sheet
    smComponent = EnumSheets.Next()
      While True
        If smComponent Is Nothing Then
            Exit While
        End If
          sheet = TryCast(smComponent, IAcSmSheet)
          ' To access the revision number,
        ' Revision date, Purpose and Category,
        ' cast it as IAcSmSheet2
        sheet2 = TryCast(smComponent, IAcSmSheet2)
        If sheet2 IsNot Nothing Then
            'Revision Number
            Dim revNumber As String
            revNumber = sheet2.GetRevisionNumber()
              'Revision Date
            Dim revDate As String
            revDate = sheet2.GetRevisionDate()
              'Purpose
            Dim purpose As String
            purpose = sheet2.GetIssuePurpose()
              'Category
            Dim cat As String
            cat = sheet2.GetCategory()
        End If
          smComponent = EnumSheets.Next()
    End While
      mgr.Close(db)
End Sub

