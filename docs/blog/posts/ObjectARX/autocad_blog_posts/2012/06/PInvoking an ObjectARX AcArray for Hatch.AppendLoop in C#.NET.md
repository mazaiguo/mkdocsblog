---
title: "PInvoking an ObjectARX AcArray for Hatch.AppendLoop in C#.NET"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C#
  - C++
  - Hatch
  - ObjectARX
description: "it’s funny how some things turn out Just recently, I had a developer telling me about some Mixed Mode DLL issues he was having; he needed his Mixed..."
author: Autodesk
---
# PInvoking an ObjectARX AcArray for Hatch.AppendLoop in C#.NET

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/pinvoking-an-objectarx-acarray-for-hatchappendloop-in-cnet.html

## 文章内容

by Fenton Webb
it’s funny how some things turn out Just recently, I had a developer telling me about some Mixed Mode DLL issues he was having; he needed his Mixed Mode DLL to run a specific version of the .NET framework. Apparently, that was because without that specific version of the runtime, other parts of his program simply wouldn’t work.
I like to steer away from Mixed Mode DLLs because they are a real pain moving forward, so my immediate question was, “Why do you need a Mixed Mode DLL anyway?”…
After a long chat, it turns out that the only real reason he needed it was to be able to call a specific version of the ObjectARX AcDbHatch::appendLoop() function, which is not exposed in .NET for some reason – here’s the function definition in ObjectARX…
Acad::ErrorStatus appendLoop( Adesk::Int32 loopType,
const AcGePoint2dArray& vertices,
const AcGeDoubleArray& bulges );
  The main problem with PInvoking this particular function is that we don’t expose an equivalent AcGeDoubleArray in our .NET API (I suspect that perhaps for this reason, this function was never exposed). Anyway, we (DevTech) declared a while back that this function was not supported to PInvoke, which is why this developer insisted that he needed the Mixed Mode DLL, but of course this stance doesn’t help with this particular Mixed Mode DLL problem so I decided to solve it.
Everything is PInvoke’able, it just depends on how much work you think it’s worth to put in to achieve it. I figured that the possible workarounds to this problem were to either
PInvoke
Work out the Bulge geometry using AcGeCurves and Edge types
to me, PInvoke’ing was much less work (and of course much more fun! )
So, to PInvoke this particular appendLoop() function would take some careful thought because specifying an array of doubles via .NET and then passing that array to Unmanaged code is laced with danger. The reason is mainly down to the .NET GC – anything allocated by the GC could potentially be moved around, and that will simply crash any unmanaged code that uses it. What was needed was to simply pin the GC allocated memory so that the GC knew not to mess with it. Pinning memory in C#.NET is done using the fixed keyword.
The other thing to consider is the actual class definition, the data members you define .NET side must be the same size and in the same order as the corresponding unmanaged version; for this you can use the StructLayout attribute,
e.g.
[StructLayout(LayoutKind.Auto)]
So just before you take a look at the code, I wanted to welcome all to memory pointers and addresses in .NET!! All of which requires the unsafe keyword to mark that part of the code as being dangerous to buffer overruns, etc, so that the .NET runtime can somehow protect itself from hackers
// PInvoking appendLoop() using "fixed" memory in an "unsafe" .NET context
// by Fenton Webb, DevTech, Autodesk, 05/06/2012
[CommandMethod("HatchLoop")]
static public void HatchLoop()
{
Document doc = Application.DocumentManager.MdiActiveDocument;
Database db = doc.Database;
Editor ed = doc.Editor;
using (Transaction Tx = db.TransactionManager.StartTransaction())
{
Hatch hatch = new Hatch();
hatch.SetDatabaseDefaults();
hatch.Elevation = 0.0;
hatch.Normal = Vector3d.ZAxis;
hatch.SetHatchPattern(HatchPatternType.PreDefined, "AR-B816");
Point2dCollection vertices = new Point2dCollection();
vertices.Add(new Point2d(0, 0));
vertices.Add(new Point2d(100, 0));
vertices.Add(new Point2d(100, 50));
vertices.Add(new Point2d(0, 50));
vertices.Add(new Point2d(0, 0));
DoubleCollection bulges = new DoubleCollection();
bulges.Add(0.0);
bulges.Add(0.0);
bulges.Add(0.0);
bulges.Add(0.0);
bulges.Add(0.0);
unsafe
{
// create the AcGePoint2dArray marshaler class
AcArray verticesAcArray = new AcArray();
// grab the double array
Point2d[] verticesArray = vertices.ToArray();
// get a pointer and pin it so the GC won't move it
fixed (Point2d* verticesPtr = &verticesArray[0])
{
// record the acarray properties
verticesAcArray.array = (IntPtr)verticesPtr;
verticesAcArray.mPhysicalLen = verticesArray.Length;
verticesAcArray.mLogicalLen = verticesArray.Length;
// create the AcGeDoubleArray marshaler class
AcArray bulgesAcArray = new AcArray();
double[] bulgesArray = bulges.ToArray();
// get a pointer and pin it so the GC won't move it
fixed (double* bulgesPtr = &bulgesArray[0])
{
// record the acarray properties
bulgesAcArray.array = (IntPtr)bulgesPtr;
bulgesAcArray.mPhysicalLen = bulgesArray.Length;
bulgesAcArray.mLogicalLen = bulgesArray.Length;
appendLoop(
hatch.UnmanagedObject,
HatchLoopType.kDefault,
ref verticesAcArray.array,
ref bulgesAcArray.array);
hatch.EvaluateHatch(false);
BlockTableRecord btr = Tx.GetObject(db.CurrentSpaceId, OpenMode.ForWrite) as BlockTableRecord;
btr.AppendEntity(hatch);
Tx.AddNewlyCreatedDBObject(hatch, true);
Tx.Commit();
}
}
}
}
}
enum HatchLoopType
{
kDefault = 0,
kExternal = 1,
kPolyline = 2,
kDerived = 4,
kTextbox = 8,
kOutermost = 0x10,
kNotClosed = 0x20,
kSelfIntersecting = 0x40,
kTextIsland = 0x80,
kDuplicate = 0x100,
kIsAnnotative = 0x200,
kDoesNotSupportScale = 0x400,
kForceAnnoAllVisible = 0x800,
kOrientToPaper = 0x1000,
kIsAnnotativeBlock = 0x2000
};
[StructLayout(LayoutKind.Auto)]
struct AcArray
{
public IntPtr array;
public int mPhysicalLen;
public int mLogicalLen;
public int mGrowLen;
};
[DllImport("acdb18.dll", CallingConvention = CallingConvention.ThisCall,
CharSet = CharSet.Unicode,
EntryPoint = "?appendLoop@AcDbHatch@@QAE?AW4ErrorStatus@Acad"+
"@@JABV?$AcArray@VAcGePoint2d@@V?$AcArrayMemCopyReallocator@"+
"VAcGePoint2d@@@@@@ABV?$AcArray@NV?$AcArrayMemCopyReallocator@N@@@@@Z")]
private static extern int appendLoop32(IntPtr ths,
HatchLoopType loopType,
ref IntPtr vertices,
ref IntPtr bulges);
[DllImport("acdb18.dll", CallingConvention = CallingConvention.ThisCall,
CharSet = CharSet.Unicode,
EntryPoint = "?appendLoop@AcDbHatch@@QEAA?AW4ErrorStatus@Acad"+
"@@JAEBV?$AcArray@VAcGePoint2d@@V?$AcArrayMemCopyReallocator@"+
"VAcGePoint2d@@@@@@AEBV?$AcArray@NV?$AcArrayMemCopyReallocator@N@@@@@Z")]
private static extern int appendLoop64(IntPtr ths,
HatchLoopType loopType,
ref IntPtr vertices,
ref IntPtr bulges);
private static int appendLoop(IntPtr ths,
HatchLoopType loopType,
ref IntPtr vertices,
ref IntPtr bulges)
{
if (Marshal.SizeOf(IntPtr.Zero) > 4)
return appendLoop64(ths, loopType, ref vertices, ref bulges);
return appendLoop32(ths, loopType, ref vertices, ref bulges);
}

## 评论

**内容**: kaefer said...
Thanks for this!
Haven't you inadvertantly switched the order of the arguments in the call to appendloop? (That is, param. #3 should be ref verticesAcArray and param. #4 ref bulgesAcArray)
And isn't there another way of pinning memory in .NET, via GCHandle.Alloc, instead of unsafe/fixed?
Reply
06/06/2012 at 12:46 AM

---
**内容**: Fenton Webb said...
Thanks for saying thanks, I really appreciate it.
Yes, you are right - not making excuses but that happened when I was reformatting the code for the blog :-S Sorry about that, it's fixed now.
About the GCHandle.Alloc - you can use that, but it's not very Exception friendly and it's easy to leak memory, my way, no leaks ever.
Have fun with this stuff :-)
Reply
06/06/2012 at 10:31 AM

---
