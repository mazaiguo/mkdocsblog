---
title: "Aligning entity using 3 points"
date: 2013-07-01
categories:
  - AutoCAD
tags:
  - Database
  - Selection
description: "Here is a sample code to align a selected entity based on three source and their corresponding destination points. The order in which the point are..."
author: Autodesk
---
# Aligning entity using 3 points

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/aligning-entity-using-3-points.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to align a selected entity based on three source and their corresponding destination points. The order in which the point are selected is shown in the screenshot and a sample drawing to try the the code snippet.
Document activeDoc = Application.DocumentManager.MdiActiveDocument;
Database db = activeDoc.Database;
Editor ed = activeDoc.Editor;
  // Prompt for entity selection
PromptEntityResult per
= ed.GetEntity(new PromptEntityOptions("Select an entity : "));
if (per.Status != PromptStatus.OK)
    return;
  ObjectId oid = per.ObjectId;
  Matrix3d ucs2wcs = ed.CurrentUserCoordinateSystem;
  // 3 source points
Point3d srcpt1 = Point3d.Origin;
Point3d srcpt2 = Point3d.Origin;
Point3d srcpt3 = Point3d.Origin;
  // 3 destination points
Point3d destpt1 = Point3d.Origin;
Point3d destpt2 = Point3d.Origin;
Point3d destpt3 = Point3d.Origin;
  // Source point 1
PromptPointResult ppr1
    = ed.GetPoint(new PromptPointOptions("Select src point 1"));
if (ppr1.Status != PromptStatus.OK)
    return;
srcpt1 = ppr1.Value.TransformBy(ucs2wcs);
  // Destination point 1
ppr1 = ed.GetPoint(new PromptPointOptions("Select dest point 1"));
if (ppr1.Status != PromptStatus.OK)
    return;
destpt1 = ppr1.Value.TransformBy(ucs2wcs);
  // Display transient line to show the selection of points
IntegerCollection coll = new IntegerCollection();
Line tmpline1 = new Line(srcpt1, destpt1);
TransientManager.CurrentTransientManager.AddTransient
   (tmpline1, TransientDrawingMode.DirectShortTerm, 128, coll);
  // Source point 2
PromptPointResult ppr2
    = ed.GetPoint(new PromptPointOptions("Select src point 2"));
if (ppr2.Status != PromptStatus.OK)
    return;
srcpt2 = ppr2.Value.TransformBy(ucs2wcs);
  // Destination point 2
ppr2 = ed.GetPoint(new PromptPointOptions("Select dest point 2"));
if (ppr2.Status != PromptStatus.OK)
    return;
destpt2 = ppr2.Value.TransformBy(ucs2wcs);
  // Display transient line to show the selection of points
Line tmpline2 = new Line(srcpt2, destpt2);
TransientManager.CurrentTransientManager.AddTransient
    (tmpline2, TransientDrawingMode.DirectShortTerm, 128, coll);
  // Source point 3
PromptPointResult ppr3
    = ed.GetPoint(new PromptPointOptions("Select src point 3"));
if (ppr3.Status != PromptStatus.OK)
    return;
srcpt3 = ppr3.Value.TransformBy(ucs2wcs);
  // Destination point 3
ppr3 = ed.GetPoint(new PromptPointOptions("Select dest point 3"));
if (ppr3.Status != PromptStatus.OK)
    return;
destpt3 = ppr3.Value.TransformBy(ucs2wcs);
  // Display transient line to show the selection of points
Line tmpline3 = new Line(srcpt3, destpt3);
TransientManager.CurrentTransientManager.AddTransient
    (tmpline3, TransientDrawingMode.DirectShortTerm, 128, coll);
  try
{
    Point3d fromOrigin = srcpt1;
    Vector3d fromXaxis = srcpt2 - srcpt1;
    Vector3d fromYaxis = srcpt3 - srcpt1;
    Vector3d fromZaxis = fromXaxis.CrossProduct(fromYaxis);
      Point3d toOrigin = destpt1;
    Vector3d toXaxis =
            (destpt2 - destpt1).GetNormal() * fromXaxis.Length;
    Vector3d toYaxis
           = (destpt3 - destpt1).GetNormal() * fromYaxis.Length;
    Vector3d toZaxis = toXaxis.CrossProduct(toYaxis);
      // Get the transformation matrix for aligning coordinate systems
    Matrix3d mat = new Matrix3d();
    mat = Matrix3d.AlignCoordinateSystem(
                                            fromOrigin,
                                            fromXaxis,
                                            fromYaxis,
                                            fromZaxis,
                                            toOrigin,
                                            toXaxis,
                                            toYaxis,
                                            toZaxis
                                        );
      // Transform the selected entity
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        Entity ent = tr.GetObject(oid, OpenMode.ForWrite) as Entity;
        ent.TransformBy(mat);
        tr.Commit();
    }
}
catch (Autodesk.AutoCAD.Runtime.Exception ex )
{
    ed.WriteMessage(ex.Message);
}
  // Remove the transient lines
TransientManager.CurrentTransientManager.EraseTransient
                                              (tmpline1, coll);
tmpline1.Dispose();
  TransientManager.CurrentTransientManager.EraseTransient
                                              (tmpline2, coll);
tmpline2.Dispose();
  TransientManager.CurrentTransientManager.EraseTransient
                                              (tmpline3, coll);
tmpline3.Dispose();
The screenshots show the order of selected points and the aligned entity
Here is a sample drawing to try the sample code :
Download Test

