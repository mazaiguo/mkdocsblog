---
title: "Identify Image status"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - API
  - Plot
description: "Using “RasterImageDef” API’s “IsLoaded”, “ActiveFileName” & “SourceFileName” you can identify the status of the image in the drawing."
author: Autodesk
---
# Identify Image status

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/identify-image-status.html

## 文章内容

By Virupaksha Aithal
Using “RasterImageDef” API’s “IsLoaded”, “ActiveFileName” & “SourceFileName” you can identify the status of the image in the drawing.
Loaded : IsLoaded return True
Unloaded : IsLoaded is false and  ActiveFileName has a valid file name
Not found : IsLoaded is false and ActiveFileName is empty
Below code goes throw all the images definition in the drawing and prints its status.
[CommandMethod("ImageStatus")]
public static void ImageStatus()
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
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        DBDictionary ImageDic =
          (DBDictionary)Tx.GetObject(imageDict, OpenMode.ForRead);
          foreach (DBDictionaryEntry ImageDef in ImageDic)
        {
            RasterImageDef imageDef = (RasterImageDef)Tx.GetObject(
                                ImageDef.Value, OpenMode.ForRead);
              if (imageDef.IsLoaded)
            {
                ed.WriteMessage(imageDef.ActiveFileName +
                                " : loaded" + "\n");
            }
            else
            {
                //image may be not found or unloaded.
                if (imageDef.ActiveFileName.Length == 0)
                {
                    //no file name...
                    //ed.WriteMessage("file not found\n");
                    ed.WriteMessage(imageDef.SourceFileName +
                               " : not found" + "\n");
                }
                else
                {
                    ed.WriteMessage(imageDef.ActiveFileName +
                                 " : unloaded" + "\n");
                }
            }
        }
        Tx.Commit();
    }
}

## 评论

**内容**: Randy said...
Hi,
Part of my job involves electronically checking AutoCAD files designed and drafted by our consultants. One of my checking activities is checking xrefs. Somewhere in your toolbox of goodies, do you have a similar program in lisp or .net that reports on the status of an xref, i.e., attached, overlay, not found, unresolved, orphaned, unloaded, etc.?
Thank You!
Reply
06/27/2012 at 11:01 AM

---
**内容**: Madhukar Moogala said...
Hi Randy,
For starters, look up the methods/properties of the BlockTableRecord class in the ObjectARX Managed Reference Guide (part of the ObjectARX SDK - www.objectarx.com).
Cheers,
Stephen
Reply
06/27/2012 at 03:11 PM

---
