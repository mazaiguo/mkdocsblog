---
title: "Selecting Model Space entities from Paper Space using AutoCAD Selection Sets in C#"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C#
  - Selection
description: "I recently posted a blog on Converting Paper Space point to Model Space using AutoCAD.NET and I thought I’d extend that same blog to include using ..."
author: Autodesk
---
# Selecting Model Space entities from Paper Space using AutoCAD Selection Sets in C#

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/selecting-model-space-entities-from-paper-space-using-autocad-selection-sets-in-c.html

## 文章内容

By Fenton Webb
I recently posted a blog on Converting Paper Space point to Model Space using AutoCAD.NET and I thought I’d extend that same blog to include using a Paper Space Vport geometry to select all of the Model Space objects that it displays…
So here goes :
// select all entities in Model Space using Paper Space viewport
// by Fenton Webb, DevTech, Autodesk, 02/Apr/2012
[CommandMethod("selectMsFromPs", CommandFlags.NoTileMode)]
static public void selectMsFromPs()
{
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
  // pick a PS Viewport
  PromptEntityOptions opts = new PromptEntityOptions("Pick PS Viewport");
  opts.SetRejectMessage("Must select PS Viewport objects only");
  opts.AddAllowedClass(typeof(Autodesk.AutoCAD.DatabaseServices.Viewport), false);
  PromptEntityResult res = ed.GetEntity(opts);
  if (res.Status == PromptStatus.OK)
  {
    int vpNumber = 0;
    // extract the viewport points
    Point3dCollection psVpPnts = new Point3dCollection();
    using (Autodesk.AutoCAD.DatabaseServices.Viewport psVp = res.ObjectId.Open(OpenMode.ForRead) 
as Autodesk.AutoCAD.DatabaseServices.Viewport)
    {
      // get the vp number
      vpNumber = psVp.Number;
      // now extract the viewport geometry
      psVp.GetGripPoints(psVpPnts, new IntegerCollection(), new IntegerCollection()); 
    }
      // let's assume a rectangular vport for now, make the cross-direction grips square
    Point3d tmp = psVpPnts[2];
    psVpPnts[2] = psVpPnts[1];
    psVpPnts[1] = tmp;
      // Transform the PS points to MS points
    ResultBuffer rbFrom = new ResultBuffer(new TypedValue(5003, 3));
    ResultBuffer rbTo = new ResultBuffer(new TypedValue(5003, 2));
    double[] retPoint = new double[] { 0, 0, 0 };
    // loop the ps points 
    Point3dCollection msVpPnts = new Point3dCollection();
    foreach (Point3d pnt in psVpPnts)
    {
      // translate from from the DCS of Paper Space (PSDCS) RTSHORT=3 and 
      // the DCS of the current model space viewport RTSHORT=2
      acedTrans(pnt.ToArray(), rbFrom.UnmanagedObject, rbTo.UnmanagedObject, 0, retPoint);
      // add the resulting point to the ms pnt array
      msVpPnts.Add(new Point3d(retPoint));
      ed.WriteMessage("\n" + new Point3d(retPoint).ToString());
    }
      // now switch to MS
    ed.SwitchToModelSpace();
    // set the CVPort
    Application.SetSystemVariable("CVPORT", vpNumber);
    // once switched, we can use the normal selection mode to select
    PromptSelectionResult selectionresult = ed.SelectCrossingPolygon(msVpPnts);
    // now switch back to PS
    ed.SwitchToPaperSpace();
  }
}

## 评论

**内容**: Jeff Suffet said...
Hello
What if some of the objects in Model Space are in an XREF? Is there are way to limit the objects selected to just the subentities of the xref in the Viewport?
Reply
01/09/2014 at 06:38 AM

---
**内容**: Mustafa Deniz Yildirim said...
Does not work for me. I just want to select my titleblocks in the whole drawing. They are in my layouts so i need to attout and attin them. But i can't even select them :/(
Reply
12/04/2014 at 06:13 AM

---
**内容**: Ben said...
Would anyone know why the CVPort variable is set? I don't understand the significance of this line:
// set the CVPort
Application.SetSystemVariable("CVPORT", vpNumber);
Reply
08/28/2019 at 10:01 PM

---
