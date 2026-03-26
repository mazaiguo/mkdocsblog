---
title: "Creating a GraphicsInterface.ImageBGRA32"
date: 2013-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Here is a sample code to demonstrate the creation of an instance of "ImageBGRA32" class from a bitmap and to use it in a "WorldDraw" method. The co..."
author: Autodesk
---
# Creating a GraphicsInterface.ImageBGRA32

发布日期: 2013-09-01

原始链接: https://adndevblog.typepad.com/autocad/2013/09/creating-a-graphicsinterfaceimagebgra32.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to demonstrate the creation of an instance of "ImageBGRA32" class from a bitmap and to use it in a "WorldDraw" method. The code to copy the raw bytes between two arrays is not optimized and I think there are more efficient way to do it. But I hope this sample code helps you get started.
Circle c = (Circle)drawable;
Bitmap bitmap = new Bitmap(@"c:\Work\Test.bmp");
  BitmapData raw = bitmap.LockBits
    (
        new Rectangle(0, 0, (int)bitmap.Width, (int)bitmap.Height),
        ImageLockMode.ReadOnly,
        bitmap.PixelFormat
    );
  int size = raw.Height * raw.Stride;
byte[] rawImageRGB24 = new Byte[size];
System.Runtime.InteropServices.Marshal.Copy(
        raw.Scan0, rawImageRGB24, 0, size);
  byte[] rawImageBGRA32 = new Byte[bitmap.Width * bitmap.Height * 4];
int rgbIndex = 0;
int rgbaIndex = 0;
for (int row = 0; row < bitmap.Height; row++)
{
    for (int col = 0; col < bitmap.Width; col++)
    {
        rgbIndex = col * 3 + row * raw.Stride;
        rgbaIndex = col * 4 + row * bitmap.Width * 4;
          rawImageBGRA32[rgbaIndex]
                    = rawImageRGB24[rgbIndex];         // Blue
          rawImageBGRA32[rgbaIndex + 1]
                    = rawImageRGB24[rgbIndex + 1];    // Green
          rawImageBGRA32[rgbaIndex + 2]
                    = rawImageRGB24[rgbIndex + 2];    // Red
          rawImageBGRA32[rgbaIndex + 3]
                    = 255;                            // Alpha
    }
}
if (raw != null)
{
    bitmap.UnlockBits(raw);
}
  IntPtr unmanagedPointer
                = Marshal.AllocHGlobal(rawImageBGRA32.Length);
  Marshal.Copy(
             rawImageBGRA32,
             0,
             unmanagedPointer,
             rawImageBGRA32.Length);
  ImageBGRA32 imgBGRA32
    = new ImageBGRA32
                    (
                        (uint)bitmap.Width,
                        (uint)bitmap.Height,
                        unmanagedPointer
                    );
  bool result
        = wd.Geometry.Image
                (
                    imgBGRA32,
                    c.Center,
                    Vector3d.XAxis * (bitmap.Width / bitmap.Height),
                    Vector3d.YAxis
                );
Marshal.FreeHGlobal(unmanagedPointer);
return result;

## 评论

**内容**: Maxence said...
Is there a way to control the quality? I see that there is an enum Autodesk.AutoCAD.GraphicsSystem.Quality but I don't know how to use. With Geometry.Image, my image is drawn in LowQuality.
Reply
09/28/2013 at 10:06 AM

---
**内容**: Balaji said in reply to Maxence...
Hi Maxence,
I am not sure if this will improve the quality in case of a image drawn by a custom entity as I haven't tried it. To use this, please follow a code similar to the one explained in this blog post :
http://adndevblog.typepad.com/autocad/2012/07/api-for-3dconfig.html
AcGsConfig is a singleton class, so you may want to set it globally through a command.
Regards,
Balaji
Reply
10/02/2013 at 11:43 PM

---
**内容**: JamesOneil said...
Documentation is preferred overall the other how to make a promo video
for the professors. The method is instilled for the race. Success is beneficial and satisfactory of the top of the goals for the challenges.
Reply
04/14/2023 at 10:16 AM

---
