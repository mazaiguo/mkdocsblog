---
title: "Changing zoom in paperspace viewport"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Database
description: "The zoom of a viewport can be changed by setting the ViewHeight and ViewCenter of the viewports. This sample code  iterates through all of the layo..."
author: Autodesk
---
# Changing zoom in paperspace viewport

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/changing-zoom-in-paperspace-viewport.html

## 文章内容

By Augusto Goncalves
The zoom of a viewport can be changed by setting the ViewHeight and ViewCenter of the viewports. This sample code  iterates through all of the layouts and adjust this properties using the drawing extends information, so run the code in a drawing that has at least one entity.
[CommandMethod("changeZoom")]
static public void CommandChangeViewportZoom()
{
  // access database and editor
  Database db = Application.DocumentManager.
    MdiActiveDocument.Database;
  Editor ed = Application.DocumentManager.
    MdiActiveDocument.Editor;
    using (Transaction tr = db.
    TransactionManager.StartTransaction())
  {
    LayoutManager layoutMgr = LayoutManager.Current;
    Layout layoutObj;
    DBDictionary layoutDict;
      ed.WriteMessage("Number of Layouts = {0}\n",
      layoutMgr.LayoutCount);
    ed.WriteMessage("Current Layout = {0}\n",
      layoutMgr.CurrentLayout);
      Point3d x_Min = db.Extmin;
    Point3d x_Max = db.Extmax;
      using (layoutDict = tr.GetObject(db.LayoutDictionaryId,
      OpenMode.ForRead) as DBDictionary)
    {
      foreach (DictionaryEntry layoutEntry in layoutDict)
      {
        using (layoutObj = tr.GetObject(
          (ObjectId)(layoutEntry.Value),
          OpenMode.ForRead) as Layout)
        {
            // Set the CurrentLayout to the layout
          // if it is not Modelspace
          if (layoutObj.LayoutName != "Model")
            layoutMgr.CurrentLayout = layoutObj.LayoutName;
            ed.WriteMessage("Layout Name = {0}\n",
            layoutObj.LayoutName);
          BlockTableRecord r = tr.GetObject(
            layoutObj.BlockTableRecordId,
            OpenMode.ForRead) as BlockTableRecord;
          foreach (ObjectId obj in r)
          {
            DBObject dbobj = tr.GetObject(obj, OpenMode.ForRead);
            Viewport vp = dbobj as Viewport;
            if (vp != null)
            {
              ed.WriteMessage("\nnumber of Viewport = {0}",
                vp.Number);
                // get the screen aspect ratio to calculate
              // the height and width
              double mScrRatio;
              // width/height
              mScrRatio = (vp.Width / vp.Height);
                Point3d mMaxExt = db.Extmax;
              Point3d mMinExt = db.Extmin;
                Extents3d mExtents = new Extents3d();
              mExtents.Set(mMinExt, mMaxExt);
                // prepare Matrix for DCS to WCS transformation
              Matrix3d matWCS2DCS;
              matWCS2DCS = Matrix3d.PlaneToWorld(vp.ViewDirection);
              matWCS2DCS = Matrix3d.Displacement(
                vp.ViewTarget - Point3d.Origin)
                * matWCS2DCS;
              matWCS2DCS = Matrix3d.Rotation(
                -vp.TwistAngle, vp.ViewDirection,
                vp.ViewTarget) * matWCS2DCS;
              matWCS2DCS = matWCS2DCS.Inverse();
                // tranform the extents to the DCS
              // defined by the viewdir
              mExtents.TransformBy(matWCS2DCS);
                // width of the extents in current view
              double mWidth;
              mWidth = (mExtents.MaxPoint.X - mExtents.MinPoint.X);
                // height of the extents in current view
              double mHeight;
              mHeight = (mExtents.MaxPoint.Y - mExtents.MinPoint.Y);
                // get the view center point
              Point2d mCentPt = new Point2d(
                ((mExtents.MaxPoint.X + mExtents.MinPoint.X) * 0.5),
                ((mExtents.MaxPoint.Y + mExtents.MinPoint.Y) * 0.5));
                // check if the width 'fits' in current window,
              // if not then get the new height as
              // per the viewports aspect ratio
              if (mWidth > (mHeight * mScrRatio))
                mHeight = mWidth / mScrRatio;
                // set the viewport parameters
              if (vp.Number == 2)
              {
                vp.UpgradeOpen();
                // set the view height - adjusted by 1%
                vp.ViewHeight = mHeight * 1.01;
                // set the view center
                vp.ViewCenter = mCentPt;
                vp.Visible = true;
                vp.On = true;
                vp.UpdateDisplay();
                ed.SwitchToModelSpace();
                Application.SetSystemVariable("CVPORT", vp.Number);
              }
              if (vp.Number == 3)
              {
                vp.UpgradeOpen();
                vp.ViewHeight = mHeight * 1.25;
                //set the view center
                vp.ViewCenter = mCentPt;
                vp.Visible = true;
                vp.On = true;
                vp.UpdateDisplay();
                ed.SwitchToModelSpace();
                Application.SetSystemVariable("CVPORT", vp.Number);
              }
            }
          }
        }
      }
    }
    tr.Commit();
  }
}

## 评论

**内容**: David said...
Thanks for Post Augosto.
I used your code to meet my requirement with minor changes.
Here it is
_
Public Shared Sub CommandChangeViewportZoom()
Dim Mydb As Database = Application.DocumentManager.MdiActiveDocument.Database
Dim Myed As Editor = Application.DocumentManager.MdiActiveDocument.Editor
Using tr As Transaction = Mydb.TransactionManager.StartTransaction()
Using mylayoutDict As DBDictionary = TryCast(tr.GetObject(Mydb.LayoutDictionaryId, OpenMode.ForRead), DBDictionary)
For Each layoutEntry As DictionaryEntry In mylayoutDict
Using Mylayout As Layout = TryCast(tr.GetObject(DirectCast(layoutEntry.Value, ObjectId), OpenMode.ForRead), Layout)
If Mylayout.LayoutName <> "Model" Then
LayoutManager.Current.CurrentLayout = Mylayout.LayoutName
End If
Dim btr As BlockTableRecord = TryCast(tr.GetObject(Mylayout.BlockTableRecordId, OpenMode.ForRead), BlockTableRecord)
For Each myobjid As ObjectId In btr
Dim vp As Autodesk.AutoCAD.DatabaseServices.Viewport = TryCast(tr.GetObject(myobjid, OpenMode.ForRead), Autodesk.AutoCAD.DatabaseServices.Viewport)
If vp IsNot Nothing Then
' set the viewport parameters
If vp.Number = 2 Then
vp.UpgradeOpen()
vp.CustomScale = 1 / 72.5
vp.Visible = True
vp.On = True
vp.UpdateDisplay()
Myed.SwitchToModelSpace()
Application.SetSystemVariable("CVPORT", vp.Number)
End If
If vp.Number = 3 Then
vp.UpgradeOpen()
vp.CustomScale = 1 / 200
vp.Visible = True
vp.On = True
vp.UpdateDisplay()
Myed.SwitchToModelSpace()
Application.SetSystemVariable("CVPORT", vp.Number)
End If
Else
End If
Next
End Using
Next
End Using
tr.Commit()
End Using
End Sub

Funny thing here is 72.5 scale doesn't work and 200 scale works . Why is that. Am I doing something wrong?
Basiclly if the scale is a standard scale it would be changed but if not it won't. I am confused and a help would be appreciated.
Thanks.
Reply
12/11/2012 at 11:59 AM

---
**内容**: Augusto Goncalves said in reply to David...
Hi David,
Not sure if is there anything special, but running your code on a simple blank drawing, the scale change:
>>>
Command:
Regenerating layout.
Regenerating model - caching viewports.
Command: _.MSPACE
Command: VPSCALE
Initializing...
PS:MS == 1:1.449
Command: _.PSPACE
Command: TESTVP_DAVID_COMMAND
Regenerating model.
Regenerating layout.
Regenerating model - caching viewports.
Regenerating model.
Command: VPSCALE
PS:MS == 1:72.5
<<<
As you can see, the VPSCALE changed to 1:72.5 as specified on the code...
Am I missing any step?
Regards,
Augusto Goncalves
Reply
12/13/2012 at 08:21 AM

---
**内容**: David said...
Hello Augosto,
Thanks for your time.
When there is just one layout you are right and code acts correctly. But when there is more than one layout it acts differently which I couldn't figure out why .
David.
Reply
12/16/2012 at 10:19 AM

---
**内容**: MahmoudAbdElMoneam said...
My Assumption would be that you have to be certain that the viewport number is the one you are changing.
It worked with me after I added another 'if'.
I have a DWG file with a 'Model viewport' inside the 'Paper Space'.
so, I iterated through all the objects and got all the view ports, then worked with the viewport that is on Layer 0 Only.
Reply
04/23/2014 at 05:20 AM

---
**内容**: wang said...
what wrong with my code ,will loop in first sheet is corrent zoom to object rectangle,but for second layout,etc,become not every rectangle/border
using System;
using System.Collections.Generic;
using System.Collections;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Geometry;
using Autodesk.AutoCAD.EditorInput;
namespace latihanCAD
{
public class makeViewport
{
[DllImport("accore.dll", CallingConvention = CallingConvention.Cdecl,
EntryPoint = "?acedSetCurrentVPort@@YA?AW4ErrorStatus@Acad@@PEBVAcDbViewport@@@Z")]
extern static private int acedSetCurrentVPort(IntPtr AcDbVport);

// hapus sheet
public static void DeleteLayout(string name)
{
var doc = Application.DocumentManager.MdiActiveDocument;
var db = HostApplicationServices.WorkingDatabase;
var ed = doc.Editor;

doc.TransactionManager.EnableGraphicsFlush(true);
using (Transaction tr = db.TransactionManager.StartTransaction())
{
var bt = tr.GetObject(db.BlockTableId, OpenMode.ForRead) as BlockTable;
var btr = tr.GetObject(bt[BlockTableRecord.PaperSpace], OpenMode.ForWrite) as BlockTableRecord;
// hapus layout helper jika blm kehapus
var layoutDict1 = tr.GetObject(db.LayoutDictionaryId, OpenMode.ForRead) as DBDictionary;
foreach (DBDictionaryEntry de in layoutDict1)
{
string layoutName = de.Key;
if (layoutName == name)
{
ed.WriteMessage("nama layout /n " + layoutName.ToString());
LayoutManager.Current.DeleteLayout(layoutName); // Delete layout.
break;
tr.TransactionManager.QueueForGraphicsFlush(); doc.TransactionManager.FlushGraphics();
ed.UpdateScreen(); db.Regenmode = true;
}
}

// buat 1 layout dummi agar bisa hapus all paper space
ObjectId layIDhelper = LayoutManager.Current.CreateLayout(name);
// hapus all layout
DBDictionary layoutDict = tr.GetObject(db.LayoutDictionaryId, OpenMode.ForRead) as DBDictionary;
foreach (DBDictionaryEntry de in layoutDict)
{
string layoutName = de.Key;
if (layoutName != "Model" && layoutName != name)
{
ed.WriteMessage("nama layout /n " + layoutName.ToString());
LayoutManager.Current.DeleteLayout(layoutName); // Delete layout.
tr.TransactionManager.QueueForGraphicsFlush(); doc.TransactionManager.FlushGraphics();
ed.UpdateScreen(); db.Regenmode = true;
}
}
tr.Commit();
}

}
//buat class untuk multi value dictionary
class MyObject
{
public Point3d minvalue { get; set; }
public Point3d maxvalue { get; set; }
}

[CommandMethod("addLy")]
public static void AddLayout()
{
var doc = Application.DocumentManager.MdiActiveDocument;
var db = HostApplicationServices.WorkingDatabase;
var ed = doc.Editor;
var name = "helper";
var dic = new Dictionary();
var myListPolyValid = new List();
try
{
// 1. STEP 1 DELETE ALL SHEET DAN BUAT SHEET DUMMY ******************************************************
DeleteLayout(name);
doc.TransactionManager.EnableGraphicsFlush(true);
using (Transaction tr = db.TransactionManager.StartTransaction())
{
var bt = tr.GetObject(db.BlockTableId, OpenMode.ForRead) as BlockTable;
// 2 STEP 2 SELECT COVER GAMBAR *********************************************************************************
var option = new PromptSelectionOptions(); option.MessageForAdding = "\nselect Rectangle/Borders Cover Gambar";
var psr = ed.GetSelection(option, new SelectionFilter(new[] { new TypedValue(0, "LWPOLYLINE,Polyline") }));
if (psr.Status != PromptStatus.OK) return;
SelectionSet acSSet = psr.Value;
if (acSSet == null) return;
var exts = new Extents3d();
foreach (SelectedObject acSSObj in acSSet)
{
Polyline myrec = acSSObj.ObjectId.GetObject(OpenMode.ForWrite) as Polyline;
if (myrec.Area > 0 && myrec.NumberOfVertices > 2)
{
exts.AddExtents(myrec.GeometricExtents);
string value = exts.MinPoint.ToString() + "|" + exts.MaxPoint.ToString();
if (!dic.ContainsKey(value))
{
dic.Add(value, new MyObject { minvalue = exts.MinPoint, maxvalue = exts.MaxPoint });
}
}
else
{
continue;
}
}
if (dic.Count == 0) return;
// 3 STEP 3 BUAT LAYOUT SESUAI JUMLAH SELECTION COVER ************************************************************
string nameLayout = null;
for (int i = 0; i < dic.Count; i++)
{
nameLayout = i.ToString();
ObjectId layoutId = LayoutManager.Current.CreateLayout(nameLayout);
LayoutManager Lm;
LayoutManager.Current.CurrentLayout = nameLayout;
Lm = LayoutManager.Current;
// buat satu layout dahulu agar bisa paperspace lainnya dihapus
//buat setingan kertas di paper space
var lay = (Layout)tr.GetObject(layoutId, OpenMode.ForWrite);
SetPlotSettings(lay, "ISO_full_bleed_A3_(420.00_x_297.00_MM)", "monochrome.ctb", "DWG To PDF.pc3");
tr.TransactionManager.QueueForGraphicsFlush(); doc.TransactionManager.FlushGraphics();
ed.UpdateScreen(); db.Regenmode = true;
//Delete viewport yang ada
var vpIds = lay.GetViewports();
foreach (ObjectId vpId in vpIds)
{
var vp2 = tr.GetObject(vpId, OpenMode.ForWrite) as Viewport;
if (vp2 != null)
{
vp2.UpgradeOpen();
vp2.Erase();
}
}
// 4 STEP 4 BUAT VIEWPORT ********************************************************************************************
var btr = tr.GetObject(bt[BlockTableRecord.PaperSpace], OpenMode.ForWrite) as BlockTableRecord;
var lyID = LayoutManager.Current.GetLayoutId(LayoutManager.Current.CurrentLayout);
LayoutManager acLayoutMgr;
acLayoutMgr = LayoutManager.Current;
// Get the current layout and output its name in the Command Line window
Layout acLayout;
acLayout = tr.GetObject(acLayoutMgr.GetLayoutId(acLayoutMgr.CurrentLayout), OpenMode.ForRead) as Layout;
// Output the name of the current layout and its device
ed.WriteMessage("\nCurrent layout: " + acLayout.LayoutName);
Viewport vp = new Viewport();
vp.SetDatabaseDefaults();
vp.Width = 420;
vp.Height = 297;
vp.CenterPoint = new Point3d(Point3d.Origin.X + (420 * 0.5), Point3d.Origin.Y + (297 * 0.5), 0);
// Add the new object to the block table record and the transaction
ObjectId vpID = btr.AppendEntity(vp);
tr.AddNewlyCreatedDBObject(vp, true);
// Change the view direction
vp.ViewDirection = new Vector3d(0, 0, 0);
// Enable the viewport
// vp.On = true;
// Activate model space in the viewport
doc.Editor.SwitchToModelSpace();
// Set the new viewport current via an imported ObjectARX function
acedSetCurrentVPort(vp.UnmanagedObject);
}
LayoutManager.Current.DeleteLayout(name); // Delete Layout Helper
ed.WriteMessage("count list : {0}" + myListPolyValid.Count.ToString());
tr.TransactionManager.QueueForGraphicsFlush(); doc.TransactionManager.FlushGraphics();
ed.UpdateScreen(); db.Regenmode = true;
tr.Commit();


}
// 5 STEP 5 BUAT ZOOM GAMBAR KE VIEWPORT ********************************************************************************************

using (Transaction tr = db.TransactionManager.StartTransaction())
{
doc.TransactionManager.EnableGraphicsFlush(true);
LayoutManager layoutMgr = LayoutManager.Current;
Layout layoutObj;
DBDictionary layoutDict;
if (dic.Count == 0)
{
return;
}

int n = 0;
int counter = 0;
using (layoutDict = tr.GetObject(db.LayoutDictionaryId, OpenMode.ForRead) as DBDictionary)
{
foreach (DictionaryEntry layoutEntry in layoutDict)
{
ed.WriteMessage("\nisi dictionaryentry " + layoutEntry.Key.ToString());
using (layoutObj = tr.GetObject((ObjectId)(layoutEntry.Value), OpenMode.ForRead) as Layout)
{
// Set the CurrentLayout to the layout
// if it is not Modelspace

if (layoutObj.LayoutName != "Model" && layoutObj.LayoutName != name)
{
Extents3d mExtents = new Extents3d();
layoutMgr.CurrentLayout = layoutObj.LayoutName;
if (n + 1 > dic.Count) return;
var o = dic[dic.Keys.ElementAt(n)];
Point3d mMaxExt = o.maxvalue;
Point3d mMinExt = o.minvalue;
mExtents.Set(mMinExt, mMaxExt);
// ed.WriteMessage("Layout Name = {0}\n", layoutObj.LayoutName);
BlockTableRecord r = tr.GetObject(layoutObj.BlockTableRecordId, OpenMode.ForRead) as BlockTableRecord;

foreach (ObjectId obj in r)
{
DBObject dbobj = tr.GetObject(obj, OpenMode.ForRead);
ed.WriteMessage("\nyang ada dalam loop ke object " + obj.ObjectClass.Name.ToString());
Viewport vp = dbobj as Viewport;
if (vp != null)
{
double mScrRatio;
// width/height
mScrRatio = (vp.Width / vp.Height);
//Point3d mMaxExt = o.maxvalue;
//Point3d mMinExt = o.minvalue;
ed.WriteMessage($"\nmMinExt: {mMinExt} max extend : {mMaxExt} \n nilai n : {(n).ToString()}");
// Extents3d mExtents = new Extents3d();
//mExtents.Set(mMinExt, mMaxExt);
// prepare Matrix for DCS to WCS transformation
Matrix3d matWCS2DCS;
matWCS2DCS = Matrix3d.PlaneToWorld(vp.ViewDirection);
matWCS2DCS = Matrix3d.Displacement(
vp.ViewTarget - Point3d.Origin) * matWCS2DCS;
matWCS2DCS = Matrix3d.Rotation(
-vp.TwistAngle, vp.ViewDirection,
vp.ViewTarget) * matWCS2DCS;
matWCS2DCS = matWCS2DCS.Inverse();
// tranform the extents to the DCS
// defined by the viewdir
mExtents.TransformBy(matWCS2DCS);
// width of the extents in current view
double mWidth;
mWidth = (mExtents.MaxPoint.X - mExtents.MinPoint.X);
// height of the extents in current view
double mHeight;
mHeight = (mExtents.MaxPoint.Y - mExtents.MinPoint.Y);
// get the view center point
Point2d mCentPt = new Point2d(
((mExtents.MaxPoint.X + mExtents.MinPoint.X) * 0.5),
((mExtents.MaxPoint.Y + mExtents.MinPoint.Y) * 0.5));
// check if the width 'fits' in current window,
// if not then get the new height as
// per the viewports aspect ratio
if (mWidth > (mHeight * mScrRatio))
mHeight = mWidth / mScrRatio;
// set the viewport parameters
//if ( vp.Number == 2)
//{
vp.UpgradeOpen();
// set the view height -adjusted by 1 %
vp.ViewHeight = mHeight * 1.01;
// set the view center
vp.ViewCenter = mCentPt;
vp.Visible = true;
vp.On = true;
vp.UpdateDisplay();
// ed.SwitchToModelSpace();
// Application.SetSystemVariable("CVPORT", vp.Number);
ed.Command("_.ZOOM", "_E");
ed.Command("_.ZOOM", ".7X");

ed.Regen();
tr.TransactionManager.QueueForGraphicsFlush(); doc.TransactionManager.FlushGraphics();
ed.UpdateScreen(); db.Regenmode = true;


}

}
ed.WriteMessage($"\ndic.Min point: {o.minvalue} Dic.Max point: {o.maxvalue} \nJlh Lembar : {(n + 1).ToString()}");
n += 1;
}
}
}
}


tr.TransactionManager.QueueForGraphicsFlush(); doc.TransactionManager.FlushGraphics();
ed.UpdateScreen(); db.Regenmode = true;
tr.Commit();
}
}
catch (System.Exception ex)
{
ed.WriteMessage("error in " + ex.ToString());
}
}
// [CommandMethod("AddVP")]
public static void CreateViewport(ObjectId layID)
{
// Get the current document and database, and start a transaction
Document doc = Application.DocumentManager.MdiActiveDocument;
Database db = doc.Database;
var ed = doc.Editor;
using (var tr = db.TransactionManager.StartTransaction())
{
// Open the Block table for read
var bt = tr.GetObject(db.BlockTableId,OpenMode.ForRead) as BlockTable;
// Open the Block table record Paper space for write
var btr = tr.GetObject(bt[BlockTableRecord.PaperSpace],OpenMode.ForWrite) as BlockTableRecord;
var lyID = LayoutManager.Current.GetLayoutId(LayoutManager.Current.CurrentLayout);
LayoutManager Lm;
Lm = LayoutManager.Current;
var lay = (Layout)tr.GetObject(layID, OpenMode.ForRead);

// Switch to the previous Paper space layout
// Application.SetSystemVariable("TILEMODE", 0);
doc.Editor.SwitchToPaperSpace();
// Create a Viewport
Viewport vp = new Viewport();
vp.SetDatabaseDefaults();
vp.Width = 420;
vp.Height = 297;
vp.CenterPoint = new Point3d(Point3d.Origin.X + (420 * 0.5), Point3d.Origin.Y + (297 * 0.5), 0);
// Add the new object to the block table record and the transaction
btr.AppendEntity(vp);
tr.AddNewlyCreatedDBObject(vp, true);
// Change the view direction
vp.ViewDirection = new Vector3d(0, 0, 0);
// Enable the viewport
vp.On = true;
// Activate model space in the viewport
doc.Editor.SwitchToModelSpace();
// Set the new viewport current via an imported ObjectARX function
acedSetCurrentVPort(vp.UnmanagedObject);
// Save the new objects to the database
// doc.Editor.SwitchToPaperSpace();
vp.Locked = true;
tr.Commit();
}
}

// /// membuat plot setting
public static void SetPlotSettings(Layout lay, string pageSize, string styleSheet, string device)
{
using (var ps = new PlotSettings(lay.ModelType))
{
ps.CopyFrom(lay);
var psv = PlotSettingsValidator.Current;
// Set the device
var devs = psv.GetPlotDeviceList();
if (devs.Contains(device))
{
psv.SetPlotConfigurationName(ps, device, null);
psv.SetPlotRotation(ps, PlotRotation.Degrees180); // buat landscape juninawan edit
psv.RefreshLists(ps);
}
// Set the media name/size
var mns = psv.GetCanonicalMediaNameList(ps);
if (mns.Contains(pageSize))
{
psv.SetCanonicalMediaName(ps, pageSize);
}
// Set the pen settings
var ssl = psv.GetPlotStyleSheetList();
if (ssl.Contains(styleSheet))
{
psv.SetCurrentStyleSheet(ps, styleSheet);
}
// Copy the PlotSettings data back to the Layout
var upgraded = false;
if (!lay.IsWriteEnabled)
{
lay.UpgradeOpen();
upgraded = true;
}
lay.CopyFrom(ps);
if (upgraded)
{
lay.DowngradeOpen();
}
}
}

// FUNCTION ZOOM KE OBJECT
///
static public void ChangeZOOM(string KeynameLay,ObjectId valueDic,Point3d x_Max ,Point3d x_Min)
{
// access database and editor
var doc = Application.DocumentManager.MdiActiveDocument;
Database db = Application.DocumentManager.
MdiActiveDocument.Database;
Editor ed = Application.DocumentManager.
MdiActiveDocument.Editor;
using (Transaction tr = db.TransactionManager.StartTransaction())
{
doc.TransactionManager.EnableGraphicsFlush(true);
LayoutManager layoutMgr = LayoutManager.Current;
Layout layoutObj;
DBDictionary layoutDict;
ed.WriteMessage("Number of Layouts = {0}\n", layoutMgr.LayoutCount);
ed.WriteMessage("Current Layout = {0}\n", layoutMgr.CurrentLayout);
using (layoutDict = tr.GetObject(db.LayoutDictionaryId, OpenMode.ForRead) as DBDictionary)
{
foreach (DictionaryEntry layoutEntry in layoutDict)
{
using (layoutObj = tr.GetObject((ObjectId)(layoutEntry.Value), OpenMode.ForRead) as Layout)
{
// Set the CurrentLayout to the layout
// if it is not Modelspace
if (layoutObj.LayoutName == KeynameLay) layoutMgr.CurrentLayout = layoutObj.LayoutName;
ed.WriteMessage("Layout Name = {0}\n", layoutObj.LayoutName);
BlockTableRecord r = tr.GetObject(layoutObj.BlockTableRecordId, OpenMode.ForRead) as BlockTableRecord;
foreach (ObjectId obj in r)
{
DBObject dbobj = tr.GetObject(obj, OpenMode.ForRead);
Viewport vp = dbobj as Viewport;
if (vp != null)
{
ed.WriteMessage("\nnumber of Viewport = {0}", vp.Number);
// get the screen aspect ratio to calculate
// the height and width
double mScrRatio;
// width/height
mScrRatio = (vp.Width / vp.Height);
Point3d mMaxExt = x_Max;
Point3d mMinExt = x_Min;
Extents3d mExtents = new Extents3d();
mExtents.Set(mMinExt, mMaxExt);
// prepare Matrix for DCS to WCS transformation
Matrix3d matWCS2DCS;
matWCS2DCS = Matrix3d.PlaneToWorld(vp.ViewDirection);
matWCS2DCS = Matrix3d.Displacement(
vp.ViewTarget - Point3d.Origin) * matWCS2DCS;
matWCS2DCS = Matrix3d.Rotation(
-vp.TwistAngle, vp.ViewDirection,
vp.ViewTarget) * matWCS2DCS;
matWCS2DCS = matWCS2DCS.Inverse();
// tranform the extents to the DCS
// defined by the viewdir
mExtents.TransformBy(matWCS2DCS);
// width of the extents in current view
double mWidth;
mWidth = (mExtents.MaxPoint.X - mExtents.MinPoint.X);
// height of the extents in current view
double mHeight;
mHeight = (mExtents.MaxPoint.Y - mExtents.MinPoint.Y);
// get the view center point
Point2d mCentPt = new Point2d(
((mExtents.MaxPoint.X + mExtents.MinPoint.X) * 0.5),
((mExtents.MaxPoint.Y + mExtents.MinPoint.Y) * 0.5));
// check if the width 'fits' in current window,
// if not then get the new height as
// per the viewports aspect ratio
if (mWidth > (mHeight * mScrRatio))
mHeight = mWidth / mScrRatio;
// set the viewport parameters
if (vp.Number == 2)
{
vp.UpgradeOpen();
// set the view height -adjusted by 1 %
vp.ViewHeight = mHeight * 1.01;
// set the view center
vp.ViewCenter = mCentPt;
vp.Visible = true;
vp.On = true;
vp.UpdateDisplay();
ed.SwitchToModelSpace();
//ed.Command("_.ZOOM", "_SC");
//ed.Command("_.ZOOM", ".10X");
Application.SetSystemVariable("CVPORT", vp.Number);
}
if (vp.Number == 3)
{
vp.UpgradeOpen();
vp.ViewHeight = mHeight * 1.25;
//set the view center
vp.ViewCenter = mCentPt;
vp.Visible = true;
vp.On = true;
vp.UpdateDisplay();
ed.SwitchToModelSpace();
//ed.Command("_.ZOOM", "_SC");
//ed.Command("_.ZOOM", ".10X");
Application.SetSystemVariable("CVPORT", vp.Number);
}
tr.TransactionManager.QueueForGraphicsFlush(); doc.TransactionManager.FlushGraphics();
ed.UpdateScreen(); db.Regenmode = true;
}
}
}
}
}
tr.Commit();
}
}

}
}
Reply
08/14/2021 at 06:52 AM

---
