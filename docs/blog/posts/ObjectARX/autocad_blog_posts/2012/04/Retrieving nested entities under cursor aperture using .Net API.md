---
title: "Retrieving nested entities under cursor aperture using .Net API"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
description: "I was asked this useful question by an ADN member a while ago, being able to retrieve in real time the entities under the cursor aperture, as the u..."
author: Autodesk
---
# Retrieving nested entities under cursor aperture using .Net API

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/retrieving-nested-entities-under-cursor-aperture-using-net-api.html

## 文章内容

By Philippe Leefsma
  I was asked this useful question by an ADN member a while ago, being able to retrieve in real time the entities under the cursor aperture, as the user is moving the mouse pointer. If the question is not the most challenging, looking for retrieving as well nested entities, like for example the ones contained in an xref, is making the task more interesting…
Retrieving entities at a specified point is unfortunately not directly exposed through managed functions, so one needs to rely on P/Invoking, among others, acedSSGet and acedSSName with the “:N” option. However this later will not return entities being nested, typically in a block reference. In order to retrieve nested entities, invoking acedSSNameX is required, and due to the signature of this method, P/Invoking it from .Net is not very intuitive: declaration of a custom structure “resbuf” is required, as well as relying on a piece of unsafe code in order to map managed and unmanaged objects.
Running command “UnderCursorNested” will dump to commandline any entity under mouse cursor being a block reference placed on layer “0”, or any nested entity contained by that block reference, including entities from an xref. This filtering condition can of course be modified to suits your needs. 
  class ArxImports
{
    public struct ads_name
    {
        public IntPtr a;
        public IntPtr b;
    };
      [StructLayout(LayoutKind.Sequential, Size = 32)]
    public struct resbuf { }
      [DllImport("acad.exe",
        CallingConvention = CallingConvention.Cdecl,
        CharSet = CharSet.Unicode,
        ExactSpelling = true)]
    public static extern PromptStatus acedSSGet(
        string str, IntPtr pt1, IntPtr pt2,
        IntPtr filter, out ads_name ss);
      [DllImport("acad.exe",
        CallingConvention = CallingConvention.Cdecl,
        CharSet = CharSet.Unicode,
        ExactSpelling = true)]
    public static extern PromptStatus acedSSFree(ref ads_name ss);
      [DllImport("acad.exe",
        CallingConvention = CallingConvention.Cdecl,
        CharSet = CharSet.Unicode,
        ExactSpelling = true)]
    public static extern PromptStatus acedSSLength(
        ref ads_name ss, out int len);
      [DllImport("acad.exe",
        CallingConvention = CallingConvention.Cdecl,
        CharSet = CharSet.Unicode,
        ExactSpelling = true)]
    public unsafe static extern PromptStatus acedSSNameX(
        resbuf** rbpp, ref ads_name ss, int i);
}
  class CursorDetectCls
{
    Editor _ed;
      [CommandMethod("UnderCursorNested")]
    public void UnderCursorNested()
    {
        _ed = Application.DocumentManager.MdiActiveDocument.Editor;
          //Set up PointMonitor event
        _ed.PointMonitor +=
            new PointMonitorEventHandler(PointMonitorMulti);
    }
      void PointMonitorMulti(object sender, PointMonitorEventArgs e)
    {
        //Filters only block references (INSERT)
        //that are on layer "0"
        ResultBuffer resbuf = new ResultBuffer(
            new TypedValue(-4, "<and"),
            new TypedValue(0, "INSERT"),
            new TypedValue(8, "0"),
            new TypedValue(-4, "and>"));
          ObjectId[] ids = FindAtPointNested(
            _ed.Document,
            e.Context.RawPoint,
            true,
            resbuf.UnmanagedObject);
          //Dump result to commandline
        foreach (ObjectId id in ids)
        {
            _ed.WriteMessage("\n - Entity: {0} [Id:{1}]",
                id.ObjectClass.Name,
                id.ToString());
        }
    }
      //Retruns ObjectIds of entities at a specific position
    //Including nested entities in block references
    static public ObjectId[] FindAtPointNested(
        Document doc,
        Point3d worldPoint,
        bool selectAll,
        IntPtr filter)
    {
        System.Collections.Generic.List<ObjectId> ids =
            new System.Collections.Generic.List<ObjectId>();
          Matrix3d wcs2ucs =
            doc.Editor.CurrentUserCoordinateSystem.Inverse();
          Point3d ucsPoint = worldPoint.TransformBy(wcs2ucs);
          string arg = selectAll ? "_:E:N" : "_:N";
          IntPtr ptrPoint = Marshal.UnsafeAddrOfPinnedArrayElement(
            worldPoint.ToArray(), 0);
          ArxImports.ads_name sset;
          PromptStatus prGetResult = ArxImports.acedSSGet(
            arg, ptrPoint, IntPtr.Zero, filter, out sset);
          int len;
        ArxImports.acedSSLength(ref sset, out len);
          //Need to rely on unsafe code in order to use pointers *
        unsafe
        {
            for (int i = 0; i < len; ++i)
            {
                ArxImports.resbuf rb = new ArxImports.resbuf();
                  ArxImports.resbuf* pRb = &rb;
                  if (ArxImports.acedSSNameX(&pRb, ref sset, i) !=
                    PromptStatus.OK)
                    continue;
                  //Create managed ResultBuffer from our resbuf struct
                using (ResultBuffer rbMng = DisposableWrapper.Create(
                    typeof(ResultBuffer),
                    (IntPtr)pRb,
                    true) as ResultBuffer)
                {
                    foreach (TypedValue tpVal in rbMng)
                    {
                        //Not interested if it isn't an ObjectId
                        if (tpVal.TypeCode != 5006) //RTENAME
                            continue;
                          ObjectId id = (ObjectId)tpVal.Value;
                          if (id != null)
                            ids.Add(id);
                    }
                }
            }
        }
          ArxImports.acedSSFree(ref sset);
          return ids.ToArray();
    }
}

## 评论

**内容**: PDOTeam said...
I noticed you used "acad.exe" in the PInvoke.
With 2013, we seem to be changing to use the AcCore.dll for PInvoke for some commands. How do you know when to use "acad.exe" and "AcCore.dll" (other than trial and error)?
Reply
04/24/2012 at 06:11 AM

---
**内容**: Philippe said...
Yes that's a good point. With the introduction of AcCore.dll some exported arx methods may be moved to it whereas some others remains in acad.exe.
I don't have the list of all methods that will be moved to AcCore.dll, however it is pretty straightforward to discover them with a tool such as "depends.exe": simply open AcCore.dll from your AutoCAD install directory using this utility, you will see all exported methods it contains. It has an option to copy the methods names, so you can easily put them in a text file and perform a keyword search for example.
Depends is a free tool available here: http://www.dependencywalker.com/
Reply
04/24/2012 at 06:18 AM

---
**内容**: PDOTeam said...
Thanks for the tip on Depends!
Reply
04/24/2012 at 08:43 AM

---
**内容**: Kerry Brown said...

Regarding acad.exe and AcCore.dll export dump
I've posted a .txt file listing here :
http://www.theswamp.org/index.php?topic=41527.0
Reply
04/24/2012 at 07:48 PM

---
**内容**: kaefer said...
I was musing about getting around the unsafe keyword in this example by changing the extern declaration of acadSSNameX from resbuf** rbpp to out IntPtr rbpp (cf. acedInvoke), and about using the predefined global::AdsName struct.
http://www.theswamp.org/index.php?topic=41569.0
Many thanks for your collective wisdom!
Reply
04/24/2012 at 11:52 PM

---
**内容**: Max Senft said...
I don't know if commenting on a 2 year old post is clever, but I thought it is important to mention:
I just implemented (using AutoCAD 2010) a "virtual selection" by using the PromptNestedEntityOptions' members "NonInteractivePickPoint" and "UseNonInteractivePickPoint". I actually did not use it for a "continuing realtime" but used the PromptNestedEntityResult' member PickedPoint. But without the need of any additionally imported functions.
At another point of my software I "translated" the system's cursor position to AutoCAD Point3d using the Editor.PointToWorld() function - which you did not need here because the PointMonitor already supplies the RawPoint. I just wanted to mention it. :)
Reply
04/17/2014 at 06:26 AM

---
