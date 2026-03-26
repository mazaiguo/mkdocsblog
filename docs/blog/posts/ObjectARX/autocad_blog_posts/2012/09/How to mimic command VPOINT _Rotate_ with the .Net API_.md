---
title: "How to mimic command VPOINT <Rotate> with the .Net API?"
date: 2012-09-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - C#
  - Database
description: "I’ve got recently a request from a developer who wanted to mimic command VPOINT with option <Rotate> with the possibility of performing a zoom exte..."
author: Autodesk
---
# How to mimic command VPOINT <Rotate> with the .Net API?

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/how-to-mimic-command-vpoint-rotate-with-the-net-api.html

## 文章内容

By Philippe Leefsma
I’ve got recently a request from a developer who wanted to mimic command VPOINT with option <Rotate> with the possibility of performing a zoom extents at the end. The tricky part is to align the extents with the view direction in order to compute the correct width and height.
Here is the C# code to achieve that:
[CommandMethod("VPointNet")]
public void VPointNet()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      //Gather inputs: two angles, set zoom to extents or not...
       PromptDoubleOptions pdo1 = new PromptDoubleOptions(
        "\nEnter angle in XY plane from X axis (deg): ");
      PromptDoubleResult pdr1 = ed.GetDouble(pdo1);
      if(pdr1.Status != PromptStatus.OK)
        return;
      PromptDoubleOptions pdo2 = new PromptDoubleOptions(
        "\nEnter angle from XY plane (deg): ");
      PromptDoubleResult pdr2 = ed.GetDouble(pdo2);
      if(pdr2.Status != PromptStatus.OK)
        return;
      PromptKeywordOptions pko = new PromptKeywordOptions(
        "\nZoom Extents?");
      pko.AllowNone = false;
    pko.Keywords.Add("Yes");
    pko.Keywords.Add("No");
    pko.Keywords.Default = "Yes";
      PromptResult pkr = ed.GetKeywords(pko);
      if (pkr.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        ViewTable vt = Tx.GetObject(db.ViewTableId, OpenMode.ForRead)
            as ViewTable;
          ViewTableRecord newView = ed.GetCurrentView();
          newView.ViewDirection = ComputeViewDirection(
            DegToRad(pdr1.Value),
            DegToRad(pdr2.Value));
          newView.Name = "VPNetView";
          if (pkr.StringResult == "Yes")
        {
            db.UpdateExt(true);
                                Extents3d extents = new Extents3d(db.Extmin, db.Extmax);
              SetViewToExtents(extents, newView);
        }
           if (!vt.Has(newView.Name))
        {
            vt.UpgradeOpen();
              vt.Add(newView);
              Tx.AddNewlyCreatedDBObject(newView, true);
        }
          using (ViewTableRecord vtr = new ViewTableRecord())
        {
            vtr.CopyFrom(newView);
            ed.SetCurrentView(vtr);
        }
          Tx.Commit();
    }
}
  Vector3d ComputeViewDirection(double angleInXyPlane, double angleFromXyPlane)
{
    Vector3d v1 = Vector3d.XAxis.RotateBy(angleInXyPlane, Vector3d.ZAxis);
      Vector3d v2 = v1.CrossProduct(Vector3d.ZAxis);
      Vector3d viewDir = v1.RotateBy(angleFromXyPlane, v2);
      return viewDir;
}
  void SetViewToExtents(Extents3d extents, AbstractViewTableRecord view)
{
    // Get the screen aspect ratio to calculate the height and width
    double scrRatio = (view.Width / view.Height);
      // Prepare Matrix for DCS to WCS transformation
    Matrix3d matWCS2DCS = Matrix3d.PlaneToWorld(view.ViewDirection);
      // For DCS target point is the origin
    matWCS2DCS = Matrix3d.Displacement(
        view.Target - Point3d.Origin) * matWCS2DCS;
      // WCS Xaxis is twisted by twist angle
    matWCS2DCS = Matrix3d.Rotation(
        -view.ViewTwist,
        view.ViewDirection,
        view.Target) * matWCS2DCS;
      matWCS2DCS = matWCS2DCS.Inverse();
      // Tranform the extents to the DCS defined by the viewdir
    extents.TransformBy(matWCS2DCS);
      // Width of the extents in current view
    double width = (extents.MaxPoint.X - extents.MinPoint.X);
      // Height of the extents in current view
    double height = (extents.MaxPoint.Y - extents.MinPoint.Y);
      // Get the view center point
    Point2d center = new Point2d(
        (extents.MaxPoint.X + extents.MinPoint.X) * 0.5,
        (extents.MaxPoint.Y + extents.MinPoint.Y) * 0.5);
      // Check if the width 'fits' in current window
    // if not then get the new height as per
    // the viewports aspect ratio
    if (width > (height * scrRatio))
        height = width / scrRatio;
      view.Height = height;
    view.Width = height * scrRatio;
    view.CenterPoint = center;
}
  double DegToRad(double deg)
{
    return deg * Math.PI / 180.0;
}

