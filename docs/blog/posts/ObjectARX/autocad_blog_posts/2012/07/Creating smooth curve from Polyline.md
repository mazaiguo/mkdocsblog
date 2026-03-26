---
title: "Creating smooth curve from Polyline"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - Polyline
description: "“Polyline2d” entity has a function which can create a smooth curve consisting of pairs of arcs joining each pair of vertices. So to fit a ployline,..."
author: Autodesk
---
# Creating smooth curve from Polyline

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/creating-smooth-curve-from-polyline.html

## 文章内容

By Virupaksha Aithal
“Polyline2d” entity has a function which can create a smooth curve consisting of pairs of arcs joining each pair of vertices. So to fit a ployline, below code first converts the ployline to Polyline2d uses the “CurveFit” API and then creates a new ployline from the fitted Polyline2d.
[CommandMethod("TestFitCurve")]
public void TestFitCurve()
{
   Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
          new PromptEntityOptions("\nSelect a polyline");
    options.SetRejectMessage("\nSelect polyline ");
    options.AddAllowedClass(
       typeof(Autodesk.AutoCAD.DatabaseServices.Polyline), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      ObjectId ModelSpaceId =
            SymbolUtilityServices.GetBlockModelSpaceId(db);
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        Autodesk.AutoCAD.DatabaseServices.Polyline plineFit =
            new Autodesk.AutoCAD.DatabaseServices.Polyline();
        Autodesk.AutoCAD.DatabaseServices.Polyline pline =
            (Autodesk.AutoCAD.DatabaseServices.Polyline)Tx.GetObject(
                             acSSPrompt.ObjectId, OpenMode.ForRead);
        {
              Polyline2d poly2d = pline.ConvertTo(false);
            poly2d.CurveFit();
            plineFit.ConvertFrom(poly2d, false);
            poly2d.Dispose();
              BlockTableRecord record = Tx.GetObject(ModelSpaceId,
                              OpenMode.ForWrite) as BlockTableRecord;
            plineFit.ColorIndex = 1;//red
            record.AppendEntity(plineFit);
            Tx.AddNewlyCreatedDBObject(plineFit, true);
            Tx.Commit();
        }
      }
}

