---
title: "Get/Set image paths in drawing using .NET API"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
description: "To Get and set Image file name use the properties SourceFileName and ActiveFileName of RasterImageDef."
author: Autodesk
---
# Get/Set image paths in drawing using .NET API

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/getset-image-paths-in-drawing-using-net-api.html

## 文章内容

By Balaji Ramamoorthy
To Get and set Image file name use the properties SourceFileName and ActiveFileName of RasterImageDef.
 
Here is a sample code that changes the image file path of a raster image.
To try the below code add a raster image from UI, load the .Net dll and
issue the command editImage.
Note:
Change the file name specified (for functions SourceFileName and ActiveFileName )in the below code
to some valid file name.
[CommandMethod("editImagePath")]
public void EditImagePath()
{
    Database db = HostApplicationServices.WorkingDatabase;
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      PromptEntityOptions peo = new PromptEntityOptions("\nSelect an Image");
    peo.SetRejectMessage("\nSelected entity must be an image.");
    peo.AddAllowedClass(typeof(RasterImage), false);
      PromptEntityResult per = ed.GetEntity(peo);
    if (per.Status != PromptStatus.OK)
        return;
      ObjectId imageId = per.ObjectId;
      try
    {
        using (Transaction trans = db.TransactionManager.StartTransaction())
        {
            RasterImage myImage = trans.GetObject(imageId, OpenMode.ForRead) as RasterImage;
            RasterImageDef imageDef = trans.GetObject(myImage.ImageDefId, OpenMode.ForWrite) as RasterImageDef;
              ed.WriteMessage(imageDef.ActiveFileName);
              imageDef.SourceFileName = "C:\\Temp\\Bruno.jpg";
            imageDef.ActiveFileName = "C:\\Temp\\Bruno.jpg";
              imageDef.Load();
              trans.Commit();
        }
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.Message);
    }
}

## 评论

**内容**: Irene said...
I am having hard time finding a tutorial for removing (detaching) an xref image from the document. Do you happen to have an example?
Reply
07/30/2015 at 12:54 PM

---
**内容**: Balaji said...
Hi Irene,
This blog post should provide the steps to follow to detach it.
The code is in C++, but you can find equivalent API in the AutoCAD .Net API mostly just by dropping the "AcDb" prefix.
http://adndevblog.typepad.com/autocad/2012/08/detach-a-raster-image-using-objectarx.html
Regards,
Balaji
Reply
07/31/2015 at 08:47 AM

---
**内容**: Greg said...
Issue with a very long path (230 characters). If the image is in the same folder as DWG then specifying SourceFile=".\image.gif" results in eFileAccess error and it can't find the file. In a shorter path this is no issue. So far the only solution is to supply the full long path but then the image is not xref'd relative. Attaching the file manually through dialog interface works no problem with relative path, so the problem is only via .NET. Often, but not always, when this occurs Directory.GetCurrentDirectory doesn't return the proper current folder of the DWG so I think .NET environment is confused as to what is the current folder and SetCurrentDirectory doesn't resolve the problem.
Reply
09/27/2017 at 12:12 PM

---
