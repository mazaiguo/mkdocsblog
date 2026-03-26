---
title: "How to scale non-uniformly a raster image to fit a given area?"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - API
  - C#
  - Solid
  - Unicode
description: "Raster Images belong to the category of entities that support being scaled non-uniformly."
author: Autodesk
---
# How to scale non-uniformly a raster image to fit a given area?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-scale-non-uniformly-a-raster-image-to-fit-a-given-area.html

## 文章内容

By Philippe Leefsma
Raster Images belong to the category of entities that support being scaled non-uniformly.
The entities that support non-uniform scaling are:
AcDbLeader, AcDbMLine, AcDbMText, AcDbOle2Frame, AcDbPloyFaceMesh, AcDbPolygonMesh, AcDbRay, AcDbXline, AcDbFcf, AcDbSolid, AcDbEllipse, AcDbSpline, AcDbImage.
The API doesn’t provide a built-in functionality in order to create a non-uniform scaling matrix. You would need to create such a matrix by filling up the coefficient yourself. Building a scaling matrix is quite straightforward as it is a diagonal matrix that contains the scale coefficients corresponding respectively to x, y and z directions.
The C# command below illustrates how to scale non-uniformly a raster image so it will fit a given rectangle (Width x Height):
[CommandMethod("Scale2Fit")]
public void Scale2Fit()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions peo = new PromptEntityOptions(
        "\nSelect image: ");
      peo.SetRejectMessage("\nInvalid selection...");
    peo.AddAllowedClass(typeof(RasterImage), false);
      PromptEntityResult per = ed.GetEntity(peo);
      if (per.Status != PromptStatus.OK)
        return;
      double width = 50;
    double height = 30;
      using (Transaction Tx =
        db.TransactionManager.StartTransaction())
    {
        RasterImage image = Tx.GetObject(
            per.ObjectId,
            OpenMode.ForWrite)
                as RasterImage;
          Point3d origin = image.Orientation.Origin;
          double scaleX = width / image.Width;
        double scaleY = height / image.Height;
          double[] coeffs = new double[]
        {
            scaleX, 0, 0, 0,
            0, scaleY, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        };
          Matrix3d matrix = new Matrix3d(coeffs);
          image.TransformBy(matrix);
          //Reset original position
        image.Orientation = new CoordinateSystem3d(
            origin,
            image.Orientation.Xaxis,
            image.Orientation.Yaxis);
          Tx.Commit();
    }
}

