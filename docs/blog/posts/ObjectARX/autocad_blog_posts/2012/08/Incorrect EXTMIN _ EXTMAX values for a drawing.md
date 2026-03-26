---
title: "Incorrect EXTMIN / EXTMAX values for a drawing"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
description: "AutoCAD assumes a default value of EXTMIN and EXTMAX as (1.0E+20,1.0E+20,1.0E+20) and (-1.0E+20,-1.0E+20,-1.0E+20) and as a developer put it, it is..."
author: Autodesk
---
# Incorrect EXTMIN / EXTMAX values for a drawing

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/incorrect-extmin-extmax-values-for-a-drawing.html

## 文章内容

By Balaji Ramamoorthy
AutoCAD assumes a default value of EXTMIN and EXTMAX as (1.0E+20,1.0E+20,1.0E+20) and (-1.0E+20,-1.0E+20,-1.0E+20) and as a developer put it, it is :(1/10)th the distance of the Universe away :)
There have been a few drawings that have these values even though there are entities added to it. One possible reason for such an issue could be that the "Database.UpdateExt" method has not been called after the entities have been added to the database programmatically.
Here is a code snippet that will make this point clear :
Editor ed
        = Application.DocumentManager.MdiActiveDocument.Editor;
  // Test-1
using (Database db1 = new Database(true, false))
{
    ed.WriteMessage(String.Format("{0}Test - 1 ", Environment.NewLine));
      using (Transaction tr = db1.TransactionManager.StartTransaction())
    {
        BlockTable bt = tr.GetObject
                                    (
                                        db1.BlockTableId,
                                        OpenMode.ForRead
                                    ) as BlockTable;
          BlockTableRecord btr = tr.GetObject
                                    (
                                        db1.CurrentSpaceId,
                                        OpenMode.ForWrite
                                    ) as BlockTableRecord;
          Circle c = new Circle(Point3d.Origin, Vector3d.ZAxis, 10.0);
        btr.AppendEntity(c);
        tr.AddNewlyCreatedDBObject(c, true);
          tr.Commit();
    }
      db1.SaveAs(@"C:\Temp\Test1.dwg", DwgVersion.Newest);
    ed.WriteMessage(
            String.Format(
                            "{0}ExtMin : {1}",
                            Environment.NewLine,
                            db1.Extmin
                         )
                    );
      ed.WriteMessage(
            String.Format(
                            "{0}ExtMax : {1}",
                            Environment.NewLine,
                            db1.Extmax
                        )
                    );
      ed.WriteMessage(
            String.Format(
                            "{0}Saved Test1.dwg",
                            Environment.NewLine
                         )
                    );
}
  // Test-2
using (Database db2 = new Database(true, false))
{
    ed.WriteMessage(String.Format("{0}Test - 2 ", Environment.NewLine));
      using (Transaction tr = db2.TransactionManager.StartTransaction())
    {
        BlockTable bt = tr.GetObject
                                    (
                                        db2.BlockTableId,
                                        OpenMode.ForRead
                                    ) as BlockTable;
          BlockTableRecord btr = tr.GetObject
                                    (
                                        db2.CurrentSpaceId,
                                        OpenMode.ForWrite
                                    ) as BlockTableRecord;
          Circle c = new Circle(Point3d.Origin, Vector3d.ZAxis, 10.0);
        btr.AppendEntity(c);
        tr.AddNewlyCreatedDBObject(c, true);
          tr.Commit();
    }
      db2.UpdateExt(true);
      db2.SaveAs(@"C:\Temp\Test2.dwg", DwgVersion.Newest);
    ed.WriteMessage(
            String.Format(
                            "{0}ExtMin : {1}",
                            Environment.NewLine,
                            db2.Extmin
                         )
                    );
      ed.WriteMessage(
            String.Format(
                            "{0}ExtMax : {1}",
                            Environment.NewLine,
                            db2.Extmax
                        )
                    );
      ed.WriteMessage(
            String.Format(
                            "{0}Saved Test2.dwg",
                            Environment.NewLine
                         )
                    );
}
Test1.dwg has the extents at 1e20 even though it has an entity in the database. The reason for this is because the “UpdateExt” has not been called before saving the drawing.
Test2.dwg has the right extents after an entity is added to the database, because of the “UpdateExt” call before saving the drawing.
In ObjectARX, the equivalent method is the AcDbDatabase::updateExt().

