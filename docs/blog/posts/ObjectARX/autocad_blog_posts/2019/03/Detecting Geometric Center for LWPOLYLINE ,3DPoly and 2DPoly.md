---
title: "Detecting Geometric Center for LWPOLYLINE ,3DPoly and 2DPoly"
date: 2019-03-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - Polyline
description: "Unfortunately there is no direct API to detect geometric center for three classifications of polylines, one may use Topology libraries to find out,..."
author: Autodesk
---
# Detecting Geometric Center for LWPOLYLINE ,3DPoly and 2DPoly

发布日期: 2019-03-01

原始链接: https://adndevblog.typepad.com/autocad/2019/03/detecting-geometric-center-for-lwpolyline-3dpoly-and-2dpoly.html

## 文章内容

By Madhukar Moogala
Unfortunately there is no direct API to detect geometric center for three classifications of polylines, one may use Topology libraries to find out, or preferably the easiest at least for me is to convert the LWPOLYLINE, AcDb2dPolyline,AcDb3dPolyline to an in-memory region, apply area properties API to fetch Geometric Center.

[CommandMethod("GCTR")]
public static void GC() {

 var doc = AcCoreApp.DocumentManager.MdiActiveDocument;
 var db = doc.Database;
 var ed = doc.Editor;
 var tid = ObjectId.Null;
 Point2d centroid = Point2d.Origin;

 using(Transaction tr = db.TransactionManager.StartTransaction()) {
  try {

   TypedValue[] acTypValAr = {
    new TypedValue((int) DxfCode.Operator, "")
   };
   // Assign the filter criteria to a SelectionFilter object
   SelectionFilter acSelFtr = new SelectionFilter(acTypValAr);
   // Request for objects to be selected in the drawing area
   PromptSelectionResult acSSPrompt;
   acSSPrompt = ed.GetSelection(acSelFtr);

   // If the prompt status is OK, objects were selected
   if (acSSPrompt.Status == PromptStatus.OK) {
    SelectionSet acSSet = acSSPrompt.Value;
    foreach(SelectedObject so in acSSet) {
     var pline = tr.GetObject(so.ObjectId, OpenMode.ForRead) as Entity;
     //Convert entity to in-memory Region.
     using(DBObjectCollection segments = new DBObjectCollection()) {
      pline.Explode(segments);
      DBObjectCollection regions = Region.CreateFromCurves(segments);
      foreach(Region r in regions) {
       //to get the centroid of a region lying on the WCS XY plane:
       Point3d origin = Point3d.Origin;
       Vector3d xAxis = Vector3d.XAxis;
       Vector3d yAxis = Vector3d.YAxis;
       centroid = r.AreaProperties(ref origin, ref xAxis, ref yAxis).Centroid;
       CenterMarkEntity(centroid);
      }


     }
     ed.WriteMessage($ "\nGeometricCenter of {pline.GetRXClass().DxfName}:{centroid}");
    }
    tr.Commit();
   } else {
    Autodesk.AutoCAD.ApplicationServices.Core.Application.ShowAlertDialog("Number of objects selected: 0");
   }


  } catch (Autodesk.AutoCAD.Runtime.Exception ex) {
   ed.WriteMessage(ex.ToString());
  }
 }


}

public static void CenterMarkEntity(Point2d p) {
  var doc = AcCoreApp.DocumentManager.MdiActiveDocument;
  var db = doc.Database;
  var ed = doc.Editor;
  using(Transaction t = db.TransactionManager.StartTransaction()) {
   short mode = (short) AcCoreApp.GetSystemVariable("PDMODE");
   if (mode == 0) {
    AcCoreApp.SetSystemVariable("PDMODE", 99);
   }
   var ms = t.GetObject(SymbolUtilityServices.GetBlockModelSpaceId(db), OpenMode.ForWrite) as BlockTableRecord;
   DBPoint dbPt = new DBPoint(new Point3d(p.X, p.Y, .0)) {
    ColorIndex = 3
   };
   ms.AppendEntity(dbPt);
   t.AddNewlyCreatedDBObject(dbPt, true);
   t.Commit();

  }
 }
Test sample Drawing
SampleDrawing

## 评论

**内容**: Gilles Chanteau said...
It seems to me you have to explicitly call dispose for each DBObject in 'segments' and for each created Region.
Reply
08/31/2019 at 08:12 AM

---
