---
title: "Reclaiming memory of erased objects"
date: 2012-04-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Database
  - ObjectARX
description: "In AutoCAD, when an object is erased, it is marked as "erased" and the memory is not reclaimed until AutoCAD is closed. It is sometimes necessary t..."
author: Autodesk
---
# Reclaiming memory of erased objects

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/reclaiming-memory-of-erased-objects.html

## 文章内容

By Balaji Ramamoorthy
In AutoCAD, when an object is erased, it is marked as "erased" and the memory is not reclaimed until AutoCAD is closed. It is sometimes necessary to reclaim the memory of such erased objects without having to close AutoCAD, especially when large number of entities are being created and erased.
Please note that reclaiming the memory shoud not be used unless you absolutely need to. Also, please refer to the ObjectARX documentation regarding its usage.
Here is a sample to that uses the "Database.ReclaimMemoryFromErasedObjects" to reclaim the memory. As explained in the ObjectARX documentation, in some scenarios, AutoCAD may not be able to reclaim memory of erased objects. To check if the reclaim was successful, a simple test is to try and open the reclaimed object. If the object was actually reclaimed, AutoCAD throws a "Autodesk.AutoCAD.Runtime.Exception" with the ErrorStatus set to "ErrorStatus.PermanentlyErased".
Here is a sample code. To try this, first run the "SetupHeavyModel" command that creates about 5000 spheres at random locations. These spheres can be erased and the memory reclaimed using the "CleanDb" command. Just to ensure that this code does not stall your system, I suggest changing the number of entities to a smaller number (say 200) and then increase it if you do not see a visually detectable amount of memory getting allocated in the system resource monitor.
[CommandMethod("SetupHeavyModel")]
static public void SetupHeavyModel()
{
    Document document =
            Application.DocumentManager.MdiActiveDocument;
    Editor editor = document.Editor;
    Database db = document.Database;
      using (Transaction tr
        = document.TransactionManager.StartTransaction())
    {
        BlockTable bt = tr.GetObject(
                                        db.BlockTableId,
                                        OpenMode.ForRead
                                    ) as BlockTable;
          BlockTableRecord btr
                        = tr.GetObject(
                                        db.CurrentSpaceId,
                                        OpenMode.ForWrite
                                    ) as BlockTableRecord;
          for (int cnt = 0; cnt < 5000; cnt++)
        {
            Solid3d sphere = new Solid3d();
            sphere.SetDatabaseDefaults();
              Random randomGen = new Random(cnt + 1);
            double radius = randomGen.NextDouble() * 50.0;
            sphere.CreateSphere(radius);
              Matrix3d randomMover;
            double xVec = randomGen.NextDouble() * 800;
            double yVec = randomGen.NextDouble() * 700;
            double zVec = randomGen.NextDouble() * 600;
            randomMover
                = Matrix3d.Displacement(
                                new Vector3d(
                                                xVec,
                                                yVec,
                                                zVec
                                            )
                                       );
            sphere.TransformBy(randomMover);
              btr.AppendEntity(sphere);
            tr.AddNewlyCreatedDBObject(sphere, true);
        }
        tr.Commit();
    }
}
  [CommandMethod("CleanDb")]
static public void CleanupDbMethod()
{
    Document document =
            Application.DocumentManager.MdiActiveDocument;
    Editor editor = document.Editor;
    Database db = document.Database;
      using (ObjectIdCollection erased = new ObjectIdCollection())
    {
        using (Transaction tr
                = document.TransactionManager.StartTransaction())
        {
            BlockTable bt = tr.GetObject(
                                            db.BlockTableId,
                                            OpenMode.ForRead
                                        ) as BlockTable;
              BlockTableRecord btr = tr.GetObject
                                        (
                                            db.CurrentSpaceId,
                                            OpenMode.ForRead
                                        ) as BlockTableRecord;
              foreach(ObjectId oid in btr)
            {
                Entity ent = tr.GetObject(
                                            oid,
                                            OpenMode.ForWrite
                                         ) as Entity;
                if (ent != null)
                {
                    ent.Erase(true);
                    erased.Add(oid);
                }
            }
            tr.Commit();
        }
        db.ReclaimMemoryFromErasedObjects(erased);
          //// Test for reclaimed objects
        //using (Transaction tr
        //        = document.TransactionManager.StartTransaction())
        //{
        //    foreach (ObjectId oid in erased)
        //    {
        //        try
        //        {
        //            Entity ent = tr.GetObject
        //                            (
        //                                oid,
        //                                OpenMode.ForRead
        //                            ) as Entity;
        //        }
        //        catch (Autodesk.AutoCAD.Runtime.Exception ex)
        //        {
        //            if (ex.ErrorStatus !=
        //                        ErrorStatus.PermanentlyErased)
        //            {
        //                editor.WriteMessage
        //                    (
        //                        "Not permanently erased !!"
        //                    );
        //            }
        //        }
        //    }
        //    tr.Commit();
        //}
        erased.Clear();
    }
}

