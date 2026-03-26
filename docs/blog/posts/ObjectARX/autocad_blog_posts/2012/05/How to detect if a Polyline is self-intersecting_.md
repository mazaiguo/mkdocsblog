---
title: "How to detect if a Polyline is self-intersecting?"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - C#
  - Polyline
description: "Here is a request from one of our ADN developers:"
author: Autodesk
---
# How to detect if a Polyline is self-intersecting?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-detect-if-a-polyline-is-self-intersecting.html

## 文章内容

By Philippe Leefsma
Here is a request from one of our ADN developers:
I would like to detect if a certain polyline is self-intersecting and if so I would like to compute those intersection points. How to achieve this using the .Net API?
Solution
The following C# sample prompts the user for selecting an existing Polyline entity and then computes its self-intersecting points, if any:
[CommandMethod("SelfIntersectPline")]
public static void SelfIntersectPline()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions peo = new PromptEntityOptions(
        "\nSelect Polyline: ");
      peo.SetRejectMessage("\nMust be a Polyline...");
    peo.AddAllowedClass(typeof(Polyline), true);
      PromptEntityResult per = ed.GetEntity(peo);
      if (per.Status != PromptStatus.OK) return;
      using (Transaction Tx =
        db.TransactionManager.StartTransaction())
    {
        Polyline polyline = per.ObjectId.GetObject(
            OpenMode.ForRead)
                as Polyline;
          DBObjectCollection entities = new DBObjectCollection();
        polyline.Explode(entities);
          for (int i = 0; i < entities.Count; ++i)
        {
            for (int j = i + 1; j < entities.Count; ++j)
            {
                Curve curve1 = entities[i] as Curve;
                Curve curve2 = entities[j] as Curve;
                  Point3dCollection points = new Point3dCollection();
                curve1.IntersectWith(
                    curve2,
                    Intersect.OnBothOperands,
                    points,
                    IntPtr.Zero,
                    IntPtr.Zero);
                  foreach (Point3d point in points)
                {
                    // Make a check to skip the start/end points
                    // since they are connected vertices
                    if (point == curve1.StartPoint ||
                        point == curve1.EndPoint)
                    {
                        if (point == curve2.StartPoint ||
                            point == curve2.EndPoint)
                        {
                            // If two consecutive segments, then skip
                            if (j == i + 1)
                            {
                                continue;
                            }
                        }
                    }
                      ed.WriteMessage(
                        "\n - Intersection point: " +
                        point.ToString());
                }
            }
              // Need to be disposed explicitely
            // since entities are not DB resident
            entities[i].Dispose();
        }
    }
}

## 评论

**内容**: Cincir said...
Hi,
While inspecting namespaces i found an interesting class named CurveCurveIntersector3d in Geometry namespace. It provides functionality to find intersection of two curves. Even better it says if you give the same curve for both operands then you can get if the curve is self intersecting or not.
Reply
09/26/2012 at 06:40 PM

---
**内容**: aubelec said...
HI thanks for this but . i found a little error :
this the correct code :
If (point = curve1.StartPoint Or _
point = curve1.EndPoint) Then
If (point = curve2.StartPoint Or _
point = curve2.EndPoint) Then
Continue For
End If
End If
'// If two consecutive segments, then skip
If (j = i + 1) Then
Continue For
End If
Reply
01/03/2014 at 06:21 AM

---
**内容**: methodman said in reply to aubelec...
For c#:
if (point == pl1.StartPoint ||
point == pl1.EndPoint)
{
if (point == pl2.StartPoint ||
point == pl2.EndPoint)
{
continue;
}
}
// If two consecutive segments, then skip
if (j == i + 1)
{
continue;
}
Reply
11/25/2020 at 12:59 AM

---
