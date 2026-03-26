---
title: "Positioning a selected entity at view center"
date: 2014-04-01
categories:
  - AutoCAD
tags:
  - Database
description: "Here is a code snippet to position an entity at the center of the view. Most of this code is similar to the way we would zoom on to an entity excep..."
author: Autodesk
---
# Positioning a selected entity at view center

发布日期: 2014-04-01

原始链接: https://adndevblog.typepad.com/autocad/2014/04/positioning-a-selected-entity-at-view-center.html

## 文章内容

By Balaji Ramamoorthy
Here is a code snippet to position an entity at the center of the view. Most of this code is similar to the way we would zoom on to an entity except that the Width and Height of the view is not modified. In this case, it is only relevant to set the view center point in DCS.
Document doc = Application.DocumentManager.MdiActiveDocument;
Database db = doc.Database;
Editor ed = doc.Editor;
  PromptEntityOptions peo
            = new PromptEntityOptions("\nSelect an entity:");
PromptEntityResult per = ed.GetEntity(peo);
if (per.Status != PromptStatus.OK)
    return;
  ed.UpdateTiledViewportsInDatabase();
  using (Transaction tr = db.TransactionManager.StartTransaction())
{
    Entity ent = tr.GetObject(
                    per.ObjectId, OpenMode.ForRead) as Entity;
      Extents3d entityExtent = ent.GeometricExtents;
      ViewportTable vpTbl = tr.GetObject(
                                        db.ViewportTableId,
                                        OpenMode.ForRead
                                      ) as ViewportTable;
      ViewportTableRecord viewportTableRec
           = tr.GetObject(vpTbl["*Active"], OpenMode.ForWrite)
                                       as ViewportTableRecord;
      Matrix3d matWCS2DCS
       = Matrix3d.PlaneToWorld(viewportTableRec.ViewDirection);
      matWCS2DCS = Matrix3d.Displacement(
        viewportTableRec.Target - Point3d.Origin) * matWCS2DCS;
      matWCS2DCS = Matrix3d.Rotation
                                (
                                 -viewportTableRec.ViewTwist,
                                 viewportTableRec.ViewDirection,
                                 viewportTableRec.Target
                                 ) * matWCS2DCS;
      matWCS2DCS = matWCS2DCS.Inverse();
      entityExtent.TransformBy(matWCS2DCS);
      Point2d center = new Point2d(
    (entityExtent.MaxPoint.X + entityExtent.MinPoint.X) * 0.5,
    (entityExtent.MaxPoint.Y + entityExtent.MinPoint.Y) * 0.5);
      viewportTableRec.CenterPoint = center;
      tr.Commit();
}
  ed.UpdateTiledViewportsFromDatabase();

