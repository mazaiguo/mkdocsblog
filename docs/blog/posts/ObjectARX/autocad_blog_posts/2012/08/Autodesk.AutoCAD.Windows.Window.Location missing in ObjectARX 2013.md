---
title: "Autodesk.AutoCAD.Windows.Window.Location missing in ObjectARX 2013"
date: 2012-08-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "If you are using the code in this blog post from Kean's blog, you may find that "Autodesk.AutoCAD.Windows.Window" class no longer has the "Location..."
author: Autodesk
---
# Autodesk.AutoCAD.Windows.Window.Location missing in ObjectARX 2013

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/autodeskautocadwindowswindowlocation-missing-in-objectarx-2013.html

## 文章内容

By Balaji Ramamoorthy
If you are using the code in this blog post from Kean's blog, you may find that "Autodesk.AutoCAD.Windows.Window" class no longer has the "Location" property in the 2013 SDK. It has been replaced with "DeviceIndependentLocation" property. Similarly, the "Size" property has been replaced by the "DeviceIndependentSize" property.
Here is a sample code snippet that uses the "DeviceIndependentLocation" and "DeviceIndependentSize" to determine the location and size of the window :
Point pt = new Point(
                        (int)wd.DeviceIndependentLocation.X,
                        (int)wd.DeviceIndependentLocation.Y
                    );
  Size sz = new Size    (
                        (int)wd.DeviceIndependentSize.Width,
                        (int)wd.DeviceIndependentSize.Height
                    );
  System.Windows.Vector s =
    Autodesk.AutoCAD.Windows.Window.GetDeviceIndependentScale(IntPtr.Zero);
  pt = new Point    (
                    (int)(wd.DeviceIndependentLocation.X * s.X),
                    (int)(wd.DeviceIndependentLocation.Y * s.Y)
                );
  sz = new Size(
                (int)(wd.DeviceIndependentSize.Width * s.X),
                (int)(wd.DeviceIndependentSize.Height * s.Y)
             );

