---
title: "Render To Off-screen and SUN Enabling"
date: 2016-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - C++
description: "We will discuss few workarounds to tackle the problem with the creation of an off-screen View in .NET,"
author: Autodesk
---
# Render To Off-screen and SUN Enabling

发布日期: 2016-05-01

原始链接: https://adndevblog.typepad.com/autocad/2016/05/render-to-off-screen-and-sun-enabling.html

## 文章内容

By Madhukar Moogala
We will discuss few workarounds to tackle the problem with the creation of an off-screen View in .NET,
For C++ interested user, following comprehensive sample should help.
Problem 1:
The problem is that the off-screen view that I have to create looks as a "mirror" or "upside down" of the initial view that i want to render.
Workaround: Currently .NET API gives in-correct results, to work around the behaviour, use
 using (Bitmap bitmap = offscreenView.RenderToImage(mySettings, myRectangle))
                    {
                    if (File.Exists("D:\\Temp\\RenderTestImage.Jpg"))
                        File.Delete("D:\\Temp\\RenderTestImage.Jpg");
                    bitmap.RotateFlip(RotateFlipType.Rotate180FlipX);
                    bitmap.Save("D:\\Temp\\RenderTestImage.Jpg", System.Drawing.Imaging.ImageFormat.Jpeg);
                    }
  Problem 2:
How to enable the SUN for my off-screen view.
public void RND()
        {
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acDb = acDoc.Database;
        Editor ed = acDoc.Editor;
        /*Turn on SUN*/
     //   Application.SetSystemVariable("SUNSTATUS", 1);
        ViewportTableRecord vport = null;
        Sun sun = new Sun();
        sun.IsOn = true;
        using (Transaction acTrans = acDb.TransactionManager.StartTransaction())
            {
            vport = (ViewportTableRecord)acTrans.GetObject(acDoc.Editor.ActiveViewportId, OpenMode.ForWrite);
            vport.SetSun(sun);
            acTrans.Commit();
            }
        Autodesk.AutoCAD.Geometry.Point2d myScreenSize = (Point2d)Application.GetSystemVariable("screensize");
        double myWidth = myScreenSize.X;
        double myHeight = myScreenSize.Y;
        if (File.Exists("D:\\Temp\\RndImage.bmp"))
            File.Delete("D:\\Temp\\RndImage.bmp");
        ed.Command("_render", "", "render", myWidth.ToString(), myHeight.ToString(), "yes", "D:\\Temp\\RndImage.bmp");
        ed.Command("RENDERWINDOWCLOSE");
          }
  I have not used renderToImage API, as of now, when SUN is enabled, rendering on off-screen does not display the effects of Sun, hence above workaround is proposed now.

