---
title: "Setting transparency amount of a newly created material using .NET"
date: 2016-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
description: "To define the amount of transparency of a new material, AutoCAD .NET API uses MaterialOpacityComponent"
author: Autodesk
---
# Setting transparency amount of a newly created material using .NET

发布日期: 2016-05-01

原始链接: https://adndevblog.typepad.com/autocad/2016/05/setting-transparency-amount-of-a-newly-created-material-using-net.html

## 文章内容

By Deepak Nadig
To define the amount of transparency of a new material, AutoCAD .NET API uses MaterialOpacityComponent
Below code adds a new material to Material Library with transparency amount set to 90.
[CommandMethod("AddMaterialToLibrary")]
public static void AddMaterialToLibrary()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    String sMaterialName = "MyMaterial";
    String sTextureMapPath = @"C:\test.jpg";
    using (Transaction acTrans = doc.TransactionManager.StartTransaction())
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
              Mapper mapper = new Mapper(
                Projection.Cylinder, Tiling.Tile, Tiling.Tile,
                AutoTransform.None, mx);
              MaterialMap map =
              new MaterialMap(Source.File, tex, 1.0, mapper);
                MaterialDiffuseComponent mdc =
              new MaterialDiffuseComponent(new MaterialColor(), map);
            MaterialRefractionComponent mrc =
              new MaterialRefractionComponent(2.0, map);
              //Set the opacity
            MaterialOpacityComponent moc =
              new MaterialOpacityComponent(0.1, map);
              // Create a new material
            Material mat = new Material();
            mat.Name = sMaterialName;
            mat.Diffuse = mdc;
            mat.Refraction = mrc;
            mat.Opacity = moc;
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
Interestingly in the above code, percentage parameter of MaterialOpacityComponent can be set from values 0 to 1, where 0 indicates
non opacity(complete transparency) and 1 indicates complete opacity(non transparency).
Interactively in AutoCAD, while editing new material, we can observe the word 'transparency' and its 'amount' being
used.Here, values from 0 to 100 can be set as amount, where 0 indicates non transparency(completely opaque) and
100 indicates complete transparency(non opaque).
Because of this behaviour, for instance, if transparency amount is 75, opacity percentage has to be set as 0.25 in
the code.

