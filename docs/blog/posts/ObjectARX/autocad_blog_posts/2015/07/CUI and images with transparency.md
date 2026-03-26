---
title: "CUI and images with transparency"
date: 2015-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - CUI
description: "Till AutoCAD 2014, AutoCAD used to take only BMP format images in CUI. As BMP format doesn't work with transparency, AutoCAD used to interpret RGB ..."
author: Autodesk
---
# CUI and images with transparency

发布日期: 2015-07-01

原始链接: https://adndevblog.typepad.com/autocad/2015/07/cui-and-images-with-transparency.html

## 文章内容

By Virupaksha Aithal
Till AutoCAD 2014, AutoCAD used to take only BMP format images in CUI. As BMP format doesn't work with transparency, AutoCAD used to interpret RGB color 192,192,192 as transparent. AutoCAD users had used this workaround in CUI. 
But the limitation of this approach is that the background color is fixed as 192,192,192. Any other background color will make the background visible in CUI.
From AutoCAD 2015 (and later versions), you can provide PNG images in CUI. As PNG format supports transparency, you can set the transparency for the images and hence the workaround to set the background color as 192,192,192 is not required.
If you have a BMP with specific background color (like 192,192,192) then “Bitmap.MakeTransparent” API call can convert passed color as Transparent. Refer below code which converts the BMP with 192,192,192 background color to Transparent PNG
using (Bitmap myBitmap = new Bitmap(@"C:\temp\transparent.bmp"))
{
    //assuming that first pixel will have back ground color
    Color backColor = myBitmap.GetPixel(0, 0);
    myBitmap.MakeTransparent(backColor);
    myBitmap.Save(@"C:\temp\transparent.png",
                    System.Drawing.Imaging.ImageFormat.Png);
}

## 评论

**内容**: Senthilkumar said...
Hi Virupaksha,
Currently we are using separate resource dlls for light and dark theme as mentioned in this link (Supporting AutoCAD 2015’s dark theme).
http://through-the-interface.typepad.com/through_the_interface/2014/04/supporting-autocad-2015s-dark-theme.html
For different themes, we are using different BMPs in resource dlls. As you mentioned in this article, we can make Transparent PNG. But, when we use PNGs in resource dlls, Ribbon is not able to load that image. Is there a way to load different PNGs for light and dark theme directly in CUIX file?
Reply
01/21/2016 at 11:06 PM

---
**内容**: Suhas Hayatnagarkar said...
Hi Virupaksha,
PNG images embedded in resource only dll are not able to load. Can you please send the sample of resourceonly dll that will help us using PNGs for AutoCAD menus and ribbons and toolbars.
We have a resource dll in the cuix path that works perfectly with BMPs.
Regards
Suhas Hayatnagarkar
Reply
02/16/2016 at 12:05 AM

---
**内容**: viru said in reply to Suhas Hayatnagarkar...
Hi
I have send the sample code. I will update this blog post soon (as soon as i clean the sample)
Viru
Reply
02/16/2016 at 12:23 AM

---
**内容**: Anuj said in reply to viru...
Hi Virupaksha,
I also have same problem as Suhas Hayatnagarkar has, my resource dll works fine with BMPs but when I try to use it with PNG files, it shows default icon(?).
Can you please share sample code with me as well?
Reply
03/31/2016 at 05:53 AM

---
**内容**: viru said in reply to Anuj...
Hi Anuj,
Please refer sample (contains project) http://adndevblog.typepad.com/autocad/2014/08/using-cuix-resource-dll-with-image-transparency.html. The sample is for Ico file, but this holds good for PNG too. so please use the same sample and replace the ico files with PNG file. sometime next week i will write separate blog on this...
thanks
Viru
Reply
03/31/2016 at 11:24 PM

---
**内容**: Anuj said in reply to viru...
Hi Viru,
It's working fine.
thanks a lot.
Reply
04/12/2016 at 01:34 AM

---
**内容**: Suhas Hayatnagarkar said...
Hi Virupaksha,
Following scenario of menu crashes AutoCAD when try to select the ribbon tab that contains drop-down. Please follow following steps (AutoCAD 2017)
1. Create a Row and add Drop-Down
2. Add few commands under drop-down
3. Drop-Down Behavior --> Drop Down Menu
4. SplitButtonListStyle --> IconText
5. ButtonStyle --> SmallWithText
6. Assign the resource ID that is using PNG image (Small or Large image) --> AutoCAD Crashes
The crash is with the combination of Behavior option and PNG resource ID (work perfectly with BMP Ids). You can use your sample that you shared with me earlier.
My old menus are failing.
Regards
Suhas
Reply
04/04/2016 at 12:48 AM

---
**内容**: Frabulator said in reply to Suhas Hayatnagarkar...
There is a third party software you could try called Cuix Tools. It was made to convert older cad cuix files to run in cad 2017.
http://www.graytechnical.com/software/cuixtools/
I hope that helps
Reply
04/13/2016 at 09:36 AM

---
