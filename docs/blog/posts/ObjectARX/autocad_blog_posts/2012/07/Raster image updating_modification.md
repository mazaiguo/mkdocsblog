---
title: "Raster image updating/modification"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Database
description: "Below code shows the procedure to update/modify the image source of the raster image. Code, prompts the user to select a Raster image and from imag..."
author: Autodesk
---
# Raster image updating/modification

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/raster-image-updationmodification-.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to update/modify the image source of the raster image. Code, prompts the user to select a Raster image and from image, it finds the image definition to modify. Note, as image definition is getting modified, the change in image is reflected in all the references of the image definition.
[CommandMethod("updateImage")]
public static void updateImage()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
        new PromptEntityOptions("\nSelect Raster image to change");
    options.SetRejectMessage("\nSelect only Raster image");
    options.AddAllowedClass(typeof(RasterImage), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        //get the mleader
        RasterImage image = Tx.GetObject(acSSPrompt.ObjectId,
                                   OpenMode.ForRead) as RasterImage;
          RasterImageDef ImageDef = Tx.GetObject(image.ImageDefId,
                               OpenMode.ForWrite) as RasterImageDef;
          ImageDef.SourceFileName = "c:\\temp\\new.jpeg";
        ImageDef.ActiveFileName = "c:\\temp\\new.jpeg";
          ImageDef.Load();
          Tx.Commit();
    }
}

