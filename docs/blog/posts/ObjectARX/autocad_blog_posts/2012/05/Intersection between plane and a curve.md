---
title: "Intersection between plane and a curve"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Surface
description: "Here are the steps to find the intersection of a curve and a Plane (based on the explanation provided by my colleague, Krishnamurthy Kalvai). I hav..."
author: Autodesk
---
# Intersection between plane and a curve

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/intersection-between-plane-and-a-curve.html

## 文章内容

By Balaji Ramamoorthy
Here are the steps to find the intersection of a curve and a Plane (based on the explanation provided by my colleague, Krishnamurthy Kalvai). I have provided a sample code that implements these steps to find an intersection between an ellipse and a plane.
1. Determine if the curve lies on the plane. You may query this using Curve::GetPlane( ). Check if the plane returned is the same as / parallel to the intersection plane using Plane::IntersectWith( ).
If the planes are parallel, there can be infinite intersection points or no points of intersection at all. In either case, you may stop here and not go to step 2.
2. Project the curve onto the plane using Curve::GetProjectedCurve( ).
3. Find the intersection between the projected curve and original curve using IntersectWith( ). The intersection points will be the same as points of intersection of the curve with the Intersection plane.
4. As a final check, check to see if the intersection points lie on the plane using AcGeSurface::isOn( )
[CommandMethod("PlaneCurveIntersection")]
public static void PlaneCurveIntersection()
{
    Document activeDoc
        = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
    Editor ed = activeDoc.Editor;
      // Create the planar region and the ellipse
    ObjectId regionId = ObjectId.Null;
    ObjectId ellipseId = ObjectId.Null;
    using (Transaction tr
                = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = tr.GetObject(
                                        db.BlockTableId,
                                        OpenMode.ForRead
                                    ) as BlockTable;
          BlockTableRecord modelSpace = tr.GetObject
                        (
                            bt[BlockTableRecord.ModelSpace],
                            OpenMode.ForWrite
                        ) as BlockTableRecord;
          Autodesk.AutoCAD.DatabaseServices.Polyline polyline
            = new Autodesk.AutoCAD.DatabaseServices.Polyline();
          polyline.Closed = true;
        polyline.AddVertexAt
                    (
                        0,
                        new Point2d(10.0, -10.0),
                        0.0,
                        0.0,
                        0.0
                    );
        polyline.AddVertexAt
                    (    1,
                        new Point2d(10.0, 10.0),
                        0.0,
                        0.0,
                        0.0
                    );
        polyline.AddVertexAt
                    (    2,
                        new Point2d(-10.0, 10.0),
                        0.0,
                        0.0,
                        0.0
                    );
        polyline.AddVertexAt
                    (
                        3,
                        new Point2d(-10.0, -10.0),
                        0.0,
                        0.0,
                        0.0
                    );
        DBObjectCollection coll = new DBObjectCollection();
        coll.Add(polyline);
        DBObjectCollection rgnColl
                                = Region.CreateFromCurves(coll);
        if (rgnColl.Count > 0)
        {
            Region rgn = rgnColl[0] as Region;
            regionId = modelSpace.AppendEntity(rgn);
            tr.AddNewlyCreatedDBObject(rgn, true);
        }
        Vector3d ellipseNormal
            = Vector3d.ZAxis.RotateBy(
                                        45.0 * Math.PI / 180.0,
                                        Vector3d.XAxis
                                     );
        Vector3d ellipseMajorAxis = new Vector3d(0, 5, 0);
        ellipseMajorAxis
            = ellipseMajorAxis.RotateBy
                                    (
                                        45.0 * Math.PI / 180.0,
                                        Vector3d.XAxis
                                    );
        Ellipse ellipse = new Ellipse
                                    (
                                        Point3d.Origin,
                                        ellipseNormal,
                                        ellipseMajorAxis,
                                        0.5,
                                        0,
                                        0
                                    );
        ellipseId = modelSpace.AppendEntity(ellipse);
        tr.AddNewlyCreatedDBObject(ellipse, true);
        tr.Commit();
    }
      // Find the intersection of the curve and the plane
    using (Transaction tr
            = db.TransactionManager.StartTransaction())
    {
        Region rgn = tr.GetObject
                                (
                                    regionId,
                                    OpenMode.ForRead
                                ) as Region;
        DBObjectCollection exploded = new DBObjectCollection();
        rgn.Explode(exploded);
        Entity firstEntity = exploded[0] as Entity;
        Plane intersectionPlane = firstEntity.GetPlane();
        Curve curve = tr.GetObject
                                (
                                    ellipseId,
                                    OpenMode.ForRead
                                ) as Curve;
        Plane curvePlane = curve.GetPlane();
        if (curvePlane.IsCoplanarTo(intersectionPlane))
        {
            ed.WriteMessage("\nInfinite intersections !");
        }
        else if (curvePlane.IsParallelTo(intersectionPlane))
        {
            ed.WriteMessage("\nNo intersections !");
        }
        else
        {
            Curve projectedCurve
                = curve.GetProjectedCurve
                                    (
                                        intersectionPlane,
                                        intersectionPlane.Normal
                                    );
            Point3dCollection intPts = new Point3dCollection();
            projectedCurve.IntersectWith
                                    (
                                        curve,
                                        Intersect.ExtendBoth,
                                        intPts,
                                        IntPtr.Zero,
                                        IntPtr.Zero
                                    );
            foreach (Point3d pt in intPts)
            {
                if (curvePlane.IsOn(pt))
                {
                    ed.WriteMessage
                                (
                        string.Format(
                                        "{0}{1}",
                                        Environment.NewLine,
                                        pt.ToString()
                                     )
                                );
                }
            }
        }
        tr.Commit();
    }
}

