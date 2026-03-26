---
title: "Changing raster image paths in drawing to relative paths"
date: 2015-04-01
categories:
  - AutoCAD
tags:
  - DWG
description: "Here is a code snippet to change the raster image paths in a drawing from absolute path to one that is relative to the host drawing path. Raster im..."
author: Autodesk
---
# Changing raster image paths in drawing to relative paths

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/changing-raster-image-paths-in-drawing-to-relative-paths.html

## 文章内容

By Balaji Ramamoorthy
Here is a code snippet to change the raster image paths in a drawing from absolute path to one that is relative to the host drawing path. Raster images that already have a relative path set remain unchanged.
 using  System.IO;
   Document doc 
 = Application.DocumentManager.MdiActiveDocument;
 Editor ed = doc.Editor;
   string  dwgFilePath = null ;
 dwgFilePath = @"D:\Temp\Test.dwg" ;
   using  (Database db = new  Database(false , true ))
 {
     db.ReadDwgFile(dwgFilePath, 
         FileOpenMode.OpenForReadAndWriteNoShare, 
         false , "" );
       using  (Transaction tr 
         = db.TransactionManager.StartTransaction())
     {
         DBDictionary nod = tr.GetObject(
             db.NamedObjectsDictionaryId, 
             OpenMode.ForRead) as  DBDictionary;
         ObjectId imageDictId = nod.GetAt("ACAD_IMAGE_DICT" );
         DBDictionary imageDict 
             = tr.GetObject(imageDictId, OpenMode.ForRead) 
                 as  DBDictionary;
           foreach  (DBDictionaryEntry dbDictEntry in  imageDict)
         {
             RasterImageDef rasterImageDef = tr.GetObject(
                 dbDictEntry.Value, 
                 OpenMode.ForWrite) as  RasterImageDef;
               ed.WriteMessage("{0} Old SourcefileName : {1}" , 
             Environment.NewLine, rasterImageDef.SourceFileName);
               try 
             {
                 if  (File.Exists(rasterImageDef.SourceFileName))
                 {
                     dynamic dwgPathUri 
                             = new  Uri(dwgFilePath);
                     dynamic rasterImagePathUri 
                         = new  Uri(rasterImageDef.SourceFileName);
                       // Make the raster image path  
                     // relative to the drawing path 
                     dynamic relativeRasterPathUri 
                         = dwgPathUri.MakeRelativeUri
                                 (rasterImagePathUri);
                       // Set the source path as relative 
                     rasterImageDef.SourceFileName 
                     = Uri.UnescapeDataString(
                         relativeRasterPathUri.ToString());
                       ed.WriteMessage(
                         "{0} Image path changed to : {1}" , 
                         Environment.NewLine, 
                         rasterImageDef.SourceFileName);
                       // Reload for AutoCAD to  
                     // resolve active path 
                     rasterImageDef.Load();
                       // Check if we found it 
                     ed.WriteMessage("{0} Image found at : {1}" ,
                     Environment.NewLine, 
                     rasterImageDef.ActiveFileName);
                 }
             }
             catch  (UriFormatException ex)
             {
                 // Will ignore this. 
                 // If the raster image path is already relative 
                 // we might catch this exception 
             }
         }
           tr.Commit();
     }
       db.SaveAs(db.OriginalFileName, 
             true , 
             db.OriginalFileVersion, 
             db.SecurityParameters);
 }

## 评论

**内容**: PT said...
In the .NET environment, if you try this where the total path length of the drawing (including the drawing name) plus the length of the relative path to the image, including the image filename, exceeds the 256 limit, then this will give an eFileAccess error.
If you do the same test using the XREF palette and the right-click Path > Make Relative command, then it will work. So there seems to be a bug in the .NET API.
Reply
09/28/2017 at 04:30 PM

---
