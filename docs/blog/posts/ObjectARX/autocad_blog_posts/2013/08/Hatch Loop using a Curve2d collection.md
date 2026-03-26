---
title: "Hatch Loop using a Curve2d collection"
date: 2013-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Database
  - Hatch
description: "To create a hatch, the loop information can be provided by providing the ObjectId collection of the database-resident entities that define the hatc..."
author: Autodesk
---
# Hatch Loop using a Curve2d collection

发布日期: 2013-08-01

原始链接: https://adndevblog.typepad.com/autocad/2013/08/hatch-loop-using-a-curve2d-collection.html

## 文章内容

By Balaji Ramamoorthy
To create a hatch, the loop information can be provided by providing the ObjectId collection of the database-resident entities that define the hatch loop. For this please refer to this post : Create Hatch Objects using Trace Boundaries using .NET. The other way is to only rely on the geometry without having the entities added to the database.
Here is a sample code to demonstrate the second approach that creates the hatch loop only using the boundary geometry. To have two loops created for the same hatch, the sample code prompts for two internal points to be picked.
[CommandMethod("TH")]
public void TestHatch()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptPointResult ppr1
                 = ed.GetPoint("Pick an internal point 1 : ");
    if (ppr1.Status != PromptStatus.OK)
        return;
    Point3d internalPt1 = ppr1.Value;
    DBObjectCollection dbo1
                        = ed.TraceBoundary(internalPt1, true);
    if (dbo1 == null)
        return;
      PromptPointResult ppr2
                  = ed.GetPoint("Pick an internal point 2 : ");
    if (ppr2.Status != PromptStatus.OK)
        return;
    Point3d internalPt2 = ppr2.Value;
    DBObjectCollection dbo2
                        = ed.TraceBoundary(internalPt2, true);
    if (dbo2 == null)
        return;
      try
    {
        using (Transaction tr
                   = db.TransactionManager.StartTransaction())
        {
            BlockTable bt = tr.GetObject(
                                            db.BlockTableId,
                                            OpenMode.ForWrite
                                        ) as BlockTable;
            BlockTableRecord btr = tr.GetObject
                            (
                               bt[BlockTableRecord.ModelSpace],
                               OpenMode.ForWrite
                            ) as BlockTableRecord;
              Curve2dCollection edgePtrs1 = new Curve2dCollection();
            IntegerCollection edgeTypes1 = new IntegerCollection();
            foreach (DBObject obj in dbo1)
            {
                Entity entity = obj as Entity;
                Autodesk.AutoCAD.DatabaseServices.Polyline pline
                = entity as Autodesk.AutoCAD.DatabaseServices.Polyline;
                if (pline != null)
                {
                    GetEdgeInformation( pline,
                                        ref edgePtrs1,
                                        ref  edgeTypes1);
                }
            }
              Curve2dCollection edgePtrs2 = new Curve2dCollection();
            IntegerCollection edgeTypes2 = new IntegerCollection();
            foreach (DBObject obj in dbo2)
            {
                Entity entity = obj as Entity;
                Autodesk.AutoCAD.DatabaseServices.Polyline pline
                = entity as Autodesk.AutoCAD.DatabaseServices.Polyline;
                if (pline != null)
                {
                    GetEdgeInformation( pline,
                                        ref edgePtrs2,
                                        ref  edgeTypes2);
                }
            }
              Hatch hatchObj = new Hatch();
            hatchObj.SetDatabaseDefaults();
              Vector3d normal = new Vector3d(0.0, 0.0, 1.0);
            hatchObj.HatchObjectType = HatchObjectType.HatchObject;
            hatchObj.Color
                    = Autodesk.AutoCAD.Colors.Color.FromColor
                                    (System.Drawing.Color.Blue);
              hatchObj.Normal = normal;
            hatchObj.Elevation = 0.0;
            hatchObj.PatternScale = 0.5;
            hatchObj.SetHatchPattern
                                (
                                    HatchPatternType.PreDefined,
                                    "ZIGZAG"
                                );
              btr.AppendEntity(hatchObj);
            tr.AddNewlyCreatedDBObject(hatchObj, true);
              hatchObj.Associative = true;
            hatchObj.AppendLoop(
                                (int)HatchLoopTypes.Default,
                                edgePtrs1,
                                edgeTypes1
                                );
            hatchObj.AppendLoop(
                                (int)HatchLoopTypes.Default,
                                edgePtrs2,
                                edgeTypes2
                               );
              hatchObj.EvaluateHatch(true);
              tr.Commit();
        }
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.ToString() + Environment.NewLine);
    }
}
  public void GetEdgeInformation
        (
            Autodesk.AutoCAD.DatabaseServices.Polyline pline,
            ref Curve2dCollection plCurves,
            ref IntegerCollection edgeTypes
        )
{
    int segCount = pline.NumberOfVertices;
    for (int cnt = 0; cnt < segCount; cnt++)
    {
        SegmentType type = pline.GetSegmentType(cnt);
          switch (type)
        {
            case SegmentType.Arc:
                CircularArc2d arc2d = pline.GetArcSegment2dAt(cnt);
                plCurves.Add(arc2d);
                edgeTypes.Add((int)Enum.Parse(typeof(HatchEdgeType),
                        HatchEdgeType.CircularArc.ToString()));
                break;
              case SegmentType.Line:
                LineSegment2d line2d = pline.GetLineSegment2dAt(cnt);
                plCurves.Add(line2d);
                edgeTypes.Add((int)Enum.Parse(typeof(HatchEdgeType),
                               HatchEdgeType.Line.ToString()));
                break;
              case SegmentType.Coincident:
                break;
            case SegmentType.Empty:
                break;
            case SegmentType.Point:
                break;
        }
    }
}
Here is a sample output for two loops that were appended and a sample drawing for you to try :
Download Test

## 评论

**内容**: Matthias Beyer said...
Hi Balaji,
I've just tried your sample. Works great in AutoCAD 2015/2017. But the created hatch isn't associative.
Is it possible to create associative hatches in the current releases of AutoCAD, too?
Reply
10/17/2016 at 05:06 AM

---
**内容**: Jacob Lewis said in reply to Matthias Beyer...
You can, but not by using the AppendLoop overload that takes a Curve2dCollection.
If you used this one instead, and passed in the ObjectId of the Polyline, AutoCAD could then maintain the association.
public void AppendLoop(HatchLoopTypes loopType, ObjectIdCollection dbObjIds);
Reply
11/03/2016 at 10:38 PM

---
**内容**: Eve De Maistre said...
An auto cat and all joyful end is placed for the fix of the joy for the items. The manner of the ai video editor are rushed for the team. The matter spilt for the terms for the width for the top the turns for humans.
Reply
07/05/2023 at 03:50 PM

---
