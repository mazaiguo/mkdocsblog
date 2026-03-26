---
title: "Applying material to a cylinder"
date: 2013-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Dimension
  - Unicode
description: "When applying a material with a texture image, it is important to get the parameters right for AutoCAD to show it as you expect. Here is a YouTube ..."
author: Autodesk
---
# Applying material to a cylinder

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/applying-material-to-a-cylinder.html

## 文章内容

By Balaji Ramamoorthy
When applying a material with a texture image, it is important to get the parameters right for AutoCAD to show it as you expect. Here is a YouTube video that shows the steps to map a material on to a cylinder using the AutoCAD UI. The recording uses a AutoCAD 2010 and the materials UI in newer releases of AutoCAD has changed since then.But the video should still give you an idea of the parameters required to get the material mapping right.
AutoCAD : David Cohn - Applying materials
In this post, we will look at a sample code to do a similar material mapping using the API. The sample code creates a cylinder and sets the material map parameters based on the dimensions of the image chosen.
using Autodesk.AutoCAD.GraphicsInterface;
  [CommandMethod("Map2Cyl")]
public static void Map2CylinderMethod()
{
    Document activeDoc = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
    Editor ed = activeDoc.Editor;
      Autodesk.AutoCAD.Windows.OpenFileDialog fd
        = new Autodesk.AutoCAD.Windows.OpenFileDialog
          (
            "Select an Image file to wrap",
            String.Empty,
            "jpg;",
            "Jpg File",
            Autodesk.AutoCAD.Windows.OpenFileDialog.OpenFileDialogFlags.NoUrls
          );
      System.Windows.Forms.DialogResult result = fd.ShowDialog();
    if (result != System.Windows.Forms.DialogResult.OK)
        return;
      String textureImageFilePath = fd.Filename;
    String materialName
            = System.IO.Path.GetFileName(textureImageFilePath);
      int imgWidth = 1;
    int imgHeight = 1;
    using (FileStream fs = new FileStream(
                                            textureImageFilePath,
                                            FileMode.Open,
                                            FileAccess.Read,
                                            FileShare.ReadWrite
                                         ))
    {
        using (System.Drawing.Image img
                        = System.Drawing.Image.FromStream(fs))
        {
            imgHeight = img.Size.Height;
            imgWidth = img.Size.Width;
        }
    }
      ObjectId surfaceId = ObjectId.Null;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        Circle circle = new Circle(
                                    Point3d.Origin,
                                    Vector3d.ZAxis,
                                    imgWidth * 0.5 / Math.PI);
          BlockTable bt = tr.GetObject(
                                        db.BlockTableId,
                                        OpenMode.ForRead
                                    ) as BlockTable;
          BlockTableRecord model = tr.GetObject(
                                bt[BlockTableRecord.ModelSpace],
                                OpenMode.ForWrite
                                ) as BlockTableRecord;
          surfaceId = model.AppendEntity(circle);
        tr.AddNewlyCreatedDBObject(circle, true);
          Profile3d profile = new Profile3d(circle);
        Vector3d direction = new Vector3d(0, 0, imgHeight);
        SweepOptions sweepOptions = new SweepOptions();
          surfaceId =
        Autodesk.AutoCAD.DatabaseServices.Surface.CreateExtrudedSurface
                    (profile, direction, sweepOptions, true);
          tr.Commit();
    }
      ObjectId materialId = AddMaterialToLibrary
                                (
                                    materialName,
                                    textureImageFilePath,
                                    imgHeight
                                );
      if (materialId.IsValid)
    {
        // Associate the surface with the cylinder
        //and set the visual style to "Realistic" to see the change
        using (Transaction tr = db.TransactionManager.StartTransaction())
        {
            Autodesk.AutoCAD.DatabaseServices.Surface surf =
                    tr.GetObject(surfaceId, OpenMode.ForWrite)
                    as Autodesk.AutoCAD.DatabaseServices.Surface;
              surf.MaterialId = materialId;
              // Apply a cylindrical material map to the surface
            // while inheriting the other mapping from the material
            Mapper mapper = new Mapper
                (
                    Projection.Cylinder,
                    Tiling.InheritTiling,
                    Tiling.InheritTiling,
                    AutoTransform.InheritAutoTransform,
                    Matrix3d.Identity
                );
            surf.MaterialMapper = mapper;
              ViewportTable vt =
            (ViewportTable)tr.GetObject(
                                            db.ViewportTableId,
                                            OpenMode.ForRead
                                        );
              ViewportTableRecord vtr =
            (ViewportTableRecord)tr.GetObject(
                                            vt["*Active"],
                                            OpenMode.ForWrite
                                        );
              DBDictionary dict =
            (DBDictionary)tr.GetObject(
                                        db.VisualStyleDictionaryId,
                                        OpenMode.ForRead
                                      );
              vtr.VisualStyleId = dict.GetAt("Realistic");
            tr.Commit();
        }
        ed.UpdateTiledViewportsFromDatabase();
    }
}
  public static ObjectId AddMaterialToLibrary
                                    (
                                        String sMaterialName,
                                        String sTextureMapPath,
                                        int height
                                    )
{
    ObjectId materialId = ObjectId.Null;
    Document doc = Application.DocumentManager.MdiActiveDocument;
    using (Transaction acTrans
                    = doc.TransactionManager.StartTransaction())
    {
        // Get the material library
        DBDictionary matLib
                = acTrans.GetObject
                        (
                            doc.Database.MaterialDictionaryId,
                            OpenMode.ForRead
                        ) as DBDictionary;
          // If this material does not exist
        if (matLib.Contains(sMaterialName) == false)
        {
            // Create the texture map image
            ImageFileTexture tex = new ImageFileTexture();
            tex.SourceFileName = sTextureMapPath;
              double uScale = 1.0, vScale = 1.0 / height;
            double uOffset = 0, vOffset = 0;
              Matrix3d mx = new Matrix3d(new double[]
                            {
                              uScale, 0, 0, uScale * uOffset,
                              0, vScale, 0, vScale * vOffset,
                              0, 0, 1, 0,
                              0, 0, 0, 1
                            }
                                       );
              // We need a cylindrical mapping with no tiling
            Mapper mapper = new Mapper
                            (
                                Projection.Cylinder,
                                Tiling.Crop,
                                Tiling.Crop,
                                AutoTransform.None,
                                mx
                            );
              MaterialMap map = new MaterialMap
                            (
                                Source.File,
                                tex,
                                1.0,
                                mapper
                            );
              // Set the opacity and refraction maps
            MaterialDiffuseComponent mdc
                = new MaterialDiffuseComponent
                            (
                                new MaterialColor(),
                                map
                            );
            MaterialRefractionComponent mrc
                = new MaterialRefractionComponent
                            (
                                2.0,
                                map
                            );
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
            materialId = matLib.SetAt(sMaterialName, mat);
            acTrans.AddNewlyCreatedDBObject(mat, true);
            acTrans.Commit();
        }
    }
    return materialId;
}
Here is the output of the program using an image of a Coca-Cola® label that I used for the texture image :

## 评论

**内容**: Volodymyr said...
Hi Balaji.
How setup self illumination of material (filter color, luminance, color temperature)?
Thank you!
Volodymyr.
Reply
08/26/2016 at 01:24 AM

---
