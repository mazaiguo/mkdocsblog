---
title: "Setting U and V tile scale of a newly created material using .NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Database
  - Plugin
description: "I'm creating a new material using the .NET API and I can set most of the things I want, but I cannot find where to set the U and V tile scales for ..."
author: Autodesk
---
# Setting U and V tile scale of a newly created material using .NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/setting-u-and-v-tile-scale-of-a-newly-created-material-using-net.html

## 文章内容

By Adam Nagy
I'm creating a new material using the .NET API and I can set most of the things I want, but I cannot find where to set the U and V tile scales for the diffuse I'm adding.
Solution
You need to set those using the transformation matrix. The following sample shows how:
using System;
using Autodesk.AutoCAD.DatabaseServices;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
using Autodesk.AutoCAD.GraphicsInterface;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.Geometry;
  namespace MaterialTest
{
  public class Commands
  {
    public static void AddMaterialToLibrary(
      String sMaterialName, String sTextureMapPath)
    {
      Document doc = acApp.DocumentManager.MdiActiveDocument;
      using (
        Transaction acTrans =
          doc.TransactionManager.StartTransaction())
      {
        // Get the material library
        DBDictionary matLib =
          (DBDictionary)acTrans.GetObject(
            doc.Database.MaterialDictionaryId, OpenMode.ForRead);
          // If this material does not exist
        if (matLib.Contains(sMaterialName) == false)
        {
          // Create the texture map image
          ImageFileTexture tex = new ImageFileTexture();
          tex.SourceFileName = sTextureMapPath;
            // Create the material map
          double uScale = 15, vScale = 20;
          double uOffset = 25, vOffset = 30;
          Matrix3d mx = new Matrix3d(new double[]{
              uScale, 0, 0, uScale * uOffset,
              0, vScale, 0, vScale * vOffset,
              0, 0, 1, 0,
              0, 0, 0, 1});
            Mapper mapper =
            new Mapper(
              Projection.Cylinder, Tiling.Tile, Tiling.Tile,
              AutoTransform.None, mx);
            MaterialMap map =
            new MaterialMap(Source.File, tex, 1.0, mapper);
            // Set the opacity and refraction maps
          MaterialDiffuseComponent mdc =
            new MaterialDiffuseComponent(new MaterialColor(), map);
          MaterialRefractionComponent mrc =
            new MaterialRefractionComponent(2.0, map);
            // Create a new material
          Material mat = new Material();
          mat.Name = sMaterialName;
          mat.Diffuse = mdc;
          mat.Refraction = mrc;
          mat.Mode = Mode.Realistic;
          mat.Reflectivity = 1.0;
          mat.IlluminationModel = IlluminationModel.BlinnShader;
            // Add it to the library
          matLib.UpgradeOpen();
          matLib.SetAt(sMaterialName, mat);
          acTrans.AddNewlyCreatedDBObject(mat, true);
          acTrans.Commit();
        }
      }
    }
      [CommandMethod("Test")]
    public static void Test()
    {
      AddMaterialToLibrary(
        "MyMaterial", @"C:\MaterialTest\MaterialTest\test.png");
    }
  }
}
Here you see the properties of the material we created in the user interface:

## 评论

**内容**: Fred Dickinson said...
Thanks for this site.
Just one little thing ... could you change the gold lettering to a colour with better contrast on a white/grey background?
Reply
05/29/2012 at 04:43 AM

---
**内容**: vilas jadhav said...
Dear Sir,
It is very useful task for me . but I am in strong in Auto lisp , It is possible to create new material library in auto lisp.
thanks
Vilas Jadhav
Reply
01/07/2014 at 04:41 AM

---
**内容**: ChenX said...
Can i set uv to rotate?
Reply
09/04/2017 at 06:58 PM

---
