---
title: "Pattern generation of linetype with text on polyline entity"
date: 2018-10-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Polyline
  - Unicode
description: "Generating linetype with text on a Polyline entity could result in linetype pattern generated continuously across all vertices as below image. This..."
author: Autodesk
---
# Pattern generation of linetype with text on polyline entity

发布日期: 2018-10-01

原始链接: https://adndevblog.typepad.com/autocad/2018/10/pattern-generation-of-linetype-with-text-on-polyline-entity.html

## 文章内容

By Deepak Nadig
Generating linetype with text on a Polyline entity could result in linetype pattern generated continuously across all vertices as below image. This is because the linetype generation property of Polyline is ON              
Interactively this can be changed by issuing PEDIT command, setting Ltype gen as Off.
Command: PEDIT
Enter an option [Open/Join/Width/Edit vertex/Fit/Spline/Decurve/Ltype gen/Reverse/Undo]: L
Enter polyline linetype generation option [ON/OFF] <On>: OFF
    Via .NET API, Polyline entity has no property to change this. Thanks to Polyline2d.LinetypeGenerationOn property, we can convert the Polyline entity to Polyline2d and set this property false. Code sample shown below with the output image.  
  // code modified from the link 
//http://through-the-interface.typepad.com/through_the_interface/2008/01/creating-a-comp.html
[CommandMethod("CCL")]
public void CreateComplexLinetype()
{
    Document doc =
        Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
    Transaction tr =
        db.TransactionManager.StartTransaction();
    using (tr)
    {
        TextStyleTable tt =
            (TextStyleTable)tr.GetObject(
            db.TextStyleTableId,
            OpenMode.ForRead
            );
        LinetypeTable lt =
            (LinetypeTable)tr.GetObject(
            db.LinetypeTableId,
            OpenMode.ForWrite
            );
        LinetypeTableRecord ltr =
            new LinetypeTableRecord();

        ltr.Name = "COLD_WATER_SUPPLY";
        ltr.AsciiDescription =
            "Cold water supply ---- CW ---- CW ---- CW ----";
        ltr.PatternLength = 0.9;
        ltr.NumDashes = 3;
        // Dash #1
        ltr.SetDashLengthAt(0, 0.5);
        // Dash #2
        ltr.SetDashLengthAt(1,-0.2);
        ltr.SetShapeStyleAt(1, tt["Standard"]);
        ltr.SetShapeNumberAt(1, 0);
        ltr.SetShapeScaleAt(1, 0.1);
        ltr.SetTextAt(1, "CW");
        ltr.SetShapeRotationAt(1, 0);
        ltr.SetShapeOffsetAt(1, new Vector2d(0, -0.05));
        // Dash #3
        ltr.SetDashLengthAt(2, -0.2);

        // Add the new linetype to the linetype table
        ObjectId ltId = lt.Add(ltr);                
        tr.AddNewlyCreatedDBObject(ltr, true);
        // Create a test line with this linetype
        BlockTable bt =
            (BlockTable)tr.GetObject(
            db.BlockTableId,
            OpenMode.ForRead
            );
        BlockTableRecord btr =
            (BlockTableRecord)tr.GetObject(
            bt[BlockTableRecord.ModelSpace],
    OpenMode.ForWrite
    );

        using (Polyline acPoly = new Polyline())
        {
            acPoly.SetDatabaseDefaults(db);
            acPoly.AddVertexAt(0, new Point2d(0, 0), 0, 0, 0);
            acPoly.AddVertexAt(1, new Point2d(0, 2), 0, 0, 0);
            acPoly.AddVertexAt(2, new Point2d(2, 2), 0, 0, 0);
            acPoly.AddVertexAt(3, new Point2d(2, 0), 0, 0, 0);
            acPoly.Closed = true;
            btr.AppendEntity(acPoly);
            tr.AddNewlyCreatedDBObject(acPoly, false);
            Polyline2d poly2 = acPoly.ConvertTo(true);
            poly2.LinetypeGenerationOn = false;
            poly2.LinetypeId = ltId;
            tr.AddNewlyCreatedDBObject(poly2, true);
        }
        tr.Commit();
    }
}
Result :

## 评论

**内容**: Salahddin said...
Hi do you have training center or learning center autocad bahrain
Reply
07/15/2019 at 05:06 AM

---
**内容**: Autocad Bahrain said...
Hi do you have training center or learning center autocad bahrain
Reply
07/15/2019 at 05:06 AM

---
