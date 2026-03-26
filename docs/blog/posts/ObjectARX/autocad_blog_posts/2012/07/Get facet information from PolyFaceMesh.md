---
title: "Get facet information from PolyFaceMesh"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - C++
  - Database
description: "This is the .NET version of this post"
author: Autodesk
---
# Get facet information from PolyFaceMesh

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/get-facet-information-from-polyfacemesh.html

## 文章内容

By Adam Nagy
This is the .NET version of this post
Usually it is quite easy to migrate an ARX code to .NET, since it is just a thin wrapper on top of the ARX API. You need to omit the AcDb prefix from the database class types, use foreach instead of a function that creates an iterator, use transactions, and you have most of the below code ready :)
[CommandMethod("PolyTest_PolyFace")]
public void PolyTest_PolyFace()
{
  Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
    PromptEntityResult per = ed.GetEntity("Select a poly face mesh");
  if (per.Status != PromptStatus.OK)
    return;
    int color = 0;
    Database db = ed.Document.Database;
  using (Transaction tr = db.TransactionManager.StartTransaction())
  {
    BlockTable bt =
      (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);

    BlockTableRecord ms =
      (BlockTableRecord)tr.GetObject(
        bt[BlockTableRecord.ModelSpace],
        OpenMode.ForWrite); 
      PolyFaceMesh pfm =
      (PolyFaceMesh)tr.GetObject(per.ObjectId, OpenMode.ForRead);
      Point3dCollection vertices = new Point3dCollection();
      foreach (ObjectId id in pfm)
    {
      DBObject obj = tr.GetObject(id, OpenMode.ForRead);
        if (obj is PolyFaceMeshVertex)
      {
        PolyFaceMeshVertex vertex = (PolyFaceMeshVertex)obj;
        vertices.Add(vertex.Position); 
      }
      else if (obj is FaceRecord)
      {
        FaceRecord face = (FaceRecord)obj;
          Point3dCollection pts = new Point3dCollection();
          for (short i = 0; i < 4; i++)
        {
          short index = face.GetVertexAt(i);
            if (index != 0)
            pts.Add(vertices[Math.Abs(index) - 1]);
        }
          // If there are 4 points then we draw crosses
        // (could also be 3)
        if (pts.Count == 4)
        {
          for (int j = 0; j < 2; j++)
          {
            Line line = new Line(pts[j], pts[j + 2]);
            line.ColorIndex = color;
              ms.AppendEntity(line);
            tr.AddNewlyCreatedDBObject(line, true);
          }
        }
          color = (color + 1) % 7;
      }
    }
      tr.Commit();
  }
}

## 评论

**内容**: Emanuel Ceballos said...
Excellent post, it helped a lot. Thanks very much.
Reply
04/09/2013 at 12:06 PM

---
