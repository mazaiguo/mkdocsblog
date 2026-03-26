---
title: "Saving drawing as DXF"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - DWG
  - DXF
  - Database
description: "You can use database API “DxfOut” to export/save the drawing as DXF file. Below simple code shows the procedure to save the current drawing to vari..."
author: Autodesk
---
# Saving drawing as DXF

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/saving-drawing-as-dxf.html

## 文章内容

By Virupaksha Aithal
You can use database API “DxfOut” to export/save the drawing as DXF file. Below simple code shows the procedure to save the current drawing to various versions of DXF
DwgVersion.AC1021 – for AutoCAD 2007 version
DwgVersion. AC1800– for AutoCAD 2004 version
DwgVersion. AC1015 – for AutoCAD 2000 version
DwgVersion. AC1009 – for AutoCAD R12 version
[CommandMethod("SaveDxfFile")]
public static void SaveDxfFile()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
      //save as R12 version dxf
    //db.DxfOut("c:\\temp\\test.dxf", 16, DwgVersion.AC1009);
      //save as 2000 version dxf
    //db.DxfOut("c:\\temp\\test.dxf", 16, DwgVersion.AC1015);
      //save as 2004 version dxf
    //db.DxfOut("c:\\temp\\test.dxf", 16, DwgVersion.AC1800);
      //save as 2007 version dxf
    db.DxfOut("c:\\temp\\test.dxf", 16, DwgVersion.AC1021);
}

## 评论

**内容**: Bernhard Hfaner said...
I need help in saving a drawing in AutoCAD 2000 or 2004dxf-format. With savas the dxf-options don't show up!
It is very important to me since I must write dxf-files and for that purpose I am making drawings with needed content which then serves as template for writing the appropriate dxf-file. Thanks
Reply
06/27/2013 at 09:10 AM

---
**内容**: Massimo said in reply to Bernhard Hfaner...
Look better, the option is still there, just pull down the file-type list.
By the way, this blog is about plug-in development...
Reply
06/28/2013 at 02:31 AM

---
**内容**: Bertrand said...
I am wondering if it's possible to create a dxf of only some entities from modelspace...
Reply
03/11/2015 at 05:00 AM

---
**内容**: Virupaksha Aithal said...
Hi
I feel you can achieve this by using wblock API.
First, create a new database from selected entities using wblock. Refer http://adndevblog.typepad.com/autocad/2012/06/wblock-creating-new-drawing-from-selected-objects.html .
Now, use the new database to call dxout as shown in above post
Reply
03/23/2015 at 03:22 AM

---
