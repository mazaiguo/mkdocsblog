---
title: "Obtaining the Layer States from an External DWG file"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - DWG
  - Layer
description: "Here’s some code which shows how to obtain the LayerStates from an external DWG file using VB.NET"
author: Autodesk
---
# Obtaining the Layer States from an External DWG file

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/obtaining-the-layer-states-from-an-external-dwg-file.html

## 文章内容

by Fenton Webb
Here’s some code which shows how to obtain the LayerStates from an external DWG file using VB.NET
<CommandMethod("GetLayerStates")> _
Public Sub GetLayerStates()
    Dim doc As Document = Application.DocumentManager.MdiActiveDocument
  Dim ed As Editor = doc.Editor
    ' select a dwg file
  Dim openFileDlg As OpenFileDialog
  openFileDlg = New OpenFileDialog("Select DWG File", "fenton.dwg", "dwg", "Select DWG file", 0)
  ' if something was selected
  If openFileDlg.ShowModal() = True Then
      ' extract the file path
    Dim dwgPath As String = openFileDlg.Filename
      ' now get the layer state name
    Dim lsName As PromptResult
    lsName = ed.GetString("Enter Layer State name")
    ' if ok
    If lsName.Status = PromptStatus.OK Then
        ' now open the dwg in a side database
      Using sideDb As Database = New Database(False, True)
        ' read the dwg file
        sideDb.ReadDwgFile(dwgPath, IO.FileShare.Read, False, Nothing)
        ' close the file and make sure we have read everything in
        sideDb.CloseInput(True)
          ' get the layer state manager
        Dim lsManager As LayerStateManager = sideDb.LayerStateManager
          ed.WriteMessage(vbNewLine + "Data for Later State " _
+ lsName.StringResult)
        ed.WriteMessage(vbNewLine + "Mask = " _
+ lsManager.GetLayerStateMask(lsName.StringResult).ToString())
        ' obtain all of the layers for a particular layerstate
        Dim lsLayers As ArrayList = _
lsManager.GetLayerStateLayers(lsName.StringResult, False)
          For Each layer As String In lsLayers
          ed.WriteMessage(vbNewLine + "Layer = " + layer)
        Next
        End Using
    End If
    End If
  End Sub

