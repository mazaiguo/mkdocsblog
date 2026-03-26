---
title: "Continuous orbit around an entity"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Here is a sample code to orbit around a selected entity. After zooming-in on the selected entity and setting the view to an orthographic view, a fu..."
author: Autodesk
---
# Continuous orbit around an entity

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/continuous-orbit-around-an-entity.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to orbit around a selected entity. After zooming-in on the selected entity and setting the view to an orthographic view, a full 360 degrees orbit is performed around the entity. The sample code consists of two parts :
1) Zoom-in on an entity and setting the orthographic view
2) Orbit around the entity with Z axis as the up-vector.
The orbit can be stopped by pressing the Escape key or will stop on its own after the 360 degree orbit is complete.
[CommandMethod("COrbit")]
public static void ContinuousOrbitMethod()
{
    Document doc
                = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions peo
                = new PromptEntityOptions("\nSelect an entity:");
    PromptEntityResult per = ed.GetEntity(peo);
      if (per.Status != PromptStatus.OK)
        return;
      ed.UpdateTiledViewportsInDatabase();
      using (Transaction tr
                    = db.TransactionManager.StartTransaction())
    {
        Entity ent
            = tr.GetObject(per.ObjectId, OpenMode.ForRead) as Entity;
          ViewportTable vpTbl
            = tr.GetObject(   
                                db.ViewportTableId,
                                OpenMode.ForRead
                          ) as ViewportTable;
        ViewportTableRecord viewportTableRec
                = tr.GetObject(
                                vpTbl["*Active"],
                                OpenMode.ForWrite
                              ) as ViewportTableRecord;
          viewportTableRec.SetViewDirection
                            (
                                OrthographicView.RightView
                            );
        tr.Commit();
    }
      Extents3d entityExtentWCS
                = new Extents3d(Point3d.Origin, Point3d.Origin);
    Extents3d entityExtentDCS
                = new Extents3d(Point3d.Origin, Point3d.Origin);
    double fieldWidth = 0.0;
    double fieldHeight = 0.0;
      using (Transaction tr
                    = db.TransactionManager.StartTransaction())
    {
        Entity ent = tr.GetObject(
                                    per.ObjectId,
                                    OpenMode.ForRead
                                 ) as Entity;
          entityExtentWCS = ent.GeometricExtents;
        // We will transform this later to DCS
        entityExtentDCS = ent.GeometricExtents;
          ViewportTable vpTbl = tr.GetObject(
                                            db.ViewportTableId,
                                            OpenMode.ForRead
                                          ) as ViewportTable;
          ViewportTableRecord viewportTableRec
                          = tr.GetObject(
                                            vpTbl["*Active"],
                                            OpenMode.ForWrite
                                        ) as ViewportTableRecord;
          //get the screen aspect ratio to calculate the height and width
        double scrRatio = (viewportTableRec.Width / viewportTableRec.Height);
          //prepare Matrix for DCS to WCS transformation
        Matrix3d matWCS2DCS
                = Matrix3d.PlaneToWorld(
                                viewportTableRec.ViewDirection
                                       );
          //for DCS target point is the origin
        matWCS2DCS
            = Matrix3d.Displacement (
                    viewportTableRec.Target - Point3d.Origin
                                    ) * matWCS2DCS;
          //WCS Xaxis is twisted by twist angle
        matWCS2DCS = Matrix3d.Rotation
                                (
                                    -viewportTableRec.ViewTwist,
                                    viewportTableRec.ViewDirection,
                                    viewportTableRec.Target
                                ) * matWCS2DCS;
          matWCS2DCS = matWCS2DCS.Inverse();
          //tranform the extents to the DCS defined by the viewdir
        entityExtentDCS.TransformBy(matWCS2DCS);
          double maxX = entityExtentDCS.MaxPoint.X,
               maxY = entityExtentDCS.MaxPoint.Y,
               minX = entityExtentDCS.MinPoint.X,
               minY = entityExtentDCS.MinPoint.Y;
          //width of the extents in current view
        double width = maxX -minX;
          //height of the extents in current view
        double height = maxY - minY;
          //get the view center point
        Point2d center = new Point2d((maxX + minX) * 0.5,
                                     (maxY + minY) * 0.5);
          // check if the width 'fits' in current window
        // if not then get the new height as per the
        // viewports aspect ratio
        if (width > (height * scrRatio))
            height = width / scrRatio;
          viewportTableRec.Height = height;
        viewportTableRec.Width = height * scrRatio;
        viewportTableRec.CenterPoint = center;
          fieldWidth = height * scrRatio;
        fieldHeight = height;
          tr.Commit();
    }
      ed.UpdateTiledViewportsFromDatabase();
      // Create and add our message filter to know if
    // escape is pressed during orbit.
    MyMessageFilter filter = new MyMessageFilter();
    System.Windows.Forms.Application.AddMessageFilter(filter);
      Manager gsm = doc.GraphicsManager;
    short vpNum = (short)Application.GetSystemVariable("CVPORT");
    Autodesk.AutoCAD.GraphicsSystem.View v = gsm.GetGsView(vpNum, false);
      Point3d position = v.Position;
    Point3d target
        = entityExtentWCS.MinPoint +
          (entityExtentWCS.MaxPoint - entityExtentWCS.MinPoint) * 0.5;
    Vector3d upVector = Vector3d.ZAxis;
    v.SetView(position, target, upVector, fieldWidth, fieldHeight);
    gsm.SetViewportFromView(vpNum, v);
      double maxSteps = 360.0;
    double xincr = (2.0 * Math.PI/ maxSteps);
    double yincr = 0.0;
    for (int step = 0; step < 360; step++)
    {
        if (filter.bCanceled == true)
        {
            ed.WriteMessage("\nOrbit cancelled.");
            break;
        }
          v.Orbit(xincr, yincr);
        ed.UpdateScreen();
          System.Threading.Thread.Sleep(100);
          // Check for user input events
        System.Windows.Forms.Application.DoEvents();
    }
    System.Windows.Forms.Application.RemoveMessageFilter(filter);
}
Here is the MessageFilter class to monitor the Escape key press :
public class MyMessageFilter : System.Windows.Forms.IMessageFilter
{
    public const int WM_KEYDOWN = 0x0100;
      public bool bCanceled = false;
      public bool PreFilterMessage(ref System.Windows.Forms.Message m)
    {
        if (m.Msg == WM_KEYDOWN)
        {
            // Check for the Escape keypress
            System.Windows.Forms.Keys kc =
                (System.Windows.Forms.Keys)(int)m.WParam &
                        System.Windows.Forms.Keys.KeyCode;
              if (m.Msg == WM_KEYDOWN &&
                kc == System.Windows.Forms.Keys.Escape)
            {
                bCanceled = true;
            }
            // Return true to filter all keypresses
            return true;
        }
        // Return false to let other messages through
        return false;
    }
}

