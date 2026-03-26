---
title: "Using Curve.Extend"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "In AutoCAD 2013, the "Curve.Extend" method does not extend by the right amount when used on lines. It works as expected on Arcs and elliptical arcs..."
author: Autodesk
---
# Using Curve.Extend

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/using-curveextend.html

## 文章内容

By Balaji Ramamoorthy
In AutoCAD 2013, the "Curve.Extend" method does not extend by the right amount when used on lines. It works as expected on Arcs and elliptical arcs. While this will most likely be addressed in the next release of AutoCAD, the simple workaround for now is to extend lines by calculating the start/end point and rely on Curve.Extend for other curves such as arcs and elliptical arcs.
Here is a sample code to extend the curve at its end by 10% of the curve length :
[CommandMethod("xt")]
public void XtendMethod()
{
    Document doc
                = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
    Database db = doc.Database;
      try
    {
        PromptEntityOptions peo
                = new PromptEntityOptions("\nSelect a Curve");
        peo.SetRejectMessage("\nSelected entity must be a Curve.");
        peo.AddAllowedClass(typeof(Curve), false);
          PromptEntityResult per = ed.GetEntity(peo);
        if (per.Status != PromptStatus.OK)
            return;
          using (Transaction tr
                    = db.TransactionManager.StartTransaction())
        {
            Curve curve
                = tr.GetObject    (
                                    per.ObjectId,
                                    OpenMode.ForWrite
                                ) as Curve;
              Line line = curve as Line;
              if (line != null)
            {
                double dist = line.Length * 0.1;
                Vector3d dir
                    = (line.EndPoint - line.StartPoint).GetNormal();
                line.EndPoint += dir * dist;
            }
            else
            {
                double ep = curve.EndParam;
                ep = ep * 1.1;
                curve.Extend(ep);
            }
            tr.Commit();
        }
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.Message);
    }
}

