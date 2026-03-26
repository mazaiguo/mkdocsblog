---
title: "Getting the extents of AutoCAD model window"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - AutoCAD
  - C#
  - Dimension
description: "Several developers have been asking this question recently through ADN support, on how to retrieve the extents of the AutoCAD model window in world..."
author: Autodesk
---
# Getting the extents of AutoCAD model window

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/getting-the-extents-of-autocad-model-window.html

## 文章内容

By Philippe Leefsma
Several developers have been asking this question recently through ADN support, on how to retrieve the extents of the AutoCAD model window in world coordinates.
There are several approaches to achieve that, but the easiest according to me, is to rely on the “SCREENSIZE” system variable.
Here is the C# code:
  [CommandMethod("ScreenExtents")]
public void ScreenExtents()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
       Point2d screenSize = (Point2d)
        Application.GetSystemVariable("SCREENSIZE");
      System.Drawing.Point upperLeft = new System.Drawing.Point(0, 0);
      System.Drawing.Point lowerRight = new System.Drawing.Point(
        (int)screenSize.X,
        (int)screenSize.Y);
      Point3d upperLeftWorld = ed.PointToWorld(upperLeft, 0);
    Point3d lowerRightWorld = ed.PointToWorld(lowerRight, 0);
     using (Transaction Tx = db.TransactionManager.StartTransaction())
   {
        //Draws a line to visualize result...
        Line line = new Line(upperLeftWorld, lowerRightWorld);
          BlockTableRecord btr = Tx.GetObject(
            db.CurrentSpaceId, OpenMode.ForWrite)
                as BlockTableRecord;
          btr.AppendEntity(line);
        Tx.AddNewlyCreatedDBObject(line, true);
         Tx.Commit();
    }
}

## 评论

**内容**: Steven Taitinger said...
How do you get the size of the extents of model space in vba? The limits property of the document seems more related to the paper space than the model space and the width and height properties seem to be relative to the application window size.
Reply
12/10/2013 at 10:58 AM

---
**内容**: Philippe Leefsma said in reply to Steven Taitinger...
Hi Steven,
The easiest way is probably to use EXTMIN/EXTMAX system variables:

Dim Extmin As Variant
Dim Extmax As Variant

Extmin = ThisDrawing.GetVariable("EXTMIN")
Extmax = ThisDrawing.GetVariable("EXTMAX")

Debug.Print "ExtMIN = [" & Extmin(0) & ", "; Extmin(1) & ", "; Extmin(2) & "]"
Debug.Print "ExtMAX = [" & Extmax(0) & ", "; Extmax(1) & ", "; Extmax(2) & "]"
Reply
12/16/2013 at 05:20 AM

---
