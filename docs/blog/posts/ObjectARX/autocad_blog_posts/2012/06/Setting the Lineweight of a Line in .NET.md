---
title: "Setting the Lineweight of a Line in .NET"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Plugin
description: "Here’s a simple example, originally posted by Fenton on the ADN website,  showing how to set the lineweight of a line as you’re adding it to the cu..."
author: Autodesk
---
# Setting the Lineweight of a Line in .NET

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/setting-the-lineweight-of-a-line-in-net.html

## 文章内容

By Stephen Preston
Here’s a simple example, originally posted by Fenton on the ADN website,  showing how to set the lineweight of a line as you’re adding it to the currently active space (model or paper):
[Autodesk.AutoCAD.Runtime.CommandMethod("CreateLine")]
// creates a line and sets the lineweight for it,
//  by Fenton Webb, DevTech, Autodesk
public void CreateLine()
{
  // create a new line
  Line line =
        new Line(new Point3d(0, 0, 0), new Point3d(100, 100, 0));
  // set the lineweight for it
  line.LineWeight = LineWeight.LineWeight211;
  // add the object to the current space
  Database db =
          Application.DocumentManager.MdiActiveDocument.Database;
  // make sure lineweights are turned on
  db.LineWeightDisplay = true;
  // start a new transaction
  using (Transaction myT = db.TransactionManager.StartTransaction())
  {
    try
    {
      // get the current space and open it for write
      BlockTableRecord btr =
        (BlockTableRecord)myT.GetObject(db.CurrentSpaceId,
                                      OpenMode.ForWrite, false);
      // add line to the blocktable record
      btr.AppendEntity(line);
      // now to the tranaction manager
      myT.AddNewlyCreatedDBObject(line, true);
      // all ok, lets commit it
      myT.Commit();
    }
    catch
    {
      // Handle errors
    }
  }
}

