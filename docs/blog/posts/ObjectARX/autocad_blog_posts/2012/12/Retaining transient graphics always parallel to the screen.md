---
title: "Retaining transient graphics always parallel to the screen"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - API
  - Dimension
description: "You may be interested in using transient graphics that is always retained parallel to the screen despite of any view changes."
author: Autodesk
---
# Retaining transient graphics always parallel to the screen

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/retaining-transient-graphics-always-parallel-to-the-screen.html

## 文章内容

By Balaji Ramamoorthy
You may be interested in using transient graphics that is always retained parallel to the screen despite of any view changes.
The “Editor.PointToWorld” method can be used to convert a point whose coordinates are known in screen coordinates and obtain its WCS equivalent. This method can be used to compute the points in WCS while we specify the coordinates in DCS.
However, the difficulty in implementing it is to know when the view changed so that you can refresh the transient graphics to follow the view change.
This is because there is no direct way provided by the API to know when the view parameters got changed.
 The object modified event for a viewport table record is only triggered when the view change is performed using the view cube. Pan / zoom using mouse wheel does not trigger it.
As a workaround for this, you may consider using a timer callback to monitor the view parameters and after the view parameters change, use transient graphics to draw parallel to the screen (DCS).
The other way is to use the Editor.PointMonitor event but you may not get this event notification when zoom/pan from the command prompt. After the mouse enters the editor, the transient graphics does get refreshed.
Here is a sample code using the second approach. It draws a rectangle using transient graphics and retains it always parallel to the screen:
using System.Drawing;
using Autodesk.AutoCAD.GraphicsInterface;
  public class TestCommands : IExtensionApplication
{
    public static DBObjectCollection _transients = null;
    public double _viewSize = 1.0;
    public Point3d _viewCtr = Point3d.Origin;
    public Point3d _viewDir = Point3d.Origin;
      [CommandMethod("DrawTransientRect", CommandFlags.Session)]
    public void DrawTransientRectMethod()
    {
        Document activeDoc
            = Application.DocumentManager.MdiActiveDocument;
        Database db = activeDoc.Database;
        Editor ed = activeDoc.Editor;
          // Clear the previous transient graphics
        ClearTransientGraphics();
          Point2d screenSize
            = (Point2d)Application.GetSystemVariable("SCREENSIZE");
          // Width and height of the rectangle
        int width = 20;
        int height = 60;
          // Four corner points in screen coordinates
        System.Drawing.Point upperLeft
                            = new System.Drawing.Point(20, 20);
          System.Drawing.Point upperRight
            = new System.Drawing.Point(upperLeft.X + width, upperLeft.Y);
          System.Drawing.Point lowerLeft
            = new System.Drawing.Point(upperLeft.X, upperLeft.Y + height);
          System.Drawing.Point lowerRight
            = new System.Drawing.Point(upperLeft.X + width, upperLeft.Y + height);
          // Four corner points in WCS
        Point3d upperLeftWorld = ed.PointToWorld(upperLeft, 0);
        Point3d upperRightWorld = ed.PointToWorld(upperRight, 0);
        Point3d lowerLeftWorld = ed.PointToWorld(lowerLeft, 0);
        Point3d lowerRightWorld = ed.PointToWorld(lowerRight, 0);
          // Create the transient entities
        Line l1 = new Line(upperLeftWorld, upperRightWorld);
        l1.ColorIndex = 2;
        Line l2 = new Line(upperRightWorld, lowerRightWorld);
        l2.ColorIndex = 2;
        Line l3 = new Line(lowerRightWorld, lowerLeftWorld);
        l3.ColorIndex = 2;
        Line l4 = new Line(lowerLeftWorld, upperLeftWorld);
        l4.ColorIndex = 2;
          _transients.Add(l1);
        _transients.Add(l2);
        _transients.Add(l3);
        _transients.Add(l4);
          IntegerCollection intCol = new IntegerCollection();
        TransientManager tm = TransientManager.CurrentTransientManager;
        tm.AddTransient
            (
                l1,
                TransientDrawingMode.Main,
                128,
                intCol
            );
          tm.AddTransient
            (
                l2,
                TransientDrawingMode.Main,
                128,
                intCol
            );
          tm.AddTransient
            (
                l3,
                TransientDrawingMode.Main,
                128,
                intCol
            );
          tm.AddTransient
            (
                l4,
                TransientDrawingMode.Main,
                128,
                intCol
            );
    }
      // Erases any transient graphics
    void ClearTransientGraphics()
    {
        TransientManager tm
                = TransientManager.CurrentTransientManager;
        IntegerCollection intCol = new IntegerCollection();
        if (_transients != null)
        {
            foreach (DBObject transient in _transients)
            {
                tm.EraseTransient(
                                    transient,
                                    intCol
                                    );
                transient.Dispose();
            }
            _transients.Clear();
        }
        else
            _transients = new DBObjectCollection();
    }
      #region IExtensionApplication Members
      void IExtensionApplication.Initialize()
    {
        Document activeDoc
            = Application.DocumentManager.MdiActiveDocument;
        Editor ed = activeDoc.Editor;
          // Subscribe to PointMonitor event to refresh
        // transient graphics in case of any view changes.
        ed.PointMonitor +=
                new PointMonitorEventHandler(ed_PointMonitor);
    }
      void ed_PointMonitor(object sender, PointMonitorEventArgs e)
    {
        Document activeDoc = Application.DocumentManager.MdiActiveDocument;
        double viewSize
            = (double)Application.GetSystemVariable("VIEWSIZE");
          Point3d viewCtr
            = (Point3d)Application.GetSystemVariable("VIEWCTR");
          Point3d viewDir
            = (Point3d)Application.GetSystemVariable("VIEWDIR");
          // Simple check to verify if the view parameters changed
        // since we last drew the transient graphics
        if (    viewSize != _viewSize ||
                viewCtr.Equals(_viewCtr) == false ||
                viewDir.Equals(_viewDir) == false
            )
        {
            _viewSize = viewSize;
              _viewCtr
                = (Point3d)Application.GetSystemVariable("VIEWCTR");
              _viewDir = viewDir;
              // Draw the transient graphics again since
            // the view parameters seem to have changed
            DrawTransientRectMethod();
        }
    }
      void IExtensionApplication.Terminate()
    {
        Document activeDoc
            = Application.DocumentManager.MdiActiveDocument;
        if (activeDoc != null)
        {
            // Unsubscribe
            Editor ed = activeDoc.Editor;
            ed.PointMonitor -=
                new PointMonitorEventHandler(ed_PointMonitor);
        }
          // Cleanup before we leave
        ClearTransientGraphics();
    }
      #endregion
}

