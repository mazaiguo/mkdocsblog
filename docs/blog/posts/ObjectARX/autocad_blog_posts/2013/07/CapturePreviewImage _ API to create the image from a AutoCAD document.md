---
title: "CapturePreviewImage : API to create the image from a AutoCAD document"
date: 2013-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
description: "The easy way to create an image from the drawing file is to use the “CapturePreviewImage” API of document. As this is an API of document, you need ..."
author: Autodesk
---
# CapturePreviewImage : API to create the image from a AutoCAD document

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/capturepreviewimage-api-to-create-the-image-from-a-autocad-document.html

## 文章内容

By Virupaksha Aithal
The easy way to create an image from the drawing file is to use the “CapturePreviewImage” API of document. As this is an API of document, you need to open the drawing file in the editor to use this API.
[CommandMethod("CreateImage")]
static public void CreateImage()
{
    //zoom extents... need to use .NET 4.0
    dynamic acad = Application.AcadApplication;
    acad.ZoomExtents();
      Document doc = Application.DocumentManager.MdiActiveDocument;
    using (Bitmap image = doc.CapturePreviewImage(376, 292))
    {
        //save the image...
        image.Save("c:\\temp\\test.png",
                    System.Drawing.Imaging.ImageFormat.Png);
    }
}

