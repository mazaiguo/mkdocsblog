---
title: "Making two commands act as one"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plugin
description: "When a command invokes another command in your plug-in, you may want AutoCAD to treat them as a single command for sake of undo and when user wishe..."
author: Autodesk
---
# Making two commands act as one

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/making-two-commands-act-as-one.html

## 文章内容

By Balaji Ramamoorthy
When a command invokes another command in your plug-in, you may want AutoCAD to treat them as a single command for sake of undo and when user wishes to repeat the last run command.
For example, if a command "Test1" invokes another command named "Test2", you may want both the actions to be undone by AutoCAD when user presses the Ctrl+Z. Similarly, when repeating the last run command by pressing the "Enter" key, you may want AutoCAD to invoke "Test1" and not "Test2" command.
To do this, you will need to "hide" the "Test2" command by using the "CommandFlags.NoHistory" and "CommandFlags.NoUndoMarker".
Here is the sample code. To understand the effect of these commandflags, you may compare the AutoCAD behavior with and without these Command flags.
[CommandMethod("Test1")]
static public void Test1Method()
{
    Document activeDoc = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
      Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    ed.WriteMessage("\nInside Test1...");
      // Create a Line
    double dist = 10.0;
    Point3d mid = Point3d.Origin;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = tr.GetObject(
                                        db.BlockTableId,
                                        OpenMode.ForRead
                                    ) as BlockTable;
        BlockTableRecord ms = tr.GetObject
                                        (
                                            db.CurrentSpaceId,
                                            OpenMode.ForWrite
                                        ) as BlockTableRecord;
        Point3d sp = mid.TransformBy
                        (
                            Matrix3d.Displacement
                            (
                                new Vector3d(-0.70710678,
                                             -0.70710678,
                                             0.0
                                            ) * dist
                            )
                        );
        Point3d ep = mid.TransformBy
                        (
                            Matrix3d.Displacement
                            (
                                new Vector3d(
                                             0.70710678,
                                             0.70710678,
                                             0.0
                                            ) * dist
                            )
                        );
        Line line = new Line(sp, ep);
          ms.AppendEntity(line);
        tr.AddNewlyCreatedDBObject(line, true);
        tr.Commit();
    }
      // Invoke "Test2"
    activeDoc.SendStringToExecute("Test2 ", false, false, false);
}
  // Uncomment this to understand the difference.
//[CommandMethod("Test2")]
  [CommandMethod("Test2", CommandFlags.NoHistory | CommandFlags.NoUndoMarker)]
static public void Test2Method()
{
    Document activeDoc
                = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
      Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    ed.WriteMessage("\nInside Test2...");
      // Create a Circle
    double radius = 10.0;
    Point3d center = Point3d.Origin;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = tr.GetObject(
                                       db.BlockTableId,
                                       OpenMode.ForRead
                                   ) as BlockTable;
        BlockTableRecord ms = tr.GetObject
                                        (
                                            db.CurrentSpaceId,
                                            OpenMode.ForWrite
                                        ) as BlockTableRecord;
          Circle circle = new Circle(center, Vector3d.ZAxis, radius);
          ms.AppendEntity(circle);
        tr.AddNewlyCreatedDBObject(circle, true);
        tr.Commit();
    }
}

