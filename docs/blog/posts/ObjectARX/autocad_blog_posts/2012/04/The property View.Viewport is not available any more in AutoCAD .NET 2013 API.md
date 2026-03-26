---
title: "The property View.Viewport is not available any more in AutoCAD .NET 2013 API"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Dimension
  - Unicode
description: "The property Autodesk.AutoCAD.GraphicsSystem.View.Viewport has been removed from the AutoCAD .NET 2013 API. You can use the Autodesk.AutoCAD.Graphi..."
author: Autodesk
---
# The property View.Viewport is not available any more in AutoCAD .NET 2013 API

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/the-property-viewviewport-is-not-available-any-more-in-autocad-net-2013-api.html

## 文章内容

By Gopinath Taget
The property Autodesk.AutoCAD.GraphicsSystem.View.Viewport has been removed from the AutoCAD .NET 2013 API. You can use the Autodesk.AutoCAD.GraphicsSystem.View.ViewportExtents property instead.
There is  a little difference between these two properties though:
 Viewport property returned the extents of the viewport in device coordinates (pixels), but ViewportExtents property returns the extents of the viewport in normalized device coordinates.
What does normalized device coordinates mean? In this context, it means that the viewport extents are normalized against the size of the device object containing the viewport. So the approach to get the proper viewport size is as follows:
Device dev = view.Device;
System.Drawing.Size s = dev.Size;  //container or window size
Extents2d extents = view.ViewportExtents;
  Point2d min_pt = new Point2d(extents.MinPoint.X * s.Width,
    extents.MinPoint.Y * s.Height);
Point2d max_pt = new Point2d(extents.MaxPoint.X * s.Width,
    extents.MaxPoint.Y * s.Height);
  System.Drawing.Rectangle view_rect =
    new System.Drawing.Rectangle(
        (int)min_pt.X,
        (int)min_pt.Y,
        (int)System.Math.Abs(max_pt.X - min_pt.X),
        (int)System.Math.Abs(max_pt.Y - min_pt.Y));

## 评论

**内容**: Ilya Solovyev said...
Device dev = view.Device;
System.Drawing.Size s = dev.Size; //container or window size
The Device class doesn't contain property Size
Reply
01/13/2014 at 02:40 AM

---
**内容**: AlexFielder said in reply to Ilya Solovyev...
I've hit this same snag in AutoCAD 2014 just this week.
In VB I've been trying to use the following:
Dim s As Size = New Size(gsm.DeviceIndependentDisplaySize.Width, gsm.DeviceIndependentDisplaySize.Height)
without success. :(
perhaps it's worth an updated article?
Reply
03/20/2014 at 10:04 AM

---
**内容**: AlexFielder said...
Actually, In a typical case of http://en.wikipedia.org/wiki/Rubber_duck_debugging I modified my code to include a multiplication of the view.ViewPortExtents min & max values by the s value I posted above and lo & behold it now works:
Private Shared Function ScreenShotToFile(pt1 As Point3d, pt2 As Point3d, filename As String) As String
Dim doc As Document = Application.DocumentManager.MdiActiveDocument
Dim db As Database = doc.Database
Dim ed As Editor = doc.Editor
Dim cvport = CShort(Application.GetSystemVariable("CVPORT"))
Dim width As Double = CDbl(pt2.X - pt1.X)
Dim height As Double = CDbl(pt2.Y - pt1.Y)
Dim img As System.Drawing.Image
Dim view As ViewTableRecord = ed.GetCurrentView()
'start transaction
Using trans As Transaction = db. _
TransactionManager.StartTransaction()
'get the entity' extends
'configure the new current view
view.Width = pt2.X - pt1.X
view.Height = pt2.Y - pt1.Y
view.CenterPoint = New Point2d( _
pt1.X + (view.Width / 2), _
pt1.Y + (view.Height / 2))
'update the view
ed.SetCurrentView(view)
trans.Commit()
End Using
Using tr As Transaction = doc.TransactionManager.StartTransaction()
Dim vst As GraphicsInterface.VisualStyleType = GraphicsInterface.VisualStyleType.Basic
Dim gsm As GraphicsSystem.Manager = doc.GraphicsManager
Using gfxview As GraphicsSystem.View = New GraphicsSystem.View
gsm.SetViewFromViewport(gfxview, cvport)
gfxview.VisualStyle = New GraphicsInterface.VisualStyle(vst)
Using dev As GraphicsSystem.Device = gsm.CreateAutoCADOffScreenDevice()
Dim s As Size = New Size(gsm.DeviceIndependentDisplaySize.Width, gsm.DeviceIndependentDisplaySize.Height)
Dim sz As New Size(Math.Abs(pt1.X - pt2.X), Math.Abs(pt1.Y - pt2.Y))
dev.OnSize(s)
dev.DeviceRenderType = GraphicsSystem.RendererType.Default
dev.BackgroundColor = Color.White
dev.Add(gfxview)
dev.Update()
Using model As GraphicsSystem.Model = gsm.CreateAutoCADModel
Using trans As Transaction = doc.TransactionManager.StartTransaction()
Dim bt As BlockTable = trans.GetObject(doc.Database.BlockTableId, OpenMode.ForRead)
Dim btr As BlockTableRecord = trans.GetObject(bt(BlockTableRecord.PaperSpace), OpenMode.ForRead)
gfxview.Add(btr, model)
trans.Commit()
End Using
Dim extents As Extents2d = gfxview.ViewportExtents
Dim min_pt As New Point2d(extents.MinPoint.X * s.Width, extents.MinPoint.Y * s.Height)
Dim max_pt As New Point2d(extents.MaxPoint.X * s.Width, extents.MaxPoint.Y * s.Height)
Dim view_rect As New System.Drawing.Rectangle(CInt(min_pt.X), _
CInt(min_pt.Y), _
CInt(System.Math.Abs(max_pt.X - min_pt.X)), _
CInt(System.Math.Abs(max_pt.Y - min_pt.Y)))
img = gfxview.GetSnapshot(view_rect)
Dim processed As Bitmap = img
If filename IsNot Nothing AndAlso filename <> "" Then
processed.Save(filename, ImageFormat.Png)
ed.WriteMessage(vbCrLf & "Image captured and saved to ""{0}"".", filename)
End If
'cleanup
processed.Dispose()
gfxview.EraseAll()
dev.Erase(gfxview)
End Using
End Using
End Using
tr.Commit()
End Using
Return filename
End Function
Reply
03/20/2014 at 10:17 AM

---
