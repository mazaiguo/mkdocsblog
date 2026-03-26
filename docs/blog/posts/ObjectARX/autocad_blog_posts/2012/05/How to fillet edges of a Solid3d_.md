---
title: "How to fillet edges of a Solid3d?"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - C#
  - Database
  - Solid
description: "The following C# sample demonstrates the use of "Solid3d.FilletEdges" method:"
author: Autodesk
---
# How to fillet edges of a Solid3d?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-fillet-edges-of-a-solid3d.html

## 文章内容

By Philippe Leefsma
  The following C# sample demonstrates the use of "Solid3d.FilletEdges" method:
[CommandMethod("TestFillet")]
public void TestFillet()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        BlockTableRecord blkRec =
            Tx.GetObject(db.CurrentSpaceId, OpenMode.ForWrite, false)
                as BlockTableRecord;
          Solid3d solid = new Solid3d();
          solid.CreateBox(500.0, 400.0, 1000.0);
          blkRec.AppendEntity(solid);
        Tx.AddNewlyCreatedDBObject(solid, true);
          ObjectId[] ids = new ObjectId[] { solid.ObjectId };
          SubentityId subentId = new SubentityId(
            SubentityType.Null, IntPtr.Zero);
          FullSubentityPath path = new FullSubentityPath(
            ids, subentId);
          List<SubentityId> subentIds = new List<SubentityId>();
        DoubleCollection radii = new DoubleCollection();
        DoubleCollection startSetback = new DoubleCollection();
        DoubleCollection endSetback = new DoubleCollection();
          using (Autodesk.AutoCAD.BoundaryRepresentation.Brep brep =
            new Autodesk.AutoCAD.BoundaryRepresentation.Brep(path))
        {
            foreach (Autodesk.AutoCAD.BoundaryRepresentation.Edge
                edge in brep.Edges)
            {
                subentIds.Add(edge.SubentityPath.SubentId);
                radii.Add(10.0);
                  // Setback fillets. Defines a setback distance
                // from a vertex at which the fillets start to blend
                startSetback.Add(5.0);
                endSetback.Add(5.0);
            }
        }
          solid.FilletEdges(
            subentIds.ToArray(),
            radii,
            startSetback,
            endSetback);
          Tx.Commit();
    }
}

## 评论

**内容**: George Csikos said...
Philippe can this be done without actually appending the entity to the drawing first? I want to create an in-memory 3D solid that is then passed into the HLR (hidden line removal tool in the utilities of the ObjectARX API) so we can get 2D projections of the filleted solid. I do not need a DWG resident instance of the solid. It could be added it and erased it but that adds to the undo list unnecessarily.
Reply
05/21/2014 at 04:07 PM

---
**内容**: Philippe Leefsma said in reply to George Csikos...
Hi George, I doubt it's possible: the solid needs to be database resident in order to have its subentity path affected.
You can turn off the undo mechanism using Database.DisableUndoRecording as a workaround.
Hope that helps,
Philippe.
Reply
05/26/2014 at 01:23 AM

---
