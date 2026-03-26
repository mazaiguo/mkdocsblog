---
title: "Detecting entities under cursor while selection is running"
date: 2014-02-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - C#
  - C++
  - ObjectARX
description: "The PointMonitor callback in .Net lets you access the entities that are under the cursor aperture as the user is hovering the mouse, however this f..."
author: Autodesk
---
# Detecting entities under cursor while selection is running

发布日期: 2014-02-01

原始链接: https://adndevblog.typepad.com/autocad/2014/02/detecting-entities-under-cursor-while-selection-is-running.html

## 文章内容

By Philippe Leefsma
The PointMonitor callback in .Net lets you access the entities that are under the cursor aperture as the user is hovering the mouse, however this feature gets disabled while running an Editor.GetEntity.
There is a workaround for that behavior that involves P/Invoking a bunch of ObjectARX methods, as we like to do. Below is a C# sample for that.
Nested entities can also be detected as exposed in this previous post:
Retrieving nested entities under cursor aperture using .Net API
  class ArxImports
{
    public struct ads_name
    {
        public IntPtr a;
        public IntPtr b;
    };
      [StructLayout(LayoutKind.Sequential, Size = 32)]
    public struct resbuf { }
      [DllImport("accore.dll",
        CallingConvention = CallingConvention.Cdecl,
        CharSet = CharSet.Unicode,
        ExactSpelling = true)]
    public static extern PromptStatus acedSSGet(
        string str, IntPtr pt1, IntPtr pt2,
        IntPtr filter, out ads_name ss);
      [DllImport("accore.dll",
        CallingConvention = CallingConvention.Cdecl,
        CharSet = CharSet.Unicode,
        ExactSpelling = true)]
    public static extern PromptStatus acedSSFree(
        ref ads_name ss);
      [DllImport("accore.dll",
        CallingConvention = CallingConvention.Cdecl,
        CharSet = CharSet.Unicode,
        ExactSpelling = true)]
    public static extern PromptStatus acedSSLength(
        ref ads_name ss, out int len);
      [DllImport("accore.dll",
        CallingConvention = CallingConvention.Cdecl,
        CharSet = CharSet.Unicode,
        ExactSpelling = true)]
    public static extern PromptStatus acedSSName(
        ref ads_name ss, int i, out ads_name name);
      [DllImport("acdb19.dll",
        CallingConvention = CallingConvention.Cdecl,
        CharSet = CharSet.Unicode,
        ExactSpelling = true)]
    public static extern ErrorStatus acdbGetObjectId(
        out ObjectId id, ref ads_name name);
}
  static System.Collections.Generic.List<ObjectId>
    FindAtPoint(Point3d worldPoint, bool selectAll = true)
{
    System.Collections.Generic.List<ObjectId> ids =
        new System.Collections.Generic.List<ObjectId>();
      Document doc = Application.DocumentManager.MdiActiveDocument;
      Matrix3d wcs2ucs =
        doc.Editor.CurrentUserCoordinateSystem.Inverse();
      Point3d ucsPoint = worldPoint.TransformBy(wcs2ucs);
               string arg = selectAll ? ":E" : string.Empty;
               IntPtr ptrPoint = Marshal.UnsafeAddrOfPinnedArrayElement(
        worldPoint.ToArray(), 0);
      ArxImports.ads_name sset;
      PromptStatus prGetResult = ArxImports.acedSSGet(
        arg, ptrPoint, IntPtr.Zero, IntPtr.Zero, out sset);
      int len;
    ArxImports.acedSSLength(ref sset, out len);
      if (len <= 0)
        return ids;
               for (int i = 0; i < len; ++i)
    {
        ArxImports.ads_name name;
          if (ArxImports.acedSSName(
            ref sset, i, out name) != PromptStatus.OK)
            continue;
                        ObjectId id;
          if (ArxImports.acdbGetObjectId(
            out id, ref name) != ErrorStatus.OK)
            continue;
          ids.Add(id);
    }
      ArxImports.acedSSFree(ref sset);
      return ids;
}
  Editor AdnEditor;
  [CommandMethod("PointMonitorSelection")]
public void PointMonitorSelection()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      try
    {
        AdnEditor = doc.Editor;
          AdnEditor.PointMonitor +=
            FindUsingPointMonitor;
                PromptEntityOptions peo = new PromptEntityOptions(
            "Select an entity...");
          PromptEntityResult per = ed.GetEntity(peo);
          if (per.Status != PromptStatus.OK)
            return;
          ObjectId id = per.ObjectId;
          ed.WriteMessage("\n - Selected " +
            " Entity: " + id.ObjectClass.Name +
            " Id: " + id.ToString());
    }
    catch(System.Exception ex)
    {
        ed.WriteMessage("\nException: " + ex.Message);
    }
    finally
    {
        AdnEditor.PointMonitor -=
            FindUsingPointMonitor;
    }
}
  void FindUsingPointMonitor(object sender, PointMonitorEventArgs e)
{
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      // Not working when running editor selection
    //foreach (var subId in e.Context.GetPickedEntities())
    //{
    //    foreach (var id in subId.GetObjectIds())
    //    {
    //        ed.WriteMessage("\n - " +
    //            " Entity: " + id.ObjectClass.Name +
    //            " Id: " + id.ToString());
    //    }
    //}
      var ids = FindAtPoint(e.Context.RawPoint);
      foreach (var id in ids)
    {
        ed.WriteMessage("\n + " +
            " Entity: " + id.ObjectClass.Name +
            " Id: " + id.ToString());
    }
}

## 评论

**内容**: Winslow North said...
the point monitor worked great for me in ACAD2014 however now we are using ACAD2016 it will not work because of the DLLImport of acdb19.dll. Is there a way to make it load eighter version since we now have both versions of AutoCAD in house?
Reply
01/13/2017 at 09:30 AM

---
**内容**: Andy Morch said...
There is a little bug in 'FindAtPoint'.
Instead of:
string arg = selectAll ? ":E" : string.Empty;
It must be:
string arg = selectAll ? "_:E" : string.Empty;
Otherwise 'SelectAll' does not work!
Reply
09/16/2020 at 05:15 AM

---
