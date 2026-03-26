---
title: "Align the UCS to an entity"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Database
  - UCS
description: "Below code shows the procedure to align the UCS to a line. Below code treats the Lines start point is origin of the UCS."
author: Autodesk
---
# Align the UCS to an entity

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/align-the-ucs-to-an-entity.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to align the UCS to a line. Below code treats the Lines start point is origin of the UCS.
[CommandMethod("SetUCS")]
static public void SetUCS()
{
    // get the database
    Database db = HostApplicationServices.WorkingDatabase;
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    // select a line
    PromptEntityOptions options = new PromptEntityOptions(
                    "\nSelect an Line Entity to set the UCS too : ");
      options.SetRejectMessage("\nSelect Line");
    options.AddAllowedClass(typeof(Line), false);
      PromptEntityResult res = ed.GetEntity(options);
    // if ok
    if (res.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        Line ent = Tx.GetObject(res.ObjectId, OpenMode.ForRead) as
                        Line;
        // get the ucs from the entity
        Matrix3d ecs = new Matrix3d();
        // set the direction of the
        Vector3d xVec = (ent.EndPoint - ent.StartPoint);
        // normalise
        xVec = xVec.GetNormal();
        // set up the coord system that we want
        CoordinateSystem3d coordSystem = new CoordinateSystem3d(
          ent.StartPoint, xVec,
          xVec.CrossProduct(ent.Normal).Negate());
          CoordinateSystem3d cosy =
               ed.CurrentUserCoordinateSystem.CoordinateSystem3d;
        // now align from the current ucs to ours
        ecs = Matrix3d.AlignCoordinateSystem(
                                              cosy.Origin,
                                              cosy.Xaxis,
                                              cosy.Yaxis,
                                              cosy.Zaxis,
                                              coordSystem.Origin,
                                              coordSystem.Xaxis,
                                              coordSystem.Yaxis,
                                              coordSystem.Zaxis
                                              );
        // now set the current ucs to the ecs
        ed.CurrentUserCoordinateSystem = ecs;
          Tx.Commit();
    }
      // finally update the viewport
    ed.UpdateTiledViewportsInDatabase();
  }

