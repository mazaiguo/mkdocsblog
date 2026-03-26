---
title: "Layout View that shows in SheetSet Manager"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "For a layout view which is created using the API to show up in the SheetSet Manager user interface, the created view must be associated with its la..."
author: Autodesk
---
# Layout View that shows in SheetSet Manager

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/layout-view-that-shows-in-sheetset-manager-.html

## 文章内容

By Balaji Ramamoorthy
For a layout view which is created using the API to show up in the SheetSet Manager user interface, the created view must be associated with its layout.  
Here is a sample code to create layout view :
Private _viewName As String
  Public Sub CreateLayoutView()
    Dim doc As Document = Application.DocumentManager.MdiActiveDocument
    Dim db As Database = doc.Database
    Dim ed As Editor = doc.Editor
      Using Tx As Transaction = db.TransactionManager.StartTransaction()
        Dim vt As ViewTable = TryCast(Tx.GetObject(db.ViewTableId, OpenMode.ForRead), ViewTable)
          If Not vt.Has(_viewName) Then
            Dim min2d As Point2d = DirectCast(Application.GetSystemVariable("LIMMIN"), Point2d)
            Dim max2d As Point2d = DirectCast(Application.GetSystemVariable("LIMMAX"), Point2d)
              Dim newView As New ViewTableRecord()
              newView.CenterPoint = min2d + (max2d - min2d) * 0.5
              newView.Height = max2d.Y - min2d.Y
            newView.Width = max2d.X - min2d.X
            newView.ViewDirection = New Vector3d(0, 0, 1)
            newView.SetUcsToWorld()
            newView.Name = _viewName
            newView.IsPaperspaceView = True
              vt.UpgradeOpen()
              Dim viewId As ObjectId = vt.Add(newView)
              Dim layManager As LayoutManager = LayoutManager.Current
            Dim layoutId As ObjectId = layManager.GetLayoutId(layManager.CurrentLayout)
            newView.Layout = layoutId
              Tx.AddNewlyCreatedDBObject(newView, True)
        End If
        Tx.Commit()
    End Using
End Sub

