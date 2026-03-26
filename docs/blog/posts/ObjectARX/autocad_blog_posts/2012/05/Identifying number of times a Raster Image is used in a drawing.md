---
title: "Identifying number of times a Raster Image is used in a drawing"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Database
description: "Each raster image will have a definition called “RasterImageDef” and will be stores inside the raster image Dictionary. A raster image reactor is s..."
author: Autodesk
---
# Identifying number of times a Raster Image is used in a drawing

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/identifying-number-times-a-raster-images-is-used-in-a-drawing.html

## 文章内容

By Virupaksha Aithal
Each raster image will have a definition called “RasterImageDef” and will be stores inside the raster image Dictionary. A raster image reactor is stored in “RasterImageDef” for each image referred to it. So if you count the number of raster image reactor, then you can identify the number of raster images referring to same “RasterImageDef”. Refer below code.
[CommandMethod("ImageCount")]
public static void ImageCount()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      ObjectId imageDict = RasterImageDef.GetImageDictionary(db);
      if (imageDict == ObjectId.Null)
    {
        ed.WriteMessage("No images in the drawing.\n");
        return;
    }
      using (Transaction Tx =
        db.TransactionManager.StartTransaction())
    {
        DBDictionary ImageDic =
          (DBDictionary)Tx.GetObject(imageDict,OpenMode.ForRead);
          ObjectIdCollection ImageCount = new ObjectIdCollection();
          foreach (DBDictionaryEntry ImageDef in ImageDic)
        {
            RasterImageDef imageDef = (RasterImageDef)Tx.GetObject(
                                ImageDef.Value, OpenMode.ForRead);
              ObjectIdCollection ids =
                                imageDef.GetPersistentReactorIds();
              foreach (ObjectId id in ids)
            {
                DBObject reactor =
                                Tx.GetObject(id, OpenMode.ForRead);
                string name = reactor.GetRXClass().DxfName;
                if (string.Compare(name,
                                    "IMAGEDEF_REACTOR", true) == 0)
                {
                    if (!reactor.OwnerId.IsErased)
                    {
                        DBObject obj = Tx.GetObject(reactor.OwnerId,
                                                    OpenMode.ForRead);
                          if (obj is RasterImage)
                        {
                            ImageCount.Add(obj.ObjectId);
                        }
                    }
                  }
            }
              if (ImageCount.Count > 0)
            {
                ed.WriteMessage("Raster image file " +
                    imageDef.ActiveFileName + "  is used "
               + ImageCount.Count.ToString() + " times\n");
            }
              ImageCount.Clear();
        }
          Tx.Commit();
    }
}

## 评论

**内容**: Francois said...
Keep them coming ;-)
If you have the same for xrefs, please, fell fre :-)
Reply
05/29/2012 at 05:17 AM

---
**内容**: Virupaksha Aithal said...
Thanks for the comments.
Sure, you will have xref related posts from our team.
Thanks
Viru
Reply
05/30/2012 at 12:27 AM

---
**内容**: Doublefish said...
How detect status in raster image ?
FileNotFound and Unloaded ?
Reply
06/27/2012 at 04:16 AM

---
**内容**: Virupaksha Aithal said...
Thanks for the comments.
Please refer new post http://adndevblog.typepad.com/autocad/2012/06/identify-image-status.html for the image status.
Thanks
Viru
Reply
06/27/2012 at 04:55 AM

---
