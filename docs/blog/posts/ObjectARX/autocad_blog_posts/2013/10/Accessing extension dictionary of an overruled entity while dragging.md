---
title: "Accessing extension dictionary of an overruled entity while dragging"
date: 2013-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
description: "When an entity that is being overruled is dragged, AutoCAD only creates a shallow copy of it. For this reason, the extension dictionary of the clon..."
author: Autodesk
---
# Accessing extension dictionary of an overruled entity while dragging

发布日期: 2013-10-01

原始链接: https://adndevblog.typepad.com/autocad/2013/10/accessing-extension-dictionary-of-an-overruled-entity-while-dragging.html

## 文章内容

By Balaji Ramamoorthy
When an entity that is being overruled is dragged, AutoCAD only creates a shallow copy of it. For this reason, the extension dictionary of the cloned entity is inaccessible from within the overrule class. One way to ensure that we get access to the extension dictionary is to drag the original entity and not its clone using the "TransformOverrule::CloneMeForDragging" and return false. Using this technique is not suggested as it is only meant for use with complex entities that can cause performance issues when cloned for dragging purposes. 
The workaround is to override the "TransformOverrule::CloneMeForDragging" and continue to return "true" and use the original entity which is a parameter to this method to access the extension dictionary.
Here is a sample code to demonstrate this.
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.GraphicsInterface;
  public class HelperClass
{
    const String _extDictName = "myExtDict";
    const String _XRecName = "myXRec";
    List<TypedValue> _data = new List<TypedValue>();
      public List<TypedValue> Data
    {
        get { return _data; }
    }
      private static HelperClass _instance;
    public String DictionaryName
    {
        get { return _extDictName; }
    }
      public String XRecordName
    {
        get { return _XRecName; }
    }
      protected HelperClass()
    {
    }
      public static HelperClass GetSingleton
    {
        get
        {
            if (_instance == null)
            {
                _instance = new HelperClass();
            }
            return _instance;
        }
    }
      public void CaptureXRecordData(DBObject obj)
    {
        Xrecord xRec = null;
        ObjectId id = obj.ExtensionDictionary;
          _data.Clear();
        if (! id.IsValid)
            return;
          Database db
        = Application.DocumentManager.MdiActiveDocument.Database;
        using (Transaction tr
            = db.TransactionManager.StartOpenCloseTransaction())
        {
            DBDictionary extDict = tr.GetObject(
                                    id,
                                    OpenMode.ForRead,
                                    false) as DBDictionary;
            if (extDict.Contains(DictionaryName))
            {
                ObjectId dictId = extDict.GetAt(DictionaryName);
                DBDictionary myDict = tr.GetObject(
                                    dictId,
                                    OpenMode.ForRead,
                                    false) as DBDictionary;
                xRec = tr.GetObject(
                                    myDict.GetAt(XRecordName),
                                    OpenMode.ForRead,
                                    false) as Xrecord;
                  if (xRec != null)
                {
                    ResultBuffer rb = xRec.Data;
                    if (rb != null)
                    {
                        TypedValue[] tvArray = rb.AsArray();
                        foreach (TypedValue tv in tvArray)
                        {
                            _data.Add(
                                    new TypedValue(
                                                   tv.TypeCode,
                                                   tv.Value
                                                  )
                                     );
                        }
                        rb.Dispose();
                    }
                }
            }
            tr.Commit();
        }
    }
}
  public class MyCommands
{
    static CMyDrawableOverrule lineOverrule = null;
    static CMyTransformeOverrule transformOverrule = null;
      [CommandMethod("OT")]
    public void OverruleTest()
    {
        Editor ed
        = Application.DocumentManager.MdiActiveDocument.Editor;
        PromptEntityResult per;
        per = ed.GetEntity("Pick a line to overrule");
        if(per.Status != PromptStatus.OK)
            return;
          Database db = HostApplicationServices.WorkingDatabase;
        using (Transaction tr
                    = db.TransactionManager.StartTransaction())
        {
            Entity ent = (Entity)tr.GetObject(
                            per.ObjectId, OpenMode.ForWrite);
              RegAppTable regTable = (RegAppTable)tr.GetObject(
                    db.RegAppTableId, OpenMode.ForRead, false);
              if (!regTable.Has("TEST"))
            {
                regTable.UpgradeOpen();
                RegAppTableRecord app = new RegAppTableRecord();
                app.Name = "TEST";
                regTable.Add(app);
                tr.AddNewlyCreatedDBObject(app, true);
            }
            ent.XData = new ResultBuffer(
                                new TypedValue(1001, "TEST"),
                                new TypedValue(1070, 100));
              string extDictName = "myExtDict";
            string xRecName = "myXRec";
              if (ent.ExtensionDictionary == ObjectId.Null)
            {
                ent.CreateExtensionDictionary();
            }
              DBDictionary xDict = tr.GetObject(
                            ent.ExtensionDictionary,
                            OpenMode.ForWrite) as DBDictionary;
              xDict.TreatElementsAsHard = true;
              if (!xDict.Contains(extDictName))
            {
                DBDictionary newDict = new DBDictionary();
                newDict.TreatElementsAsHard = true;
                  xDict.SetAt(extDictName, newDict);
                tr.AddNewlyCreatedDBObject(newDict, true);
                  Xrecord xRec = new Xrecord();
                  xRec.Data = new ResultBuffer(
                            new TypedValue((int)DxfCode.Text,
                                            "Autodesk"));
                  newDict.SetAt(xRecName, xRec);
                tr.AddNewlyCreatedDBObject(xRec, true);
            }
            tr.Commit();
        }
          if (lineOverrule == null)
        {
            transformOverrule = new CMyTransformeOverrule();
            Overrule.AddOverrule(
                RXObject.GetClass(typeof(Line)),
                transformOverrule,
                true);
              transformOverrule.SetXDataFilter("TEST");
              lineOverrule = new CMyDrawableOverrule();
            Overrule.AddOverrule(
                RXObject.GetClass(typeof(Line)),
                lineOverrule,
                true);
              lineOverrule.SetXDataFilter("TEST");
              Overrule.Overruling = true;
        }
          Application.DocumentManager.MdiActiveDocument.Editor.Regen();
    }
}
  public class CMyDrawableOverrule : DrawableOverrule
{
    [DllImport("acdb19.dll",
                CharSet = CharSet.Unicode,
                CallingConvention = CallingConvention.Cdecl,
                EntryPoint = "?fromAcDbTextStyle@@YA?AW4ErrorStatus@Acad@@AEAVAcGiTextStyle@@AEBVAcDbObjectId@@@Z")]
      private static extern Autodesk.AutoCAD.Runtime.ErrorStatus
        fromAcDbTextStyle(System.IntPtr style, ref ObjectId id);
      public override bool WorldDraw(Drawable drawable, WorldDraw wd)
    {
        base.WorldDraw(drawable, wd);
          Line line = drawable as Line;
        if (line == null)
            return true;
          using (LineSegment3d seg = new LineSegment3d(
                    line.StartPoint, line.EndPoint))
        {
            if (wd.IsDragging)
            {
                wd.SubEntityTraits.Color = 1;
                  // Retrieve the extension dictionary
                // values retrieved using helper class
                List<TypedValue> tvList
                       = HelperClass.GetSingleton.Data;
                  foreach (TypedValue tv in tvList)
                {
                    ObjectId textStyleId =
                    Application.DocumentManager.MdiActiveDocument.Database.Textstyle;
                      Autodesk.AutoCAD.GraphicsInterface.TextStyle iStyle
                    = new Autodesk.AutoCAD.GraphicsInterface.TextStyle();
                      if (fromAcDbTextStyle
                        (
                            iStyle.UnmanagedObject,
                            ref textStyleId
                        ) == Autodesk.AutoCAD.Runtime.ErrorStatus.OK)
                    {
                        wd.Geometry.Text(
                                        seg.MidPoint,
                                        line.Normal,
                                        Vector3d.XAxis,
                                        tv.Value.ToString(),
                                        true, iStyle);
                    }
                }
            }
            else
                wd.SubEntityTraits.Color = 2;
              wd.Geometry.Circle(seg.MidPoint,
                               seg.Length * 0.25,
                               line.Normal);
        }
        return true;
    }
}
  public class CMyTransformeOverrule : TransformOverrule
{
    public override bool CloneMeForDragging(Entity entity)
    {
        // Retrieve the extension dictionary from the original
        // entity. While dragging, the clone created is a
        //shallow clone and the extension dictionary isnt accessible
        HelperClass.GetSingleton.CaptureXRecordData(entity);
          // Permit cloning while dragging
        return true;
    }
}
Here is a screenshot that displays the content of the extension dictionary while the entity is being dragged

## 评论

**内容**: Dmitriy Zagorulkin said...
Hello!
Thanks for this code sample!
But I found here problem with use _PASTECLIP command. I paste in drawing several objects with different values in Extension Dictionary. In this case method CMyTransformeOverrule.CloneMeForDragging not work. And CMyDrawableOverrule.WorldDraw take old values from HelperClass.GetSingleton.Data:
https://screencast.autodesk.com/main/details/5ec69fc8-05e5-40b3-b3e3-0bafc2e8dfd3
My solution - add this code:
if (line.ExtensionDictionary != ObjectId.Null)
HelperClass.GetSingleton.CaptureXRecordData(line);
in method CMyDrawableOverrule.WorldDraw after this check:
if (line == null)
return true;
Reply
10/31/2014 at 01:08 AM

---
**内容**: Дмитрий Загорулькин said...
Hello!
Thanks for this code sample!
But I found here problem with use _PASTECLIP command. I paste in drawing several objects with different values in Extension Dictionary. In this case method CMyTransformeOverrule.CloneMeForDragging not work. And CMyDrawableOverrule.WorldDraw take old values from HelperClass.GetSingleton.Data:
https://screencast.autodesk.com/main/details/5ec69fc8-05e5-40b3-b3e3-0bafc2e8dfd3
My solution - add this code:
if (line.ExtensionDictionary != ObjectId.Null)
HelperClass.GetSingleton.CaptureXRecordData(line);
in method CMyDrawableOverrule.WorldDraw after this check:
if (line == null)
return true;
Reply
10/31/2014 at 01:13 AM

---
**内容**: Carl Golenberg said...
I've gotten this working - with a rather complex polyline object.
(for those wondering why theirs doesn't work at first, the objects must ultimatley be based off part of the passed enity - so it has a parametric relationship..) anyway, enacting the grip overrule kills this :/ why?
Reply
11/17/2014 at 04:06 AM

---
