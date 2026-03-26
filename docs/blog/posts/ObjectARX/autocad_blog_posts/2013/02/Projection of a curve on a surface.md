---
title: "Projection of a curve on a surface"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - Database
  - Surface
description: "Here is a sample code to project a line on to a cylindrical surface."
author: Autodesk
---
# Projection of a curve on a surface

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/projection-of-a-curve-on-a-surface.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to project a line on to a cylindrical surface.
It creates a cylindrical surface and a line and then does the projection. The project entities are added to the database.
[CommandMethod("ProjectLine")]
static public void ProjectLineMethod()
{
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
      ObjectId surfaceId = ObjectId.Null;
    using (Transaction tr
                    = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = tr.GetObject(
                                        db.BlockTableId,
                                        OpenMode.ForRead
                                    ) as BlockTable;
          BlockTableRecord ms = tr.GetObject(
                                bt[BlockTableRecord.ModelSpace],
                                OpenMode.ForWrite
                                    ) as BlockTableRecord;
          Arc arc = new Arc(  Point3d.Origin,
                            10.0,
                            Math.PI * 0.5,
                            Math.PI * 1.5
                        );
        ms.AppendEntity(arc);
        tr.AddNewlyCreatedDBObject(arc, true);
          Line line = new Line(   Point3d.Origin,
                                new Point3d(0.0, 10.0, 0.0)
                            );
        ms.AppendEntity(line);
        line.ColorIndex = 2;
        tr.AddNewlyCreatedDBObject(line, true);
          Profile3d profile = new Profile3d(arc);
        Vector3d direction = new Vector3d(0, 0, 20.0);
          SweepOptions sweepOptions = new SweepOptions();
          surfaceId =
            Autodesk.AutoCAD.DatabaseServices.Surface.CreateExtrudedSurface
            (
                profile,
                direction,
                sweepOptions,
                true
            );
        Autodesk.AutoCAD.DatabaseServices.Surface surface
            = tr.GetObject
                (
                    surfaceId,
                    OpenMode.ForWrite
                ) as Autodesk.AutoCAD.DatabaseServices.Surface;
          Entity[] projectedEntities
            = surface.ProjectOnToSurface(line, Vector3d.XAxis.Negate());
        if (projectedEntities != null)
        {
            foreach (Entity ent in projectedEntities)
            {
                ed.WriteMessage(
                    String.Format("Projected entity : {0}",
                                    ent.GetType().ToString()));
                ent.ColorIndex = 1;
                ms.AppendEntity(ent);
                tr.AddNewlyCreatedDBObject(ent, true);
            }
        }
        tr.Commit();
    }
}

