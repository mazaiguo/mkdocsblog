---
title: "Iterating through line type and text styles"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Database
  - Unicode
description: "Here is a VB.NET example that gets the available linetypes and text style table names"
author: Autodesk
---
# Iterating through line type and text styles

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/iterating-through-line-type-and-text-styles.html

## 文章内容

By Virupaksha Aithal
Here is a VB.NET example that gets the available linetypes and text style table names
<CommandMethod("VBLT")> _
    Public Sub VBLT()
            Dim doc As Document = _
                        Application.DocumentManager.MdiActiveDocument
            Dim db As Database = _
                        doc.Database
            Dim tm As Transaction = _
                            db.TransactionManager.StartTransaction()
              Dim ed As Editor = doc.Editor
            Using tm
                Dim tmpObj As DBObject = _
                  tm.GetObject(db.LinetypeTableId, OpenMode.ForRead)
                Dim tbl As SymbolTable = CType(tmpObj, SymbolTable)
                If Not (tbl Is Nothing) Then
                    Dim tblRecId As ObjectId
                    For Each tblRecId In tbl
                        Dim tmpObj1 As DBObject = _
                            tm.GetObject(tblRecId, OpenMode.ForRead)
                          Dim rec As SymbolTableRecord = _
                                CType(tmpObj1, LinetypeTableRecord)
                        If Not (rec Is Nothing) Then
                            ed.WriteMessage("Adding LineType " _
                                                & rec.Name & vbCrLf)
                        End If
                    Next
                End If
                Dim tmpObj12 As DBObject = _
                    tm.GetObject(db.TextStyleTableId, _
                                                OpenMode.ForRead)
                Dim tbl1 As SymbolTable = _
                                        CType(tmpObj12, SymbolTable)
                  If Not (tbl1 Is Nothing) Then
                    Dim tblRecId1 As ObjectId
                    For Each tblRecId1 In tbl1
                        Dim tmpObj2 As DBObject = _
                             tm.GetObject(tblRecId1, _
                                                OpenMode.ForRead)
                        Dim rec As SymbolTableRecord = _
                                   CType(tmpObj2,  _
                                                TextStyleTableRecord)
                        If Not (rec Is Nothing) Then
                            ed.WriteMessage("Adding Text Style " _
                                                & rec.Name & vbCrLf)
                        End If
                    Next
                End If
            End Using
        End Sub

