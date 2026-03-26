---
title: "Saving preview image of a drawing"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - DWG
  - Palette
description: "The "acdbGetPreviewBitmapFromDwg" method returns the HBITMAP of the drawing's preview image.Here is a sample code to save this preview image as a b..."
author: Autodesk
---
# Saving preview image of a drawing

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/saving-preview-image-of-a-drawing.html

## 文章内容

By Balaji Ramamoorthy
The "acdbGetPreviewBitmapFromDwg" method returns the HBITMAP of the drawing's preview image.Here is a sample code to save this preview image as a bitmap.
#include <atlimage.h>
#include <Gdiplusimaging.h>
  static void AsdkSavePreviewImage(void)
{
    HBITMAP hBitmap;
    HPALETTE hPal;
      acdbGetPreviewBitmapFromDwg
                            (
                                _T("C:\\Temp\\FirstFloor.dwg"),
                                &hBitmap,
                                &hPal
                            );
    CBitmap bitmap;
    bitmap.Attach(hBitmap);
      CImage image;
    image.Attach(bitmap);
    image.Save(_T("C:\\Temp\\FirstFloor.bmp"), Gdiplus::ImageFormatBMP);
      DeleteObject(hBitmap);
    DeleteObject(hPal);
}

## 评论

**内容**: croxeldyffic said...
Hello,
very useful code snippet!
However, I just tried it with AutoCAD Mechanical 2015 and 2017, and it seems, that the system variable THUMBSIZE does not affect the size or resolution of the preview image saved under "C:\\Temp\\FirstFloor.bmp".
Is this the indended behavior?
Have a nice day!
Reply
06/08/2016 at 11:33 PM

---
**内容**: Anil said...
Without closing the drawing file if we did some modification to drawing and then using the snippet once again. Preview Image is not getting updates.
Is this the expected behavior?
Reply
01/08/2019 at 03:15 AM

---
