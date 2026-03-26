---
title: "Viewport specific implementation of AutoCAD ISOLATEOBJECTS command with a Drawable Overrule in .Net"
date: 2012-12-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
description: "Credit: This article was originally created by Philippe Leefsma."
author: Autodesk
---
# Viewport specific implementation of AutoCAD ISOLATEOBJECTS command with a Drawable Overrule in .Net

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/viewport-specific-implementation-of-autocad-isolateobjects-command-with-a-drawable-overrule-in-net.html

## 文章内容

By Gopinath Taget
Credit: This article was originally created by Philippe Leefsma.
Unfortunately there is no simple API to replicate the ISOLATEOBJECTS command. You will have to jump through some hoops.
One way to reach this goal is to use a drawable overrule that will control the visibility of the entities depending which viewport they are drawn in.
The following VB.Net sample illustrates the approach: each entity’s visibility can be controlled on a per-viewport basis. The overrule can be switched ON and OFF with the "ToggleIsolateOverrule" command. Also the overrule can be persisted across sessions as the overrule data is stored in an xRecord of the extension dictionary of each entity. However, as the overrule must be attached to each specific entity type, it may be necessary to run command "ReloadIsolateOverrule" for a specific drawing in order to reactivate the overrule for the entity type it contains.
Imports System
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.Geometry
Imports Autodesk.AutoCAD.EditorInput
Imports Autodesk.AutoCAD.GraphicsInterface
  '////////////////////////////////////////////////////////////////////////////////////////////////
'// Use: Creates a draw overrule in order to isolate selected object(s) in the active viewport.
'//      Written by Philippe Leefsma - DevTech, November 2010
'//
'////////////////////////////////////////////////////////////////////////////////////////////////
Public Class CIsolateOverrule
    Inherits DrawableOverrule
    Implements IExtensionApplication
      Private Shared _TheOverrule As CIsolateOverrule
      Private Shared _dictName As String = "IsolateOverrulexDic"
      Private Shared _viewportsNumKey As String = "IsolateOverrulexRec"
      '////////////////////////////////////////////////////////////////////////////////////////////////
    '// Use: IExtensionApplication Implementation
    '//     
    '////////////////////////////////////////////////////////////////////////////////////////////////
    Public Sub Initialize() Implements Autodesk.AutoCAD.Runtime.
      IExtensionApplication.Initialize
          If _TheOverrule Is Nothing Then
              _TheOverrule = New CIsolateOverrule
            _TheOverrule.SetExtensionDictionaryEntryFilter(_dictName)
              AddHandler Application.SystemVariableChanged,
              AddressOf SystemVariableChanged
          End If
      End Sub
      Public Sub Terminate() Implements Autodesk.AutoCAD.Runtime.
      IExtensionApplication.Terminate
      End Sub
      '////////////////////////////////////////////////////////////////////////////////////////////////
    '// Use: SystemVariableChanged Handler Implementation
    '//     
    '////////////////////////////////////////////////////////////////////////////////////////////////
    Private Shared Sub SystemVariableChanged(ByVal sender As Object,_
                                             ByVal e As
                                             Autodesk.AutoCAD.
                                             ApplicationServices.
                                            SystemVariableChangedEventArgs)
        If (e.Name.ToUpper() = "CVPORT") Then
              Dim doc As Document =
            Application.DocumentManager.MdiActiveDocument
               Dim cvport As Short =
            Application.GetSystemVariable("CVPORT")
              doc.Editor.WriteMessage(vbCrLf +
                "Current Viewport is now: " +
                cvport.ToString() + vbCrLf)
              doc.Editor.Regen()
          End If
      End Sub
      '////////////////////////////////////////////////////////////////////////////////////////////////
    '// Use: Utilities Implementation
    '//     
    '////////////////////////////////////////////////////////////////////////////////////////////////
    Private Shared Function GetxDico(ByVal entity As Entity, _
                                     ByVal Tx As Transaction, _
                                     Optional ByVal createIfNotExists
                                   As Boolean = True) As DBDictionary
          If (entity.ExtensionDictionary = ObjectId.Null) Then
              If Not createIfNotExists Then
                Return Nothing
            End If
              entity.UpgradeOpen()
            entity.CreateExtensionDictionary()
            entity.DowngradeOpen()
        End If
          Dim xDico As DBDictionary = Tx.GetObject(
                                       entity.ExtensionDictionary,
                                                 OpenMode.ForWrite)
          xDico.TreatElementsAsHard = False
          Return xDico
      End Function
      Private Shared Sub AddOverruleData(ByVal entity As Entity, _
                                       ByVal viewportNum As Short, _
                                       ByVal spaceId As ObjectId, _
                                       ByVal Tx As Transaction)
          Dim xDico As DBDictionary = GetxDico(entity, Tx)
          Dim overruleDico As DBDictionary
        Dim xRec As Xrecord
          If (Not xDico.Contains(_dictName)) Then
              overruleDico = New DBDictionary()
            overruleDico.TreatElementsAsHard = True
              xDico.SetAt(_dictName, overruleDico)
              xRec = New Xrecord()
              'Add a first {Viewport, Id} pair,
            ‘but first add a dummy pair {0, spaceId}
            'This will prevent a crash during
            ‘RemoveOverruleData if we remove the last
            'pair and the xRecord.Data is left empty...
            xRec.Data = New ResultBuffer(New TypedValue(
                                        DxfCode.Int32, 0), _
                                         New TypedValue(
                                        DxfCode.SoftPointerId,
                                        spaceId), _
                                         New TypedValue(
                                         DxfCode.Int32,
                                         viewportNum), _
                                         New TypedValue(
                                         DxfCode.SoftPointerId,
                                         spaceId))
              overruleDico.SetAt(_viewportsNumKey, xRec)
              Tx.AddNewlyCreatedDBObject(overruleDico, True)
            Tx.AddNewlyCreatedDBObject(xRec, True)
          Else
              overruleDico = Tx.GetObject(xDico.GetAt(_dictName),
                                        OpenMode.ForRead)
              xRec = Tx.GetObject(overruleDico.GetAt(_viewportsNumKey),
                                OpenMode.ForWrite)
              Dim data As New System.Collections.Generic.List(
            Of TypedValue)(
              xRec.Data.AsArray())
              data.Add(New TypedValue(DxfCode.Int32, viewportNum))
            data.Add(New TypedValue(DxfCode.SoftPointerId, spaceId))
              xRec.Data = New ResultBuffer(data.ToArray())
          End If
      End Sub
      Private Shared Sub RemoveOverruleData(ByVal entity As Entity, _
                                        ByVal viewportNum As Short, _
                                        ByVal spaceId As ObjectId, _
                                          ByVal Tx As Transaction, _
                                       Optional ByVal removeDict As _
                                          Boolean = False)
          Dim xDico As DBDictionary = GetxDico(entity, Tx, False)
          If xDico = Nothing Then
            'Seems there is nothing to remove, just leave...
            Return
        End If
          If Not (xDico.Contains(_dictName)) Then
            'Seems there is nothing to remove, just leave...
            Return
        End If
          Dim overruleDico As DBDictionary = Tx.GetObject(
            xDico.GetAt(_dictName), OpenMode.ForRead)
          If removeDict Then
              overruleDico.UpgradeOpen()
            xDico.Remove(_dictName)
            overruleDico.Erase(True)
          Else
              Dim xRec As Xrecord = Tx.GetObject(
                overruleDico.GetAt(_viewportsNumKey),
                OpenMode.ForWrite)
              Dim data As New System.Collections.Generic.List(
                   Of TypedValue)(xRec.Data.AsArray())
              For idx As Integer = 0 To data.Count - 1 Step 2
                  If data.Item(idx).Value =
                  viewportNum And data.Item(idx + 1).Value =
                  spaceId Then
                    xRec.UpgradeOpen()
                    data.RemoveAt(idx)
                    data.RemoveAt(idx)
                    xRec.Data = New ResultBuffer(data.ToArray())
                    Return
                End If
              Next
          End If
      End Sub
      Private Shared Function IsOverruled(ByVal entity As Entity, _
                                        ByVal Tx As Transaction) As Boolean
          Dim xDico As DBDictionary = GetxDico(entity, Tx, False)
          If xDico = Nothing Then
            Return False
        End If
          Return xDico.Contains(_dictName)
      End Function
      Private Shared Sub RegenOverruledEntities()
          Dim doc As Document =
        Application.DocumentManager.MdiActiveDocument
        Dim db As Database = doc.Database
        Dim ed As Editor = doc.Editor
          Using Tx As Transaction =
        db.TransactionManager.StartTransaction
              Dim bt As BlockTable = Tx.GetObject(db.BlockTableId,
                                               OpenMode.ForRead)
            Dim btr As BlockTableRecord = Tx.GetObject(
              bt(BlockTableRecord.ModelSpace), OpenMode.ForRead)
              For Each id As ObjectId In btr
                  Dim entity As Entity = Tx.GetObject(id,
                                       OpenMode.ForRead)
                  If IsOverruled(entity, Tx) Then
                      entity.UpgradeOpen()
                    entity.RecordGraphicsModified(True)
                  End If
              Next
              Tx.Commit()
          End Using
          doc.Editor.Regen()
      End Sub
      Private Shared ReadOnly Property CurrentSpaceId() As ObjectId
        Get
            Dim db As Database =
              HostApplicationServices.WorkingDatabase
              If (db.TileMode) Then
                  'If model space returns Database.CurrentSpaceId
                Return db.CurrentSpaceId
              Else
                  'If paper space returns current layout Id
                Dim layoutMng As LayoutManager =
                                         LayoutManager.Current()
                Return layoutMng.GetLayoutId(layoutMng.CurrentLayout)
              End If
        End Get
    End Property
      Private Shared Sub ReloadOverrule()
          Dim doc As Document =
                   Application.DocumentManager.MdiActiveDocument
        Dim db As Database = doc.Database
        Dim ed As Editor = doc.Editor
          Using Tx As Transaction =
                         db.TransactionManager.StartTransaction
              Dim bt As BlockTable = Tx.GetObject(
              db.BlockTableId, OpenMode.ForRead)
            Dim btr As BlockTableRecord = Tx.GetObject(
              bt(BlockTableRecord.ModelSpace), OpenMode.ForRead)
              For Each id As ObjectId In btr
                  Try
                      Dim entity As Entity = Tx.GetObject(id,
                          OpenMode.ForRead)
                      If (IsOverruled(entity, Tx)) Then
                        entity.UpgradeOpen()
                        entity.RecordGraphicsModified(True)
                        Overrule.AddOverrule(RXClass.GetClass(
                                             entity.GetType()),
                                             _TheOverrule,
                                             False)
                    End If
                  Catch ex As Autodesk.AutoCAD.Runtime.Exception
                      If ex.ErrorStatus <>
                       ErrorStatus.DuplicateKey Then
                        ed.WriteMessage(
                          vbCrLf +
                          "Exception occured when adding overrule: " +
                           vbCrLf + ex.Message)
                        Exit Sub
                    End If
                  End Try
              Next id
              Tx.Commit()
          End Using
      End Sub
      '////////////////////////////////////////////////////////////////////////////////////////////////
    '// Use: DrawableOverrule Implementation
    '//     
    '////////////////////////////////////////////////////////////////////////////////////////////////
    Public Overrides Function WorldDraw(
    ByVal drawable As Autodesk.AutoCAD.GraphicsInterface.Drawable, _
    ByVal wd As Autodesk.AutoCAD.GraphicsInterface.WorldDraw
    ) As Boolean
        Return False
    End Function
      Public Overrides Sub ViewportDraw(
    ByVal drawable As Autodesk.AutoCAD.GraphicsInterface.Drawable, _
    ByVal vd As Autodesk.AutoCAD.GraphicsInterface.ViewportDraw)
          Dim doc As Document =      
        Application.DocumentManager.MdiActiveDocument
          'Read the Xrecord data section and check
        'if our overruled entity has to be hidden
        'in the currently drawn viewport.
        'Need to compare it to current space Id as well...
        Using Tx As Transaction =
          doc.Database.TransactionManager.StartTransaction
              Dim xDico As DBDictionary = GetxDico(drawable, Tx)
              Dim overruleDico As DBDictionary =
              Tx.GetObject(xDico.GetAt(_dictName), OpenMode.ForRead)
              Dim xRec As Xrecord =
              Tx.GetObject(overruleDico.GetAt(_viewportsNumKey),
                           OpenMode.ForRead)
              Dim iter As ResultBufferEnumerator =
              xRec.Data.GetEnumerator()
              While iter.MoveNext
                  If (vd.Viewport.AcadWindowId =
                    iter.Current.Value) Then
                      'Check spaceId now 
                    iter.MoveNext()
                      If (CurrentSpaceId = iter.Current.Value) Then
                          'Our guy needs to be hidden in that viewport
                        'so get out of here and do nothing...
                        Tx.Commit()
                        Return
                    End If
                      Continue While
                  End If
                  'Skip spaceId data
                iter.MoveNext()
              End While
              Tx.Commit()
          End Using
          'If we got to this point, it means overruled
        'entity is not hidden in this specific viewport...
        Dim clone As Entity = drawable.Clone
        vd.Geometry.Draw(clone)
        clone.Dispose()
      End Sub
      Public Overrides Function SetAttributes(
  ByVal drawable As Autodesk.AutoCAD.GraphicsInterface.Drawable, _
  ByVal traits As Autodesk.AutoCAD.GraphicsInterface.DrawableTraits
  ) _
  As Integer
          'Returning "DrawableAttributes.RegenDraw"
        ' here will force viewport regen, it also impacts perfs...
        Dim ret As Integer = MyBase.SetAttributes(drawable, traits) _
                                Or DrawableAttributes.RegenDraw _
                                Or DrawableAttributes.IsAnEntity _
                              Or DrawableAttributes.IsCompoundObject
        Return ret
      End Function
      Public Overrides Function ViewportDrawLogicalFlags(
     ByVal drawable As Autodesk.AutoCAD.GraphicsInterface.Drawable, _
      ByVal vd As Autodesk.AutoCAD.GraphicsInterface.ViewportDraw) As Integer
          Dim ret As Integer =
        MyBase.ViewportDrawLogicalFlags(drawable, vd)
          Return ret
      End Function
      '////////////////////////////////////////////////////////////////////////////////////////////////
    '// Use: Commands
    '//     
    '////////////////////////////////////////////////////////////////////////////////////////////////
     <CommandMethod("IsolateOverrule")> _
    Public Shared Sub IsolateOverrule()
          Dim doc As Document =
        Application.DocumentManager.MdiActiveDocument
        Dim db As Database = doc.Database
        Dim ed As Editor = doc.Editor
          Dim pso As New PromptSelectionOptions()
        pso.RejectObjectsFromNonCurrentSpace = True
        pso.MessageForAdding = vbCrLf +
      "Select entities to isolate: "
          Dim psr As PromptSelectionResult = ed.GetSelection(pso)
          If (psr.Status <> PromptStatus.OK) Then
            Return
        End If
          Dim cvport As Short = Application.GetSystemVariable("CVPORT")
          'Creates an ObjectIdCollection to
        'make it easier with use of "contains" method
        Dim selectedIds As New ObjectIdCollection(
                         psr.Value.GetObjectIds())
          Using Tx As Transaction =
             db.TransactionManager.StartTransaction
              Dim bt As BlockTable = Tx.GetObject(db.BlockTableId,
                                                OpenMode.ForRead)
            Dim btr As BlockTableRecord = Tx.GetObject(
              bt(BlockTableRecord.ModelSpace), OpenMode.ForRead)
              For Each id As ObjectId In btr
                  Try
                      Dim entity As Entity = Tx.GetObject(id,
                                           OpenMode.ForRead)
                      'Only selected entities are not overruled
                    If selectedIds.Contains(id) Then
                                  RemoveOverruleData(entity, cvport,
                                        CurrentSpaceId, Tx)
                      Else
                          AddOverruleData(entity, cvport,
                                    CurrentSpaceId, Tx)
                          Overrule.AddOverrule(
                          RXClass.GetClass(entity.GetType()),
                          _TheOverrule,
                          False)
                      End If
                  Catch ex As Autodesk.AutoCAD.Runtime.Exception
                      If ex.ErrorStatus <>
                       ErrorStatus.DuplicateKey Then
                        ed.WriteMessage(
                          vbCrLf +
                         "Exception occured when adding overrule: " +
                          vbCrLf + ex.Message)
                        Exit Sub
                    End If
                  End Try
              Next id
              Tx.Commit()
          End Using
          CIsolateOverrule.Overruling = True
          RegenOverruledEntities()
      End Sub
    <CommandMethod("ToggleIsolateOverrule")> _
    Public Shared Sub ToggleIsolateOverrule()
          Dim doc As Document =
                Application.DocumentManager.MdiActiveDocument
        Dim db As Database = doc.Database
        Dim ed As Editor = doc.Editor
          CIsolateOverrule.Overruling = Not CIsolateOverrule.Overruling
          If (CIsolateOverrule.Overruling) Then
            doc.Editor.WriteMessage(vbLf +
                                    "IsolateOverrule is now ON" +
                                    vbCrLf)
        Else
            doc.Editor.WriteMessage(vbLf +
                                    "IsolateOverrule is now OFF" +
                                    vbCrLf)
        End If
          RegenOverruledEntities()
      End Sub
    <CommandMethod("CleanIsolateOverrule")> _
    Public Shared Sub CleanIsolateOverrule()
          Dim doc As Document =
             Application.DocumentManager.MdiActiveDocument
        Dim db As Database = doc.Database
        Dim ed As Editor = doc.Editor
          Using Tx As Transaction =
          db.TransactionManager.StartTransaction
              Dim bt As BlockTable = Tx.GetObject(
              db.BlockTableId, OpenMode.ForRead)
            Dim btr As BlockTableRecord = Tx.GetObject(
              bt(BlockTableRecord.ModelSpace), OpenMode.ForRead)
              For Each id As ObjectId In btr
                  Dim entity As Entity = Tx.GetObject(id,
                                   OpenMode.ForRead)
                  RemoveOverruleData(entity, 0, ObjectId.Null, Tx,
                                    True)
              Next
              Tx.Commit()
          End Using
          doc.Editor.Regen()
      End Sub
    <CommandMethod("ReloadIsolateOverrule")> _
    Public Shared Sub ReloadIsolateOverrule()
          Dim doc As Document =
        Application.DocumentManager.MdiActiveDocument
          ReloadOverrule()
          CIsolateOverrule.Overruling = True
          doc.Editor.Regen()
      End Sub
  End Class

