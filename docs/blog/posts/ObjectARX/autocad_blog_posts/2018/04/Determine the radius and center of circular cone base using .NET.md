---
title: "Determine the radius and center of circular cone base using .NET"
date: 2018-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Database
description: "We can make use of Brep support to determine the radius and center of a cone( properties shown up in  the image image) with circular base."
author: Autodesk
---
# Determine the radius and center of circular cone base using .NET

发布日期: 2018-04-01

原始链接: https://adndevblog.typepad.com/autocad/2018/04/determine-the-radius-and-center-of-circular-cone-base-using-net-.html

## 文章内容

By Deepak Nadig
We can make use of Brep support to determine the radius and center of a cone( properties shown up in  the image image) with circular base.    
 Below .NET code snippet can be used : 
[CommandMethod("circularConeRadiusAndCenter")]
public void circularConeRadiusAndCenter()
{
    Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;

    // Ask the user to select a solid
    PromptEntityOptions peo = new PromptEntityOptions("Select a 3D solid");
    peo.SetRejectMessage("\nA 3D solid must be selected.");
    peo.AddAllowedClass(typeof(Solid3d), true);
    PromptEntityResult per = ed.GetEntity(peo);

    if (per.Status != PromptStatus.OK)
        return;

    Transaction tr = db.TransactionManager.StartTransaction();
    using (tr)
    {
        Solid3d sol = tr.GetObject(per.ObjectId, OpenMode.ForRead) as Solid3d;
        using (Brep brep = new Brep(sol))
        {
            //check if base is a circular. If yes, then determine the center and radius
            foreach (Complex cmp in brep.Complexes)
            {
                int edgeCnt = 1;
                foreach (Edge edge in brep.Edges)
                {
                    ed.WriteMessage("\n --> Edge : {0}", edgeCnt++);
                    Curve3d edgeCurve = edge.Curve;
                    if (edgeCurve is ExternalCurve3d)
                    {
                        ed.WriteMessage("\n Edge type : {0}", "ExternalCurve3d");
                        ExternalCurve3d extCurve3d = edgeCurve as ExternalCurve3d;
                        Curve3d nativeCurve = extCurve3d.NativeCurve;
                        if (nativeCurve is CircularArc3d)
                        {
                            ed.WriteMessage("\n Native curve type : {0}", "CircularArc3d");
                            CircularArc3d circArc3d = nativeCurve as CircularArc3d;
                            ed.WriteMessage("\n radius is " + circArc3d.Radius.ToString());                                    
                            ed.WriteMessage("\n center is " + PointToStr(circArc3d.Center));
                        }
                        else
                        {
                            ed.WriteMessage("\n Native curve type of cone is not Circular");
                            return;
                        }

                    }

                }
            }
        }
    }
}
private string PointToStr(Point3d point)
{
    return "[" +
        point.X.ToString("F2") + ", " +
        point.Y.ToString("F2") + ", " +
        point.Z.ToString("F2")
        + "]";
}

