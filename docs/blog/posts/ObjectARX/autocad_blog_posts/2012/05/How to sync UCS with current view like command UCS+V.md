---
title: "How to sync UCS with current view like command UCS+V"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - UCS
description: "Here is how to achieve the same functionality than command UCS+V using .Net API:"
author: Autodesk
---
# How to sync UCS with current view like command UCS+V

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-sync-ucs-with-current-view-like-command-ucsv.html

## 文章内容

By Philippe Leefsma
  Here is how to achieve the same functionality than command UCS+V using .Net API:
//////////////////////////////////////////////////////////////////
// Use: Sync UCS with Current view like command UCS V
// Author: Philippe Leefsma, September 2011
//////////////////////////////////////////////////////////////////
[CommandMethod("UcsV")]
public static void UcsV()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      Autodesk.AutoCAD.GraphicsSystem.Manager mng =
        doc.GraphicsManager;
      short cvport = (short)Application.GetSystemVariable("CVPORT");
      Autodesk.AutoCAD.GraphicsSystem.View view =
        mng.GetGsView(cvport, true);
      Vector3d direction = (view.Target - view.Position);
    direction = direction.MultiplyBy(1 / direction.Length);
      Vector3d upVector = view.UpVector;
    upVector = upVector.MultiplyBy(1 / upVector.Length);
      Vector3d xAxis = direction.CrossProduct(upVector);
      Matrix3d ucs = Matrix3d.AlignCoordinateSystem(
        new Point3d(0, 0, 0),
        Vector3d.XAxis, Vector3d.YAxis, Vector3d.ZAxis,
        new Point3d(0, 0, 0), xAxis, upVector, direction);
      ed.CurrentUserCoordinateSystem = ucs;
}

## 评论

**内容**: AlexFielder said...
Thanks Phillipe, this could be very useful.
Do you have any examples of how to produce similar functionality to that of the PLAN command? (Aligning a view to a UCS)
Reply
05/10/2012 at 06:12 AM

---
**内容**: Philippe Leefsma said...
Hi Alex,
I don't have code that does exactly this, but below are two samples: the first one illustrates how to set properties for the current view, the second how to deal with UCSs. By combining both, you should be able to create code that provides the same functionalities than PLAN command.
[CommandMethod("SetView")]
public static void SetView()
{
Document doc = Application.DocumentManager.MdiActiveDocument;
Database db = doc.Database;
Editor ed = doc.Editor;
PromptPointOptions ppo1 =
new PromptPointOptions("\nEnter view target:");
PromptPointResult ppr1 = ed.GetPoint(ppo1);
if (ppr1.Status != PromptStatus.OK)
return;
if (ppr1.Status != PromptStatus.OK)
return;
PromptPointOptions ppo2 =
new PromptPointOptions("\nEnter point for camera: ");
PromptPointResult ppr2 = ed.GetPoint(ppo2);
if (ppr2.Status != PromptStatus.OK)
return;
using (ViewTableRecord vtr = new ViewTableRecord())
{
vtr.Target = ppr1.Value;
vtr.ViewDirection = vtr.Target.GetVectorTo(ppr2.Value);
Point3d camPt = vtr.Target.Add(vtr.ViewDirection);
ed.WriteMessage("\nCamera point x = " + camPt.X.ToString());
ed.WriteMessage("\nCamera point y = " + camPt.Y.ToString());
ed.WriteMessage("\nCamera point z = " + camPt.Z.ToString());
vtr.Height = 50.0;
vtr.CenterPoint = Point2d.Origin;
ed.SetCurrentView(vtr);
}
}

[CommandMethod("NewUCS")]
public static void NewUCS()
{
Document doc = Application.DocumentManager.MdiActiveDocument;
Database db = doc.Database;
using (Transaction Tx = db.TransactionManager.StartTransaction())
{
// Open the UCS table for read
UcsTable acUCSTbl;
acUCSTbl = Tx.GetObject(
db.UcsTableId,
OpenMode.ForRead)
as UcsTable;
UcsTableRecord acUCSTblRec;
// Check to see if the "New_UCS" UCS table record exists
if (acUCSTbl.Has("New_UCS") == false)
{
acUCSTblRec = new UcsTableRecord();
acUCSTblRec.Name = "New_UCS";
// Open the UCSTable for write
acUCSTbl.UpgradeOpen();
// Add the new UCS table record
acUCSTbl.Add(acUCSTblRec);
Tx.AddNewlyCreatedDBObject(acUCSTblRec, true);
}
else
{
acUCSTblRec = Tx.GetObject(
acUCSTbl["New_UCS"],
OpenMode.ForWrite)
as UcsTableRecord;
}
acUCSTblRec.Origin = new Point3d(4, 5, 3);
acUCSTblRec.XAxis = new Vector3d(0, 1, 0);
acUCSTblRec.YAxis = new Vector3d(0, 0, 1);
// Open the active viewport
ViewportTableRecord acVportTblRec;
acVportTblRec = Tx.GetObject(
doc.Editor.ActiveViewportId,
OpenMode.ForWrite)
as ViewportTableRecord;
// Display the UCS Icon at the origin of the current viewport
acVportTblRec.IconAtOrigin = true;
acVportTblRec.IconEnabled = true;
// Set the UCS current
acVportTblRec.SetUcs(acUCSTblRec.ObjectId);
doc.Editor.UpdateTiledViewportsFromDatabase();
// Display the name of the current UCS
UcsTableRecord acUCSTblRecActive;
acUCSTblRecActive = Tx.GetObject(
acVportTblRec.UcsName,
OpenMode.ForRead)
as UcsTableRecord;
Application.ShowAlertDialog(
"The current UCS is: " + acUCSTblRecActive.Name);
PromptPointResult pPtRes;
PromptPointOptions pPtOpts = new PromptPointOptions("");
// Prompt for a point
pPtOpts.Message = "\nEnter a point: ";
pPtRes = doc.Editor.GetPoint(pPtOpts);
Point3d pPt3dWCS;
Point3d pPt3dUCS;
// If a point was entered, then translate it to the current UCS
if (pPtRes.Status == PromptStatus.OK)
{
pPt3dWCS = pPtRes.Value;
pPt3dUCS = pPtRes.Value;
// Translate the point from the current UCS to the WCS
Matrix3d newMatrix = doc.Editor.CurrentUserCoordinateSystem;

pPt3dWCS = pPt3dWCS.TransformBy(newMatrix);
Application.ShowAlertDialog(
"The WCS coordinates are: \n" + pPt3dWCS.ToString() + "\n" +
"The UCS coordinates are: \n" + pPt3dUCS.ToString());
}
Tx.Commit();
}
}
Reply
05/16/2012 at 06:03 AM

---
**内容**: Maxence said...
Simplest version:
[CommandMethod("UcsV")]
public void UcsV()
{
Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
using (ViewTableRecord view = ed.GetCurrentView())
{
ed.CurrentUserCoordinateSystem = Matrix3d.PlaneToWorld(view.ViewDirection)
* Matrix3d.Rotation(-view.ViewTwist, Vector3d.ZAxis, Point3d.Origin);
}
}
Reply
02/27/2014 at 07:32 AM

---
