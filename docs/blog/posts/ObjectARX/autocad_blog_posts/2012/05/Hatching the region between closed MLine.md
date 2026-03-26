---
title: "Hatching the region between closed MLine"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Database
  - Hatch
description: "Here is a sample code to demonstrate a way to create a closed MLine and hatch the region between them. An internal point that lie within the MLine ..."
author: Autodesk
---
# Hatching the region between closed MLine

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/hatching-the-region-between-closed-mline.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to demonstrate a way to create a closed MLine and hatch the region between them. An internal point that lie within the MLine is determined and this internal point is used to create the hatch. Here is a sample code :
using System.Reflection;
[CommandMethod("MLineHatch")]
static public void MLineHatch()
{
    Database db
        = Application.DocumentManager.MdiActiveDocument.Database;
      // step 1: Creating the MLine
    ObjectId mlineOid = ObjectId.Null;
    using (Transaction myT
                    = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = myT.GetObject(
                                        db.BlockTableId,
                                        OpenMode.ForRead,
                                        false
                                     ) as BlockTable;
        BlockTableRecord btr
            = myT.GetObject(
                                bt[BlockTableRecord.ModelSpace],
                                OpenMode.ForWrite,
                                false
                            ) as BlockTableRecord;
          Mline ml = new Mline();
        ml.SetDatabaseDefaults();
          DBDictionary mlDict
            = myT.GetObject(
                                db.MLStyleDictionaryId,
                                OpenMode.ForRead
                            ) as DBDictionary;
        ml.Style = mlDict.GetAt("Standard");
        ml.Normal = Vector3d.ZAxis;
          ml.AppendSegment(Point3d.Origin);
        ml.AppendSegment(new Point3d(10.0, 10.0, 0.0));
        ml.AppendSegment(new Point3d(20.0, 0.0, 0.0));
        ml.IsClosed = true;
          mlineOid = btr.AppendEntity(ml);
        myT.AddNewlyCreatedDBObject(ml, true);
          myT.Commit();
    }
      // step 2: Get the internal point for us to use and
    // trigger a hatch.
    Point3dCollection hatchPoints = new Point3dCollection();
    Point3dCollection vertices = new Point3dCollection();
    using (Transaction myT
                    = db.TransactionManager.StartTransaction())
    {
        Mline ml = myT.GetObject(
                                    mlineOid,
                                    OpenMode.ForRead,
                                    false
                                ) as Mline;
          // Get the individual linees
        DBObjectCollection lines = new DBObjectCollection();
        ml.Explode(lines);
          // Get the vertices of the lines
        foreach (DBObject dbObj in lines)
        {
            Line line = dbObj as Line;
            vertices.Add(line.StartPoint);
              // Get a single point
            // (startpoint same as end point) for each loop
            if (vertices.Contains(line.EndPoint))
            {
                if (hatchPoints.Contains(line.EndPoint) == false)
                {
                    hatchPoints.Add(line.EndPoint);
                }
            }
        }
          lines.Dispose();
        myT.Commit();
    }
      // step 3 : Begin hatching the Mline using the
    // points identified in step 2
    Point3d hatchPoint;
    Point3d internalPoint;
      Object acadObject = Application.AcadApplication;
    object ActiveDocument
        = acadObject.GetType().InvokeMember
        (
            "ActiveDocument",
            System.Reflection.BindingFlags.GetProperty,
            null,
            acadObject,
            null
        );
    object[] dataArry = new object[1];
      for (int cnt = 0; cnt < hatchPoints.Count - 1; cnt++)
    {
        hatchPoint = hatchPoints[cnt];
        internalPoint
            = hatchPoint.TransformBy
                (
                    Matrix3d.Displacement
                        (
                            hatchPoint.GetVectorTo(hatchPoints[cnt + 1]) * 0.85
                        )
                );
          dataArry[0] = "-hatch P S C " + (cnt + 1).ToString() + "\n\n";
        ActiveDocument.GetType().InvokeMember(
                                                "SendCommand",
                                                BindingFlags.InvokeMethod,
                                                null,
                                                ActiveDocument,
                                                dataArry
                                             );
          dataArry[0] = internalPoint.X.ToString() + "," + internalPoint.Y.ToString();
        ActiveDocument.GetType().InvokeMember(
                                                "SendCommand",
                                                BindingFlags.InvokeMethod,
                                                null,
                                                ActiveDocument,
                                                dataArry
                                             );
          dataArry[0] = "\n\n";
        ActiveDocument.GetType().InvokeMember(
                                                "SendCommand",
                                                BindingFlags.InvokeMethod,
                                                null,
                                                ActiveDocument,
                                                dataArry
                                             );
    }
}

