---
title: "Set origin while creating a hatch using .NET"
date: 2018-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Hatch
description: "We had an issue raised by a customer regarding setting origin(image) during hatch creation."
author: Autodesk
---
# Set origin while creating a hatch using .NET

发布日期: 2018-05-01

原始链接: https://adndevblog.typepad.com/autocad/2018/05/set-origin-while-creating-a-hatch-using-net.html

## 文章内容

By Deepak Nadig
We had an issue raised by a customer regarding setting origin(image) during hatch creation.
It was found that origin of hatch has to be set in a transaction other than the one in which it is created for it to work correctly.
Below code can be used for testing : 
[CommandMethod("setOrginHatch")]
public void setOriginHatch()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;

    ObjectId mHatchId;
    Hatch mHatch = new Hatch();
    using (Transaction tr1 = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = (BlockTable)tr1.GetObject(doc.Database.BlockTableId, OpenMode.ForRead);
        BlockTableRecord btr = (BlockTableRecord)tr1.GetObject(db.CurrentSpaceId, OpenMode.ForWrite);

        Point2d pt = new Point2d(0, 0);
        Polyline mPolyline = new Polyline(4);
        mPolyline.AddVertexAt(0, pt, 0.0, -1.0, -1.0);
        mPolyline.Normal = Vector3d.ZAxis;
        mPolyline.AddVertexAt(1, new Point2d(pt.X + 10, pt.Y), 0.0, -1.0, -1.0);
        mPolyline.AddVertexAt(2, new Point2d(pt.X + 10, pt.Y + 5), 0.0, -1.0, -1.0);
        mPolyline.AddVertexAt(3, new Point2d(pt.X, pt.Y + 5), 0.0, -1.0, -1.0);
        mPolyline.Closed = true;

        ObjectId mPlineId;
        mPlineId = btr.AppendEntity(mPolyline);
        tr1.AddNewlyCreatedDBObject(mPolyline, true);

        ObjectIdCollection ObjIds = new ObjectIdCollection();
        ObjIds.Add(mPlineId);

        Vector3d normal = new Vector3d(0.0, 0.0, 1.0);
        mHatch.Normal = normal;
        mHatch.Elevation = 0.0;
        mHatch.PatternScale = 2.0;
        mHatch.SetHatchPattern(HatchPatternType.PreDefined, "NET");
        mHatch.ColorIndex = 1;
        mHatch.PatternAngle = 2;

        //trying to set origin here does not work 
        //Point2d setOrigin = new Point2d(6.698, 2.78);
        //mHatch.Origin = setOrigin;

        btr.AppendEntity(mHatch);
        tr1.AddNewlyCreatedDBObject(mHatch, true);

        mHatch.Associative = true;
        mHatch.AppendLoop(HatchLoopTypes.Outermost, ObjIds);
        mHatch.EvaluateHatch(true);

        //get the ObjectId of hatch 
        mHatchId = mHatch.ObjectId;

        tr1.Commit();
    }
    //to set the origin use another transaction 
    using (Transaction tr2 = doc.TransactionManager.StartTransaction())
    {
        Entity ent = (Entity)tr2.GetObject(mHatchId, OpenMode.ForWrite);
        if (ent != null)
        {
            Hatch nHatch = ent as Hatch;
            String hatchName = nHatch.PatternName;
            Point2d setOrigin = new Point2d(6.698, 2.78);
            nHatch.Origin = setOrigin;
            nHatch.SetHatchPattern(HatchPatternType.PreDefined, hatchName);
            nHatch.EvaluateHatch(true);
            nHatch.Draw();
        }
        tr2.Commit();
    }
}

## 评论

**内容**: Bright Computer Education said...
Thanks, admin for clearing doubts. Appreciate your prompt reply.
Reply
07/20/2018 at 06:55 AM

---
**内容**: Jose G said...
Just ran into this. using 2025 (.net 8) this bug is still not fixed. fyi
Reply
05/19/2024 at 08:26 PM

---
