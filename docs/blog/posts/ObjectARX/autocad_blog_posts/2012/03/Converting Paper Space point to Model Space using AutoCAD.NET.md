---
title: "Converting Paper Space point to Model Space using AutoCAD.NET"
date: 2012-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "Recently I tried to find some information on how to convert a Paper Space point to a Model Space point, and was shocked to find there was no simple..."
author: Autodesk
---
# Converting Paper Space point to Model Space using AutoCAD.NET

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/converting-paper-space-point-to-model-space-using-autocadnet.html

## 文章内容

By Fenton Webb
Recently I tried to find some information on how to convert a Paper Space point to a Model Space point, and was shocked to find there was no simple to use sample code!!! Perhaps I missed something obvious, nevertheless, I opted to create my own and share it with you.
The code below utilizes the acedTrans() (which has been around since the R11 ADS days) using PInvoke, it’s very simple to use when you know how.
To run and test the code out:
Run AutoCAD and load the code below
Switch to Paper Space, either click the Layout tab or set TILEMODE=0
Create a VPort
Make sure you have TILEMODE=0
Run my “ps2ms” command and click somewhere over the MS VPort. You will see a DBPoint appear directly under your cursor, but in Model space.
If you can’t see the DBPoint, simply set PDSIZE=10 and PDMODE=98
Hope you like it.
    // convert a PS point to MS and then add a DBPoint to MS to show where we picked
    // by Fenton Webb, DevTech, Autodesk, 20/Aug/2012
#if NOTACAD2013
  [DllImport("acad.exe", CallingConvention = CallingConvention.Cdecl, EntryPoint="acedTrans")]
#else
    [DllImport("accore.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "acedTrans")]
#endif
    static extern int acedTrans(double[] point, IntPtr fromRb, IntPtr toRb, int disp, double[] result);
    [CommandMethod("ps2ms", CommandFlags.NoTileMode)]
    static public void ps2ms()
    {
      Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      // pick some point in PS
      PromptPointResult res = ed.GetPoint("Pick Model Space Point");
      if (res.Status == PromptStatus.OK)
      {
        // now to make sure this works for all viewpoints
        ResultBuffer psdcs = new ResultBuffer(new TypedValue(5003, 3));
        ResultBuffer dcs = new ResultBuffer(new TypedValue(5003, 2));
        ResultBuffer wcs = new ResultBuffer(new TypedValue(5003, 0));
        double[] retPoint = new double[] { 0, 0, 0 };
          // translate from the DCS of Paper Space (PSDCS) RTSHORT=3 to
        // the DCS of the current model space viewport RTSHORT=2
        acedTrans(retPoint, psdcs.UnmanagedObject, dcs.UnmanagedObject, 0, retPoint);
        //translate the DCS of the current model space viewport RTSHORT=2
        //to the WCS RTSHORT=0
        acedTrans(retPoint, dcs.UnmanagedObject, wcs.UnmanagedObject, 0, retPoint);
          ObjectId btId = ed.Document.Database.BlockTableId;
        // create a new DBPoint and add it to model space to show where we picked
        using (DBPoint pnt = new DBPoint(new Point3d(retPoint[0], retPoint[1], retPoint[2])))
        using (BlockTable bt = btId.Open(OpenMode.ForRead) as BlockTable)
        using (BlockTableRecord ms = bt[BlockTableRecord.ModelSpace].Open(OpenMode.ForWrite)
                        as BlockTableRecord)
          ms.AppendEntity(pnt);
      }
    }

## 评论

**内容**: J Paterson said...
This sample doesn't return the point in the correct position (not under the cursor) for any view direction.
Reply
08/14/2012 at 08:34 AM

---
**内容**: Gilles Chanteau said...
I think there're two things wrong in the posted code.
1. PSDCS and DCS are related to the active Viewport, so it's needed to activate the Viewport (switching to ModelSpace if it's assumed there's only one viewport in the current layout)
2. retPoint coordinates are DCS coordinates which need to be tranlated to WCS coordinates before passint to the DBPoint ctor.
So, I'd replace:
// Transform from PS point to MS point
ResultBuffer rbFrom = new ResultBuffer(new TypedValue(5003, 3));
ResultBuffer rbTo = new ResultBuffer(new TypedValue(5003, 2));
double[] retPoint = new double[] { 0, 0, 0 };
// translate from from the DCS of Paper Space (PSDCS) RTSHORT=3
// and the DCS of the current model space viewport RTSHORT=2
acedTrans(res.Value.ToArray(), rbFrom.UnmanagedObject, rbTo.UnmanagedObject, 0, retPoint);
with:
// Transform from PS point to MS point
ResultBuffer rbPSDCS = new ResultBuffer(new TypedValue(5003, 3));
ResultBuffer rbDCS = new ResultBuffer(new TypedValue(5003, 2));
ResultBuffer rbWCS = new ResultBuffer(new TypedValue(5003, 0));
double[] retPoint = new double[] { 0, 0, 0 };
ed.SwitchToModelSpace();
using (Viewport vp = (Viewport)ed.CurrentViewportObjectId.Open(OpenMode.ForRead))
{
// translate from from the DCS of Paper Space (PSDCS) RTSHORT=3
// to the DCS of the current model space viewport RTSHORT=2
acedTrans(res.Value.ToArray(), rbPSDCS.UnmanagedObject, rbDCS.UnmanagedObject, 0, retPoint);
//translate the DCS of the current model space viewport RTSHORT=2
//to the WCS RTSHORT=0
acedTrans(retPoint, rbDCS.UnmanagedObject, rbWCS.UnmanagedObject, 0, retPoint);
}
ed.SwitchToPaperSpace();
Or, rather than P/Invoking acedTrans, use some extension methods defined in the GeometryExtension library:
http://www.theswamp.org/index.php?topic=31865.msg373672#msg373672
Reply
08/15/2012 at 02:12 AM

---
**内容**: Gilles Chanteau said in reply to Gilles Chanteau...
A more complete reply with nicer code formatting at TheSwamp:
http://www.theswamp.org/index.php?topic=42503.msg476994#msg476994
Reply
08/15/2012 at 04:50 AM

---
**内容**: BKSpurgeon said...
Hello
what is the purpose of the result buffer class?
the arx documentation is very limited on that point.
rgds
Ben
Reply
12/28/2016 at 09:02 PM

---
