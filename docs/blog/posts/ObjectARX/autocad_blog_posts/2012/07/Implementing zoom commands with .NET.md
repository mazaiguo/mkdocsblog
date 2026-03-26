---
title: "Implementing zoom commands with .NET"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "Using the ViewTableRecord object is possible to adjust one view of AutoCAD. This object can used with Editor.SetCurrentView, which will apply the c..."
author: Autodesk
---
# Implementing zoom commands with .NET

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/implementing-zoom-commands-with-net.html

## 文章内容

By Augusto Goncalves
Using the ViewTableRecord object is possible to adjust one view of AutoCAD. This object can used with Editor.SetCurrentView, which will apply the changes to the current visualization.
This sample code contains two commands: zent and zextends. Both sample commands end up using the same custom routine, ZoomToWindow (at the end of this post), but the difference is the data used. The first open any drawing entity, get its bounding box (Geometry Extend) and adjust the view to it. The second get the drawing geometry extension (EXTMAX and EXTMIN variables) information and adjust to view accordantly.
  ' the command for entity
  <CommandMethod("zent")> _
  Public Shared Sub SelectEntityToZoom()
    'select and entity
    Dim ed As Editor = Application. _
      DocumentManager.MdiActiveDocument.Editor
    Dim pes As New PromptEntityOptions("Select an entity: ")
    pes.AllowNone = False
    Dim per As PromptEntityResult = ed.GetEntity(pes)
    If (per.Status <> PromptStatus.OK) Then Return
    'call zoom to entity
    ZoomToEntity(per.ObjectId)
  End Sub
    ' get the information about the entity
  Public Shared Sub ZoomToEntity( _
                  ByVal entityId As ObjectId)
    Dim db As Database = Application. _
      DocumentManager.MdiActiveDocument.Database
    ' start transaction
    Using trans As Transaction = db. _
          TransactionManager.StartTransaction()
      ' get the entity' extends
      Dim ent As Entity = trans.GetObject( _
        entityId, OpenMode.ForRead)
      Dim extends As Extents3d = ent.GeometricExtents
      ' configure the new current view
      ZoomToWindow(New Point2d( _
                     extends.MinPoint.X, _
                     extends.MinPoint.Y), _
                   New Point2d( _
                     extends.MaxPoint.X, _
                     extends.MaxPoint.Y))
      trans.Commit()
    End Using
  End Sub
    ' the command for database extension
  <CommandMethod("zextends")> _
  Public Shared Sub ZoomExtends()
    Dim db As Database = Application. _
      DocumentManager.MdiActiveDocument.Database
    'get the database extension's points
    ZoomToWindow(New Point2d( _
                  db.Extmin.X, db.Extmin.Y), _
                 New Point2d( _
                  db.Extmax.X, db.Extmax.Y))
  End Sub
    ' zoom the current view using
  ' the minPoint and maxPoint
  Public Shared Sub ZoomToWindow( _
            ByVal minPoint As Point2d, _
            ByVal maxPoint As Point2d)
    Dim ed As Editor = Application.DocumentManager. _
      MdiActiveDocument.Editor
    Dim db As Database = Application.DocumentManager. _
      MdiActiveDocument.Database
    'get the current view
    Dim view As ViewTableRecord = ed.GetCurrentView()
    'start transaction
    Using trans As Transaction = db. _
      TransactionManager.StartTransaction()
      'get the entity' extends
      'configure the new current view
      view.Width = maxPoint.X - minPoint.X
      view.Height = maxPoint.Y - minPoint.Y
      view.CenterPoint = New Point2d( _
        minPoint.X + (view.Width / 2), _
        minPoint.Y + (view.Height / 2))
      'update the view
      ed.SetCurrentView(view)
      trans.Commit()
    End Using
  End Sub

## 评论

**内容**: Christian Blei said...
Hello Augusto,
this is only currect, if the current view is not inclined and rotated, i.e. its ucs is equivalent to WCS..
As far as I remember there is an example what to do for the general case of the current view in the .Net developer's guide introduction.
Christian
Reply
07/07/2012 at 12:49 AM

---
**内容**: Augusto Goncalves said in reply to Christian Blei...
Hi Christian,
Yes there is a sample there, just a little more complex. Thanks for pointing out, here is the link: http://exchange.autodesk.com/autocad/enu/online-help/search#WS1a9193826455f5ff2566ffd511ff6f8c7ca-4363.htm
Cheers,
Augusto
Reply
07/10/2012 at 06:03 AM

---
