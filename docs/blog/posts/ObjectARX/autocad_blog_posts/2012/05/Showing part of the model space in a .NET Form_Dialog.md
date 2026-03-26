---
title: "Showing part of the model space in a .NET Form/Dialog"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "I would like to show a certain part of the model space in my .NET Form. Is it possible?"
author: Autodesk
---
# Showing part of the model space in a .NET Form/Dialog

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/showing-part-of-the-model-space-in-a-net-formdialog.html

## 文章内容

By Adam Nagy
I would like to show a certain part of the model space in my .NET Form. Is it possible?
Solution
Yes it is.
In the following sample I created a Form called ViewForm and placed a Panel on it called ViewPanel, then used the following code to show a certain part of the model space on it:
Imports acApp = Autodesk.AutoCAD.ApplicationServices.Application
Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.GraphicsSystem
Imports GI = Autodesk.AutoCAD.GraphicsInterface
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.Geometry
  Public Class ViewForm
  Dim device As Device
  Dim view As View
  Dim model As Model
    Private Sub Form_OnLoad( _
  ByVal sender As System.Object, _
  ByVal e As System.EventArgs) _
  Handles MyBase.Load
      Dim doc As Document = acApp.DocumentManager.MdiActiveDocument
    Dim db As Database = doc.Database
    Dim gsm As Manager = doc.GraphicsManager
    ' Create a device that will draw into our panel
    device = gsm.CreateAutoCADDevice(ViewPanel.Handle)
    ' Create a view and add it to the device
    view = New View
    device.Add(view)
    device.Update()
      Using tr As Transaction = _
      db.TransactionManager.StartTransaction()
        model = gsm.CreateAutoCADModel()
      Dim bt As BlockTable = _
        tr.GetObject(db.BlockTableId, OpenMode.ForRead)
      Dim ms As BlockTableRecord = _
        tr.GetObject( _
          bt(BlockTableRecord.ModelSpace), OpenMode.ForRead)
      ' Add the model space to the view
      view.Add(ms, model)
      ' Make sure that the area that you want to show
      ' lies between these two points
      view.ZoomExtents( _
        New Point3d(-10, -10, 0), New Point3d(200, 200, 0))
      ' In case you want to show some solids in shaded mode
      view.Mode = _
        Autodesk.AutoCAD.GraphicsSystem.RenderMode.GouraudShaded
      view.VisualStyle = _
        New GI.VisualStyle(GI.VisualStyleType.GouraudWithEdges)
      ' Just to make sure that not perspective but parallel
      ' mode is used
      view.SetView(view.Position, view.Target, _
        view.UpVector, view.FieldWidth, _
        view.FieldHeight, Projection.Parallel)
    End Using
    End Sub
    Private Sub Panel_OnPaint( _
  ByVal sender As System.Object, _
  ByVal e As System.Windows.Forms.PaintEventArgs) _
  Handles ViewPanel.Paint
      ' Redraw the view
    view.Invalidate()
    view.Update()
    End Sub
    Private Sub Form_OnClosing( _
  ByVal sender As System.Object, _
  ByVal e As System.Windows.Forms.FormClosingEventArgs) _
  Handles MyBase.FormClosing
      ' Call dispose to free the underlying ObjectARX objects
    device.Dispose()
    view.Dispose()
    model.Dispose()
    End Sub
End Class
If you'd like to see a more comprehensive solution then please have a look at the BlockView.NET sample project

