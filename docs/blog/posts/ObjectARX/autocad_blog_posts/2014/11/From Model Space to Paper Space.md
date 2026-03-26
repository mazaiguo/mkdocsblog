---
title: "From Model Space to Paper Space"
date: 2014-11-01
categories:
  - AutoCAD
tags:
  - Dimension
  - Plugin
description: "Convert a coordinate from a Paper Space Viewport to the respective Model Space is possible using acedTrans and it’s already described at this blog ..."
author: Autodesk
---
# From Model Space to Paper Space

发布日期: 2014-11-01

原始链接: https://adndevblog.typepad.com/autocad/2014/11/from-model-space-to-paper-space.html

## 文章内容

By Augusto Goncalves
Convert a coordinate from a Paper Space Viewport to the respective Model Space is possible using acedTrans and it’s already described at this blog post. Note that a point on a Viewport will point to a single point on model space, meaning this is a 1 to 1 relationship.
The opposite way is not 1 to 1, but in fact 1 to many. A point on the model space can be on several paper space viewport. To make such a conversion, we need to have a viewport, then do some math to convert the coordinate. With that, the basic idea is calculate a scale factor using two points on both paper and model space. Then using those points again calculate how much the need to move.
With that in mind, the code below is the same from this post with a few new pieces in bold. To test the idea, the code is also adding DBPoints on Paper Space for each entity’s grip point (from model space).
Note this is assuming a 2D drawing on model space, showing as a 2D drawing on paper space, with a simple view (no perspective). To make it work on every possible scenario, we may need to adjust the math…
[CommandMethod("testAcadMS2PS")]
public void CmdTestAcadMS2PS()
{
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
  // pick a PS Viewport
  PromptEntityOptions opts = new PromptEntityOptions("Pick PS Viewport");
  opts.SetRejectMessage("Must select PS Viewport objects only");
  opts.AddAllowedClass(typeof(Viewport), false);
  PromptEntityResult res = ed.GetEntity(opts);
  if (res.Status == PromptStatus.OK)
  {
    int vpNumber = 0;
    // extract the viewport points
    Point3dCollection psVpPnts = new Point3dCollection();
    using (Viewport psVp =
      res.ObjectId.Open(OpenMode.ForRead) as Viewport)
    {
      // get the vp number
      vpNumber = psVp.Number;
      // now extract the viewport geometry
      psVp.GetGripPoints(psVpPnts, new IntegerCollection(),
        new IntegerCollection());
    }
 
    // let's assume a rectangular vport for now,
    // make the cross-direction grips square
    Point3d tmp = psVpPnts[2];
    psVpPnts[2] = psVpPnts[1];
    psVpPnts[1] = tmp;
 
    // Transform the PS points to MS points
    ResultBuffer rbFrom = new ResultBuffer(new TypedValue(5003, 3));
    ResultBuffer rbTo = new ResultBuffer(new TypedValue(5003, 2));
    double[] retPointDouble = new double[] { 0, 0, 0 };
    // loop the ps points 
    Point3dCollection msVpPnts = new Point3dCollection();
    foreach (Point3d pnt in psVpPnts)
    {
      // translate from from the DCS of Paper Space (PSDCS) RTSHORT=3 and 
      // the DCS of the current model space viewport RTSHORT=2
      acedTrans(pnt.ToArray(), rbFrom.UnmanagedObject,
        rbTo.UnmanagedObject, 0, retPointDouble);
      // add the resulting point to the ms pnt array
      Point3d retPoint = new Point3d(retPointDouble);
      msVpPnts.Add(retPoint);
    }
 
    // *******
    // now we assume both list of points (on MS and PS) have
    // at least 2 points, which is correct as a Viewport needs
    // 3 points for create a closed area
    // 
    // find the scale fator based on points from PS and MS
    double transformScale =
      psVpPnts[1].DistanceTo(psVpPnts[0]) /
      msVpPnts[1].DistanceTo(msVpPnts[0]);
    // and find the transformation vector (displacement)
    Vector3d transformVector = msVpPnts[0].TransformBy(
      Matrix3d.Scaling(transformScale, Point3d.Origin))
      .GetVectorTo(psVpPnts[0]);
    // *******
 
    // now switch to MS
    ed.SwitchToModelSpace();
    // set the CVPort
    Application.SetSystemVariable("CVPORT", vpNumber);
    // once switched, we can use the normal selection mode to select
    PromptSelectionResult selectionresult =
      ed.SelectCrossingPolygon(msVpPnts);
    // now switch back to PS
    ed.SwitchToPaperSpace();
 
    // *******
    Database db = Application.DocumentManager.MdiActiveDocument.Database;
    using (Transaction trans = db.TransactionManager.StartTransaction())
    {
      BlockTableRecord paperSpace = trans.GetObject(db.CurrentSpaceId,
        OpenMode.ForWrite) as BlockTableRecord;
      foreach (SelectedObject obj in selectionresult.Value)
      {
        Entity ent = trans.GetObject(obj.ObjectId, OpenMode.ForRead) as Entity;
        Point3dCollection grips = new Point3dCollection();
        ent.GetGripPoints(grips, new IntegerCollection(), new IntegerCollection());
        foreach (Point3d pt in grips)
        {
          // for each grip point on MS, add a DBPoint
          // apply first the scaling fator
          // then the displacement vector
          DBPoint point = new DBPoint(pt
            .TransformBy(Matrix3d.Scaling(transformScale, Point3d.Origin))
            .TransformBy(Matrix3d.Displacement(transformVector))
            );
          paperSpace.AppendEntity(point);
          trans.AddNewlyCreatedDBObject(point, true);
        }
      }
      trans.Commit();
    }
    // *******
  }
}
 
[DllImport("accore.dll",
  CallingConvention = CallingConvention.Cdecl, EntryPoint = "acedTrans")]
private static extern int acedTrans(double[] point, IntPtr fromRb,
  IntPtr toRb, int disp, double[] result);

