---
title: "Retrieving native curve geometry using BRep API"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - Solid
  - Surface
description: "To access the geometry of the edges that make a solid or a surface, you could use the BRep API to get the edges. The edge exposes the native curve ..."
author: Autodesk
---
# Retrieving native curve geometry using BRep API

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/retrieving-native-curve-geometry-using-brep-api.html

## 文章内容

By Balaji Ramamoorthy
To access the geometry of the edges that make a solid or a surface, you could use the BRep API to get the edges. The edge exposes the native curve which can then be used to get to the geometry such as the radius and center point of a circular edge.
As an example, here is a sample code that gets to the curve geometry by using the BRep API on an extruded surface. In this case, the edges are of type "LinearEntity3d" and "CircularArc3d".
[CommandMethod("surfTest")]
public void SurfaceTestMethod()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      ObjectId surfaceId = ObjectId.Null;
    // Create a test surface
    using (Transaction Tx
                    = db.TransactionManager.StartTransaction())
    {
        Circle circle = new Circle(
                                    new Point3d(15, 0, 15),
                                    new Vector3d(0, 1, 0),
                                    3
                                  );
          BlockTable bt = Tx.GetObject(
                                        db.BlockTableId,
                                        OpenMode.ForRead
                                    ) as BlockTable;
          BlockTableRecord model = Tx.GetObject
                        (
                            bt[BlockTableRecord.ModelSpace],
                            OpenMode.ForWrite
                        ) as BlockTableRecord;
          surfaceId = model.AppendEntity(circle);
          Tx.AddNewlyCreatedDBObject(circle, true);
          Profile3d profile = new Profile3d(circle);
          Vector3d direction = new Vector3d(0, 5, 0);
          SweepOptions sweepOptions = new SweepOptions();
          surfaceId =
            Autodesk.AutoCAD.DatabaseServices.Surface.CreateExtrudedSurface
                    (
                        profile,
                        direction,
                        sweepOptions,
                        true
                    );
          Tx.Commit();
    }
      // Use BRep to investigate the edges of the surface
    using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        Autodesk.AutoCAD.DatabaseServices.Surface surface
            = Tx.GetObject
                        (
                            surfaceId,
                            OpenMode.ForRead
                        ) as Autodesk.AutoCAD.DatabaseServices.Surface;
          using (Autodesk.AutoCAD.BoundaryRepresentation.Brep brep
            = new Autodesk.AutoCAD.BoundaryRepresentation.Brep(surface))
        {
            int edgeCnt = 1;
            foreach (Autodesk.AutoCAD.BoundaryRepresentation.Edge edge in brep.Edges)
            {
                ed.WriteMessage("\n --> Edge : {0}", edgeCnt++);
                  Curve3d edgeCurve = edge.Curve;
                  if (edgeCurve is ExternalCurve3d)
                {
                    ed.WriteMessage
                        (
                            "\n Edge type : {0}",
                            "ExternalCurve3d"
                        );
                      ExternalCurve3d extCurve3d = edgeCurve as ExternalCurve3d;
                    Curve3d nativeCurve = extCurve3d.NativeCurve;
                      if (nativeCurve is CircularArc3d)
                    {
                        ed.WriteMessage
                            (
                                "\n Native curve type : {0}",
                                "CircularArc3d"
                            );
                        CircularArc3d circArc3d
                                = nativeCurve as CircularArc3d;
                        //...
                    }
                    if (nativeCurve is CompositeCurve3d)
                    {
                        ed.WriteMessage
                            (
                                "\nNative curve type : {0}",
                                "CompositeCurve3d"
                            );
                        CompositeCurve3d compCurve3d
                            = nativeCurve as CompositeCurve3d;
                        //...
                    }
                    if (nativeCurve is EllipticalArc3d)
                    {
                        ed.WriteMessage
                            (
                                "\n Native curve type : {0}",
                                "EllipticalArc3d"
                            );
                        EllipticalArc3d ellipticalArc3d
                            = nativeCurve as EllipticalArc3d;
                        //...
                    }
                    if (nativeCurve is LinearEntity3d)
                    {
                        ed.WriteMessage
                            (
                                "\n Native curve : {0}",
                                "LinearEntity3d"
                            );
                        LinearEntity3d linearEntity3d
                            = nativeCurve as LinearEntity3d;
                        //...
                    }
                    if (nativeCurve is OffsetCurve3d)
                    {
                        ed.WriteMessage
                            (
                                "\n Native curve : {0}",
                                "OffsetCurve3d"
                            );
                        OffsetCurve3d offsetCurve3d
                            = nativeCurve as OffsetCurve3d;
                        //...
                    }
                    if (nativeCurve is SplineEntity3d)
                    {
                        ed.WriteMessage
                            (
                                "\n Native curve : {0}",
                                "SplineEntity3d"
                            );
                        SplineEntity3d splineEntity3d
                            = nativeCurve as SplineEntity3d;
                        //...
                    }
                }
            }
        }
    }
}

