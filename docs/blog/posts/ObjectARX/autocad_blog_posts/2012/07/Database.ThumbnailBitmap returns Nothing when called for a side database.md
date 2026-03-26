---
title: "Database.ThumbnailBitmap returns Nothing when called for a side database"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - DWG
  - Database
description: "The following code does not correctly ready the ThumbnailBitmap property:"
author: Autodesk
---
# Database.ThumbnailBitmap returns Nothing when called for a side database

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/databasethumbnailbitmap-returns-nothing-when-called-for-a-side-database.html

## 文章内容

By Virupaksha Aithal
The following code does not correctly ready the ThumbnailBitmap property:
    using (Database OpenDb = new Database(false, false))
    {
        OpenDb.ReadDwgFile("c:\\temp\\test.dwg",
            FileOpenMode.OpenForReadAndWriteNoShare, true, "");
          Bitmap thumbNail = OpenDb.ThumbnailBitmap;
          if (thumbNail == null)
        {
           //
        }
        else
        {
            //
        }
    }
     This is because the DWG file has been opened without share permission, and so the ThumbnailBitmap property is unable to query the DWG file for the bitmap. (For performance reasons, the bitmap is read on demand from the DWG file).
The solution is to open the DWG with share permission, for example:
using (Database OpenDb = new Database(false, false))
{
    OpenDb.ReadDwgFile("c:\\temp\\test.dwg",
        FileOpenMode.OpenForReadAndReadShare, true, "");
      Bitmap thumbNail = OpenDb.ThumbnailBitmap;
      if (thumbNail == null)
    {
       //
    }
    else
    {
        //
    }
}

