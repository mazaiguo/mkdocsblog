---
title: "Wblock to and zoom in side database"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Database
description: "Here is a sample put together from other DevBlog posts that show how you can Wblock the slected entities into a new database, create there a viewpo..."
author: Autodesk
---
# Wblock to and zoom in side database

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/wblock-to-and-zoom-in-side-database.html

## 文章内容

By Adam Nagy
Here is a sample put together from other DevBlog posts that show how you can Wblock the slected entities into a new database, create there a viewport and zoom it to the extents of the newly added entities.
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.EditorInput
Imports acApp = Autodesk.AutoCAD.ApplicationServices.Application
Imports Autodesk.AutoCAD.Geometry
  Public Class Commands
  <CommandMethod("RunTest")> _
  Public Sub RunTest()
    Using db As Database = CreateDrawing()
      Using tr As Transaction =
        db.TransactionManager.StartTransaction()
          Dim vp As Viewport = CreateViewport(db)
        ZoomExtents(vp)
          tr.Commit()
      End Using
        db.SaveAs("C:\\temp.dwg", DwgVersion.Current)
    End Using
  End Sub
    Public Function CreateDrawing() As Database
    Dim ed As Editor = acApp.DocumentManager.MdiActiveDocument.Editor
      Dim psr As PromptSelectionResult = ed.SelectAll()
    If psr Is Nothing Then Return Nothing
      Dim db As Database = ed.Document.Database
      Dim newDb As New Database(True, True)
    Dim ids As New ObjectIdCollection(psr.Value.GetObjectIds())
    db.Wblock( _
      newDb, ids, New Point3d(), DuplicateRecordCloning.Replace)
      Return newDb
  End Function
    Public Function CreateViewport(ByVal db As Database) As Viewport
    Dim bt As BlockTable =
      db.BlockTableId.GetObject(OpenMode.ForRead)
      Dim ps As BlockTableRecord =
      bt(BlockTableRecord.PaperSpace).GetObject(OpenMode.ForWrite)
      Dim vp As New Viewport()
    vp.Height = 100
    vp.Width = 100
      ps.AppendEntity(vp)
    db.TransactionManager.AddNewlyCreatedDBObject(vp, True)
      Return vp
  End Function
    Public Sub ZoomExtents(ByVal vp As Viewport)
    Dim db As Database = vp.Database
      ' get the screen aspect ratio to calculate 
    ' the height and width 
    Dim mScrRatio As Double
    ' width/height 
    mScrRatio = (vp.Width / vp.Height)
      db.UpdateExt(True)
    Dim mMaxExt As Point3d = db.Extmax
    Dim mMinExt As Point3d = db.Extmin
      Dim mExtents As New Extents3d(mMinExt, mMaxExt)
      ' prepare Matrix for DCS to WCS transformation 
    Dim matWCS2DCS As Matrix3d
    matWCS2DCS = Matrix3d.PlaneToWorld(vp.ViewDirection)
    matWCS2DCS = Matrix3d.Displacement( _
      vp.ViewTarget - Point3d.Origin) * matWCS2DCS
    matWCS2DCS = Matrix3d.Rotation( _
      -vp.TwistAngle, vp.ViewDirection, vp.ViewTarget) * matWCS2DCS
    matWCS2DCS = matWCS2DCS.Inverse()
      ' tranform the extents to the DCS 
    ' defined by the viewdir 
    mExtents.TransformBy(matWCS2DCS)
      ' width of the extents in current view 
    Dim mWidth As Double
    mWidth = (mExtents.MaxPoint.X - mExtents.MinPoint.X)
      ' height of the extents in current view 
    Dim mHeight As Double
    mHeight = (mExtents.MaxPoint.Y - mExtents.MinPoint.Y)
      ' get the view center point 
    Dim mCentPt As New Point2d( _
      ((mExtents.MaxPoint.X + mExtents.MinPoint.X) * 0.5), _
      ((mExtents.MaxPoint.Y + mExtents.MinPoint.Y) * 0.5))
      ' check if the width 'fits' in current window, 
    ' if not then get the new height as 
    ' per the viewports aspect ratio 
    If mWidth > (mHeight * mScrRatio) Then
      mHeight = mWidth / mScrRatio
    End If
      ' set the view height - adjusted by 1% 
    vp.ViewHeight = mHeight * 1.01
    ' set the view center 
    vp.ViewCenter = mCentPt
    vp.Visible = True
    vp.On = True
    vp.UpdateDisplay()
  End Sub
  End Class

## 评论

**内容**: Patrick Emin said...
Ther has been a discussion about that here: http://www.acadnetwork.com/topic-232.0.html
Reply
11/22/2012 at 07:26 AM

---
**内容**: Justin Ralston said...
Adam
Hi I am trying to do what you have done in this post but wait to zoom extents in modelspace of the new drawing.
I have spent hors trying to figure this out and logged a support request with Autodesk with not luck.
Are you able to post a code example on how you would do that.
Regards
Justin Raslton
Reply
06/27/2013 at 03:05 AM

---
