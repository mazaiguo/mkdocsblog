---
title: "How to use CreateLoftedSolid"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
  - Solid
description: "I have two rectanlges and I would like to create a lofted solid from them. I tried the below code and played with the input parameters but it just ..."
author: Autodesk
---
# How to use CreateLoftedSolid

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/how-to-use-createloftedsolid.html

## 文章内容

By Adam Nagy
I have two rectanlges and I would like to create a lofted solid from them. I tried the below code and played with the input parameters but it just does not seem to work. Could you provide a sample?
...
Dim vol As New DatabaseServices.Solid3d()
vol.CreateLoftedSolid(New DatabaseServices.Entity() {e1, e2},
                      Nothing, Nothing, Nothing)
...
Solution
The only parameter for CreateLoftedSolid that can be null/Nothing is the pathCurve parameter.
Knowing that you can modify the code like this.
Note: please pick the entities in this order: rectangle 1, rectangle 2, path.
Imports acApp = Autodesk.AutoCAD.ApplicationServices.Application
Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.EditorInput
Imports Autodesk.AutoCAD.Runtime
  Public Class Commands
  <CommandMethod("CreateLoft")> _
  Public Sub CreateLoft()
    Dim ed As Editor = acApp.DocumentManager.MdiActiveDocument.Editor
    Dim db As Database = HostApplicationServices.WorkingDatabase
    Dim psr As PromptSelectionResult = ed.GetSelection()
      If psr.Status <> PromptStatus.OK Or psr.Value.Count <> 3 Then
      Return
    End If
      Using tr As Transaction =
      db.TransactionManager.StartTransaction()
        Dim ent1 As Entity =
        tr.GetObject(psr.Value(0).ObjectId, OpenMode.ForRead)
      Dim ent2 As Entity =
        tr.GetObject(psr.Value(1).ObjectId, OpenMode.ForRead)
      Dim path As Entity =
        tr.GetObject(psr.Value(2).ObjectId, OpenMode.ForRead)
        Dim sld As New Solid3d
      Dim options As New LoftOptions
      ' In case of this specific drawing passing in Nothing as
      ' path would give similar results
      sld.CreateLoftedSolid(New Entity() {ent1, ent2},
                            New Entity() {}, path, options)
        Dim bt As BlockTable =
        tr.GetObject(db.BlockTableId, OpenMode.ForRead)
        Dim ms As BlockTableRecord =
        tr.GetObject(bt(BlockTableRecord.ModelSpace),
                     OpenMode.ForWrite)
        ms.AppendEntity(sld)
      tr.AddNewlyCreatedDBObject(sld, True)
        tr.Commit()
    End Using
  End Sub
End Class
I tested the above code with the following drawing: Download Rectangles

## 评论

**内容**: Daniel Vink said...
Adam,
I've been trying to create a solid loft from several cross profiles and no path in .NET for a while now. Both the AutoCAD command with solid and LoftedSurface .net method work, so I know it's possible. Generating a path is not possible, and selecting an approximate path gives a "The guide is not G1 between first and last sections." error.
Would it be possible for you to share the 'specific drawing' mentioned in the code comments? It might help in figuring out the G1 error.
Reply
05/06/2013 at 02:34 AM

---
**内容**: Adam Nagy said...
Hi Daniel,
I've added a drawing to the article that the code seems to work with fine.
Cheers,
Adam
Reply
05/10/2013 at 04:08 AM

---
**内容**: Sergey Makarov said...
Hi Adam!
When I create a Solid3d using the CreateLoftedSolid(...) method I got a significant time delay. Array of 300 polylines with elevation and rotation takes 10 second to Solid3d creation. Help me please to make this process faster.
// Modal Command with localized name
[CommandMethod("MyGroup", "MyTest", "MyTestLocal", CommandFlags.Modal)]
public void MyTest() // This method can have any name
{
Database db = Application.DocumentManager.MdiActiveDocument.Database;
using (Transaction ts = db.TransactionManager.StartTransaction())
{
// Open the Block table for read
BlockTable acBlkTbl;
acBlkTbl = ts.GetObject(db.BlockTableId,
OpenMode.ForRead) as BlockTable;
// Open the Block table record Model space for write
BlockTableRecord acBlkTblRec;
acBlkTblRec = ts.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
OpenMode.ForWrite) as BlockTableRecord;

Entity[] pls = new Entity[300];
for (int i = 0; i < 300; i++)
{
Polyline pl = new Polyline();
pl.AddVertexAt(0, new Point2d(0.0, 0.0), 0.0, 0.0, 0.0);
pl.AddVertexAt(0, new Point2d(0.0, 0.5), 0.0, 0.0, 0.0);
pl.AddVertexAt(0, new Point2d(0.2, 1.0), 0.0, 0.0, 0.0);
pl.AddVertexAt(0, new Point2d(1.0, 1.0), 0.0, 0.0, 0.0);
pl.AddVertexAt(0, new Point2d(1.0, 0.0), 0.0, 0.0, 0.0);
pl.Closed = true;
pl.Elevation = i * 2.0;
pl.TransformBy(Matrix3d.Rotation(i, Vector3d.ZAxis, Point3d.Origin));
pls[i] = pl;
}
LoftOptionsBuilder loftOptionsBuilder = new LoftOptionsBuilder()
{
Ruled = true
};
Solid3d solid = new Solid3d();
solid.CreateLoftedSolid(pls, new Entity[] { }, null, loftOptionsBuilder.ToLoftOptions());
acBlkTblRec.AppendEntity(solid);
ts.AddNewlyCreatedDBObject(solid, true);
ts.Commit();
}
}
Reply
08/18/2022 at 01:06 AM

---
**内容**: Adam Nagy said in reply to Sergey Makarov...
I don't think I could offer anything more beyond what's discussed in this very comprehensive blog post: https://modthemachine.typepad.com/my_weblog/2015/09/improving-your-programs-performance.html
Reply
08/18/2022 at 02:53 AM

---
