---
title: "Creating an ellipse"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "If you set the properties of the ellipse in the below manner, it won't work because the Center cannot be set for a curve that still does not have i..."
author: Autodesk
---
# Creating an ellipse

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/creating-an-ellipse.html

## 文章内容

By Balaji Ramamoorthy
If you set the properties of the ellipse in the below manner, it won't work because the Center cannot be set for a curve that still does not have its start and end point defined.
This does not work :
myEllipse = New Ellipse()
myEllipse.Center = New Point3d(0.0, 0.0, 0.0)
myEllipse.StartPoint = New Point3d(-10, 0, 0)
myEllipse.EndPoint = New Point3d(10, 0, 0)
myEllipse.RadiusRatio = 2.0
This is "as designed" - The call to StartPoint and EndPoint will throw an exception when the curve has no start point and end point. Use the HasStartPoint and HasEndPoint properties before calling StartPoint and EndPoint.
The way to create an ellipse is to use the constructor of ellipse class and pass the parameters.
For example:
Ellipse myEllipse = new Ellipse(center, normal, majorAxis, radiusRatio, startAng, endAng);
Here is a sample code :
[CommandMethod("CreateEllipse")]
static public void CreateEllipseMethod()
{
    Document doc
            = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction tr
                    = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = tr.GetObject(
                                        db.BlockTableId,
                                        OpenMode.ForRead,
                                        false
                                    ) as BlockTable;
          BlockTableRecord modelSpace =
                 tr.GetObject(
                                bt[BlockTableRecord.ModelSpace],
                                OpenMode.ForWrite,
                                false
                              ) as BlockTableRecord;
          Point3d center = Point3d.Origin;
        Vector3d normal = Vector3d.ZAxis;
        Vector3d majorAxis = 100 * Vector3d.XAxis;
        double radiusRatio = 0.5;
        double startAng = 0.0;
        double endAng = 360 * Math.Atan(1.0) / 45.0;
          Ellipse ellipse = new Ellipse(center,
                                        normal,
                                        majorAxis,
                                        radiusRatio,
                                        startAng,
                                        endAng
                                    );
          // The following lines don't work!!               
        //Ellipse ellipse = new Ellipse();
        //ellipse.SetDatabaseDefaults();
        //ellipse.Center = Point3d.Origin;
        //ellipse.StartPoint = new Point3d(-10.0, 0.0, 0.0);
        //ellipse.EndPoint = new Point3d(10.0, 0.0, 0.0);
        //ellipse.RadiusRatio = 2.0;
        //ellipse.ColorIndex = 1;
          ellipse.ColorIndex = 1;
          modelSpace.AppendEntity(ellipse);
        tr.AddNewlyCreatedDBObject(ellipse, true);
          tr.Commit();
    }
}

## 评论

**内容**: Kai Siegele said...
Dear Mr. Ramamoorthy,
I am going to draw an ellipse in two dimensions having an origin, a height and a width.
I am trying to use your example but I cannot follow how to calculate the value for radiusRatio (from 2.0 to 0.5) and how to calculate the 100 (perhaps from -10 and 10?).
Would you be so kind and give me a hint? I am looking to your reply.
Best reagards
Kai Siegele
Reply
01/15/2013 at 02:28 AM

---
**内容**: Balaji said in reply to Kai Siegele...
Dear Kai Siegele,
Sorry if the commented lines caused some confusion. The commented lines were only to inform that the Center cannot be set without having the start and end points defined. The values that I have taken are arbitrary and does not have any relation with the major axis of 100 that I have used in the working code.
Here is the explanation of the working code :
Major Axis = 100 units
So, major axis points will be (-100, 0) and (100,0)
Radius ratio is 0.5 which makes the minor axis = 50
So, minor axis points will be (0, 50) and (0, -50)
Hope this clarifies and let me know if you have any specific queries on this topic.
Reply
01/15/2013 at 02:45 AM

---
