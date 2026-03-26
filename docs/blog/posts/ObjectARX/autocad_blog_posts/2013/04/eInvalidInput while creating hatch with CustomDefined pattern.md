---
title: "eInvalidInput while creating hatch with CustomDefined pattern"
date: 2013-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Hatch
description: "If the "SetHatchPattern" method throws an "eInvalidInput" exception while creating a hatch using a CustomDefined hatch pattern, here are few points..."
author: Autodesk
---
# eInvalidInput while creating hatch with CustomDefined pattern

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/einvalidinput-while-creating-hatch-with-customdefined-pattern.html

## 文章内容

By Balaji Ramamoorthy
If the "SetHatchPattern" method throws an "eInvalidInput" exception while creating a hatch using a CustomDefined hatch pattern, here are few points to check.
1) Is the pattern file that defines the custom hatch pattern named correctly ? The name of the hatch pattern and the pat file name should be the same.
2) Is the folder in which the pat file is placed, added to the AutoCAD support path ?
3) Is the line breaks in the pat file ok ? The easiest way to ensure that it is ok is to take an existing custom hatch pattern file and change the definitions to suit your requirements. AutoCAD is sensitive to line breaks in the pat file and "eInvalidInput" exception because of this can be hard to spot. You can find several online resources such as this to download a custom hatch pattern file.
Here is a sample code to try out the custom hatch pattern :
Document doc = Application.DocumentManager.MdiActiveDocument;
Database db = doc.Database;
Editor ed = doc.Editor;
  PromptResult prHatchPatternName
        = ed.GetString("\nEnter custom hatch pattern name : ");
if (prHatchPatternName.Status != PromptStatus.OK)
    return;
string patName = prHatchPatternName.StringResult;
  PromptPointResult ppr = ed.GetPoint("Pick insertion point: ");
if (ppr.Status != PromptStatus.OK)
    return;
Point3d insertionPt = ppr.Value;
  try
{
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt
            = tr.GetObject(db.BlockTableId, OpenMode.ForWrite) as BlockTable;
          BlockTableRecord btr
            = tr.GetObject( bt[BlockTableRecord.ModelSpace],
                            OpenMode.ForWrite
                          ) as BlockTableRecord;
          Point2d pt = new Point2d(insertionPt.X, insertionPt.Y);
          Polyline plBox;
        plBox = new Polyline(4);
        plBox.Normal = Vector3d.ZAxis;
        plBox.AddVertexAt(0, pt, 0.0, -1.0, -1.0);
        plBox.AddVertexAt(1, new Point2d(pt.X + 10, pt.Y), 0.0, -1.0, -1.0);
        plBox.AddVertexAt(2, new Point2d(pt.X + 10, pt.Y + 5), 0.0, -1.0, -1.0);
        plBox.AddVertexAt(3, new Point2d(pt.X, pt.Y + 5), 0.0, -1.0, -1.0);
        plBox.Closed = true;
          ObjectId pLineId;
        pLineId = btr.AppendEntity(plBox);
        tr.AddNewlyCreatedDBObject(plBox, true);
          ObjectIdCollection ObjIds = new ObjectIdCollection();
        ObjIds.Add(pLineId);
          Hatch hatchObj = new Hatch();
        hatchObj.SetDatabaseDefaults();
          Vector3d normal = new Vector3d(0.0, 0.0, 1.0);
        hatchObj.HatchObjectType = HatchObjectType.HatchObject;
        hatchObj.Color
                = Autodesk.AutoCAD.Colors.Color.FromColor(System.Drawing.Color.Blue);
        hatchObj.Normal = normal;
        hatchObj.Elevation = 0.0;
          hatchObj.SetHatchPattern(HatchPatternType.CustomDefined, patName);
          btr.AppendEntity(hatchObj);
        tr.AddNewlyCreatedDBObject(hatchObj, true);
        hatchObj.Associative = true;
        hatchObj.AppendLoop((int)HatchLoopTypes.Default, ObjIds);
        hatchObj.EvaluateHatch(true);
          tr.Commit();
    }
}
catch (System.Exception ex)
{
    ed.WriteMessage(ex.ToString() + Environment.NewLine);
}

## 评论

**内容**: ko0ls said...
i choose patName="SOLID".But error not dissapear
Reply
03/29/2014 at 09:12 AM

---
**内容**: Balaji said...
Hello,
"Solid" is one of the predefined hatch patterns.
You will need : SetHatchPattern(HatchPatternType.PreDefined, "SOLID")
Please look for "SetHatchPattern" in this blog or in the discussion forums and you will find examples.
Regards,
Balaji
Reply
04/01/2014 at 05:33 PM

---
**内容**: Craig said...
Thanks Balaji,
It was line breaks for me.
Craig
Reply
03/02/2015 at 08:36 AM

---
