---
title: "RasterImage Inverse Transform"
date: 2013-08-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "A BlockReference provides the "BlockTransform" matrix which can be helpful in case you need to transform the entity to negate the effects of displa..."
author: Autodesk
---
# RasterImage Inverse Transform

发布日期: 2013-08-01

原始链接: https://adndevblog.typepad.com/autocad/2013/08/rasterimage-inverse-transform.html

## 文章内容

By Balaji Ramamoorthy
A BlockReference provides the "BlockTransform" matrix which can be helpful in case you need to transform the entity to negate the effects of displacement, rotation and scaling. A RasterImage entity does not provide a similar matrix, but can be constructed knowing the individual rotation, displacement and scale values in x and y directions. Here is a sample code to negate the scaling, displacement and rotation of a selected raster image.
[CommandMethod("RITest")]
public void RITestMethod()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed
        = Application.DocumentManager.MdiActiveDocument.Editor;
      PromptEntityOptions opts
            = new PromptEntityOptions("Pick a raster image : ");
    opts.SetRejectMessage("Must select a raster image");
    opts.AddAllowedClass
          (
            typeof(Autodesk.AutoCAD.DatabaseServices.RasterImage),
            false
          );
      PromptEntityResult res = ed.GetEntity(opts);
    if (res.Status != PromptStatus.OK)
        return;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        RasterImage ri = tr.GetObject(
                                        res.ObjectId,
                                        OpenMode.ForWrite
                                     ) as RasterImage;
          Matrix3d invTransform = Matrix3d.Identity;
          invTransform = invTransform.PreMultiplyBy
                (
                    Matrix3d.Rotation(  -ri.Rotation,
                                        Vector3d.ZAxis,
                                        ri.Orientation.Origin)
                );
          invTransform = invTransform.PreMultiplyBy
                (
                    Matrix3d.Displacement( 
                    Point3d.Origin - ri.Orientation.Origin)
                );
          Vector2d riScale = ri.Scale;
        double scaleX = riScale.X;
        double scaleY = riScale.Y;
          double[] coeffs = new double[]
        {
            scaleX, 0, 0, 0,
            0, scaleY, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        };
          Matrix3d scaleMatrix = new Matrix3d(coeffs);
        invTransform = invTransform.PreMultiplyBy
                                    (scaleMatrix.Inverse());
          ri.TransformBy(invTransform);
          // If you need the transformation matrix and not its inverse,
        // simply invert the matrix again.
        // Matrix3d riTransform = invTransform.Inverse();
          tr.Commit();
    }

## 评论

**内容**: Romain said...
It works really good thank you Balaji !
Not need to use PixelModelTransform()
Reply
08/30/2013 at 08:20 AM

---
**内容**: Balaji said in reply to Romain...
Thanks Romain.
I am glad it helped.
Reply
08/31/2013 at 06:36 AM

---
