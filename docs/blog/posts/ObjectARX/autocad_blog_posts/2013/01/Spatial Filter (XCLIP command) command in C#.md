---
title: "Spatial Filter (XCLIP command) command in C#"
date: 2013-01-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Block
  - C#
  - C++
description: "Is it possible to programmatically create a spatial filter like XCLIP command in .Net? Unfortunately the AcDbIndexFilterManager::addFilter method i..."
author: Autodesk
---
# Spatial Filter (XCLIP command) command in C#

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/spatial-filter-xclip-command-command-in-c.html

## 文章内容

By Augusto Goncalves
Is it possible to programmatically create a spatial filter like XCLIP command in .Net? Unfortunately the AcDbIndexFilterManager::addFilter method is not exposed, but we can P/Invoke it. The following C# sample illustrates how to do that. Note that some version specific decorated names are used (see EntryPoint parameter), which can cause this code not to work on other versions.
// required ObjectARX methods, called with P/Invoke
// this is valid for R19 release (AutoCAD 2013)
[DllImport("acdb19.dll",
    CharSet = CharSet.Unicode,
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "?addFilter@AcDbIndexFilterManager@@YA?AW4ErrorStatus@Acad@@PAVAcDbBlockReference@@PAVAcDbFilter@@@Z")]
private static extern int addFilter32(IntPtr pBlkRef, IntPtr pFilter);
[DllImport("acdb19.dll",
    CharSet = CharSet.Unicode,
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "?addFilter@AcDbIndexFilterManager@@YA?AW4ErrorStatus@Acad@@PEAVAcDbBlockReference@@PEAVAcDbFilter@@@Z")]
private static extern int addFilter64(IntPtr pBlkRef, IntPtr pFilter);
  /// <summary>
/// Check if the OS is 32 or 64 bit
/// </summary>
static public bool is64bits
{
  get { return (Application.GetSystemVariable
    ("PLATFORM").ToString().IndexOf("64") > 0); }
}
  //Create a spatial filter on the selected block reference
//create rectangular cliping area by providing the 2 corners
[CommandMethod("NetClip")]
public void NetClip()
{
  // required variables
  Document doc = Application.DocumentManager.
    MdiActiveDocument;
  Database db = doc.Database;
  Editor ed = doc.Editor;
    // select a block reference
  PromptEntityOptions peo = new PromptEntityOptions(
    "\nSelect a block reference: ");
  peo.SetRejectMessage("\nMust be a block reference...");
  peo.AddAllowedClass(typeof(BlockReference), true);
  PromptEntityResult per = ed.GetEntity(peo);
  if (per.Status != PromptStatus.OK) return;
    PromptPointOptions ppo = new PromptPointOptions(
    "\nSelect rect clip 1st corner: ");
  PromptPointResult ppr1 = ed.GetPoint(ppo);
    if (ppr1.Status != PromptStatus.OK)
    return;
    PromptCornerOptions pco = new PromptCornerOptions(
    "\nSelect rect clip 2nd corner: ", ppr1.Value);
  pco.UseDashedLine = true;
    PromptPointResult ppr2 = ed.GetCorner(pco);
    if (ppr2.Status != PromptStatus.OK)
    return;
    using (Transaction trans = db.TransactionManager
    .StartTransaction())
  {
    BlockReference bref = trans.GetObject(per.ObjectId,
      OpenMode.ForWrite) as BlockReference;
      //Define clip rectangle
    Point3d pt3d1 = ppr1.Value.TransformBy(
      bref.BlockTransform.Inverse());
    Point3d pt3d2 = ppr2.Value.TransformBy(
      bref.BlockTransform.Inverse());
      Point2dCollection boundary =
      GetClipRectangle(pt3d1, pt3d2);
      double elevation = 0.0;
      SpatialFilter filter = new SpatialFilter();
      filter.Definition = new
      SpatialFilterDefinition(boundary,
      bref.Normal, elevation, 1000, -1000, true);
      //P/Invoke AcDbIndexFilterManager::addFilter
    int es;
    if (is64bits)
      es = addFilter64(bref.UnmanagedObject,
        filter.UnmanagedObject);
    else
      es = addFilter32(bref.UnmanagedObject,
        filter.UnmanagedObject);
      if (es == 0)
    {
      ed.WriteMessage(
        "\nSpatial filter added successfully...");
      DrawClipBoundary(boundary, bref,
        bref.Normal, elevation);
    }
    else
    {
      ed.WriteMessage(
        "\nSpatial filter failed:(...Error code:"
        + es.ToString());
    };
      // need to explicitely close the filter
    filter.Close();
    trans.Commit();
  }
}
  // the clip rectangle needs to be provided
// with (lower-left, upper-right) so we may
// need to re-arrange depending on how the
// user selected corners
Point2dCollection GetClipRectangle(
  Point3d p1, Point3d p2)
{
  Point2dCollection clipRect =
    new Point2dCollection();
    double minX = p1.X;
  double minY = p1.Y;
    double maxX = p2.X;
  double maxY = p2.Y;
    if (minX > p2.X)
  {
    minX = p2.X;
    maxX = p1.X;
  }
    if (minY > p2.Y)
  {
    minY = p2.Y;
    maxY = p1.Y;
  }
    clipRect.Add(new Point2d(minX, minY));
  clipRect.Add(new Point2d(maxX, maxY));
    return clipRect;
}
  //Just an optional method in order to visualize the clip area
void DrawClipBoundary(
  Point2dCollection boundary,
  BlockReference bref,
  Vector3d Normal,
  double elevation)
{
  Database db = HostApplicationServices.
    WorkingDatabase;
    using (Transaction trans =
    db.TransactionManager.StartTransaction())
  {
    BlockTable bT = trans.GetObject(
      db.BlockTableId, OpenMode.ForRead)
      as BlockTable;
    BlockTableRecord bTR = trans.GetObject(
      bT[BlockTableRecord.ModelSpace],
      OpenMode.ForWrite)
        as BlockTableRecord;
      Polyline pline = new Polyline();
    pline.Closed = true;
    pline.Thickness = 0.0;
    pline.SetPropertiesFrom(bref);
    pline.Normal = Normal;
    pline.Elevation = elevation;
    pline.ColorIndex = 1;
      pline.AddVertexAt(0,
      new Point2d(
        boundary[0].X, boundary[0].Y), 0, 0, 0);
    pline.AddVertexAt(1,
      new Point2d(
        boundary[0].X, boundary[1].Y), 0, 0, 0);
    pline.AddVertexAt(2,
      new Point2d(
        boundary[1].X, boundary[1].Y), 0, 0, 0);
    pline.AddVertexAt(3,
      new Point2d(
        boundary[1].X, boundary[0].Y), 0, 0, 0);
      pline.TransformBy(bref.BlockTransform);
      bTR.AppendEntity(pline);
    trans.AddNewlyCreatedDBObject(pline, true);
    trans.Commit();
  }
}

## 评论

**内容**: Antti Karanta said...
I tested this on AutoCAD 2015. The only required change was to change acdb19.dll => acdb20.dll
Running the command works fine the first time. However, it leaves the system in unstable state as running the same command again for the same object causes Runtime error R6025 - pure virtual function call, i.e. crashes AutoCAD. The same thing happens if one tries to run the XCLIP command on the object first clipped with the given code. NB, running XCLIP several times for an object does not crash AutoCAD.
The crash happens on this line:
PromptPointResult ppr = ed.GetPoint( ppo );

Any ideas on how to get around this?
The same problem happens with similar code presented in http://through-the-interface.typepad.com/through_the_interface/2010/11/adding-a-2d-spatial-filter-to-perform-a-simple-xclip-on-an-external-reference-in-autocad-using-net.html
Reply
11/13/2015 at 01:16 AM

---
**内容**: Augusto Goncalves said in reply to Antti Karanta...
Thanks for your feedback Antti.
As Kean also mentioned, can you provide the steps so we can reproduce it?
Thanks!
Augusto Goncalves
Reply
11/13/2015 at 05:36 AM

---
**内容**: Antti Karanta said...
I thought I did. :) But I'll reiterate:
Either: run your command ("NetClip") twice on the same block reference.
Or: run "NetClip" on a block reference and then XCLIP on it (just press enter to select defaults of all the choices).
The first alternative is a little better as you can more easily see which call causes AutoCAD to crash.
PS. I forgot to mention that I am running 64-bit AutoCAD on Windows 7.
Reply
11/13/2015 at 05:40 AM

---
**内容**: Augusto Goncalves said in reply to Antti Karanta...
And what kind of drawing? Anything special?
Reply
11/13/2015 at 05:43 AM

---
**内容**: Antti Karanta said...
No special drawing needed. I tested this starting with an empty drawing (created using acadiso.dwt) into which I drew six circles, which I then combined to a block.
I can send you the file if you wish. As it does not seem possible to attach binaries to this post, send me an address I can send it to to antti.karanta at-sign neromsoft.com
Reply
11/13/2015 at 05:49 AM

---
**内容**: Antti Karanta said in reply to Antti Karanta...
I now tested this also on AutoCAD 2016 (64-bit on Windows 8) and there is no crash. So apparently the crash only occurs on AutoCAD 2015 (and possibly older, can't say).
There is another strange effect (on AutoCAD 2016), though - when running "NETCLIP" twice on the same block reference the latter command does no clipping - it just draws the boundary.
If it is of importance, I drew the latter clip region smaller than the original.
I wrote detailed instructions on how to reproduce the crash as a reply to Kean's post.
Reply
11/16/2015 at 12:59 AM

---
**内容**: Augusto Goncalves said in reply to Antti Karanta...
I would suggest the same as Kean, it's likely something on the API side that was improved on 2016.
Reply
11/17/2015 at 12:07 PM

---
**内容**: Antti Karanta said in reply to Augusto Goncalves...
Ok, thanks.
Do you have any ideas on why the second invocation of NETCLIP fails to change the clipping rectangle? The boundary is drawn ok, but that is a totally independent operation.
Should the existing SpatialFilter be first programmatically deleted before assigning a new one with addFilter32/64?
Running xclip twice in a row for a block reference does change the clipping.
Reply
11/18/2015 at 12:51 AM

---
**内容**: Augusto Goncalves said in reply to Antti Karanta...
I would need to debug it more, but seems related to the dictionary entry.
Reply
11/18/2015 at 06:13 AM

---
