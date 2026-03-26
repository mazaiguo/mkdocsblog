---
title: "Color translation between RGB and AutoCAD ACI using ObjectARX"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "Translating an RGB color to the nearest equivalent AutoCAD Color Index (ACI) can be done by using the "loopUpACI" and "lookUpRGB" methods implement..."
author: Autodesk
---
# Color translation between RGB and AutoCAD ACI using ObjectARX

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/color-translation-between-rgb-and-autocad-aci-using-objectarx.html

## 文章内容

By Balaji Ramamoorthy
Translating an RGB color to the nearest equivalent AutoCAD Color Index (ACI) can be done by using the "loopUpACI" and "lookUpRGB" methods implemented in 'AcCmEntityColor '.
The following examples uses the lookUpRGB() to convert the ACI value 47 to get the corresponding RGB values and using the same RGB values to get the ACI using lookUpACI() function
Here is the sample code :
AcCmEntityColor cEntityColor;
  Adesk::UInt8 iIndex = 47;
  // Get the RGB equivalent of the ACI
Adesk::UInt32 nValue = cEntityColor.lookUpRGB(iIndex);
  Adesk::UInt8 blue, green, red;
  // now convert back to the original values, first 8 bits blue 
blue = nValue;
  // now move nValue right 8 bits, green
nValue = nValue >> 8;
// now get the green
green = nValue;
  // move right to the next 8 bits
nValue = nValue >> 8;
// now get the red
red = nValue;
  AcCmColor cColor;
cColor.setRGB(red, green, blue);
  // Get the ACI equivalent of the RGB
Adesk::UInt8 aci = AcCmEntityColor::lookUpACI(
                                                cColor.red(),
                                                cColor.green(),
                                                cColor.blue()
                                             );

## 评论

**内容**: Peter Wu said...
Is it possible to expose the code that does lookUpACI? I tried different ways and cannot get close to what this function does...
Reply
07/30/2014 at 05:57 PM

---
