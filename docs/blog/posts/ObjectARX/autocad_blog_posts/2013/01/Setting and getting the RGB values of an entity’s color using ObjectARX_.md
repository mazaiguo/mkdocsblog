---
title: "Setting and getting the RGB values of an entity’s color using ObjectARX?"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "The key to setting the color of an entity using an RGB value is to specify the “color method” explicitly."
author: Autodesk
---
# Setting and getting the RGB values of an entity’s color using ObjectARX?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/setting-and-getting-the-rgb-values-of-an-entitys-color-using-objectarx.html

## 文章内容

By Gopinath Taget
The key to setting the color of an entity using an RGB value is to specify the “color method” explicitly.
Here's some code which shows how to get and set the color RGB values. Notice, in the second part of the function, before setting the nValue value, we call the setColorMethod() method on AcCmColor object.
void asdkGetColor()
{
Adesk::UInt8 blue, green, red;
  AcCmColor colors;
 // set the color method
Acad::ErrorStatus es =
  colors.setColorMethod(AcCmEntityColor::kByColor);
 // ok, lets try and set the color using setRGB and setColor
es = colors.setRGB(3, 2, 1); // nValue is an RGB value
   // get the RGB value as an Adesk::Int32
Adesk::Int32 nValue = colors.color();
   // now convert back to the original values, first 8 bits blue
blue = nValue;
 // now move nValue right 8 bits, green
nValue = nValue>>8;
 // now get ﻿﻿the green
green = nValue;
 // move right to the ﻿﻿next 8 bits red
nValue = nValue>>8;
red = nValue;
   // should be red = 3, green = 2, blue = 1 :-)
  {
  // lets try the other way
  AcCmColor colors;
  Acad::ErrorStatus es =
   colors.setColorMethod(AcCmEntityColor::kByColor);
  // simply get the value with no colours
  // set, only the color method bits
  Adesk::Int32 nValue = colors.color();
    // now set up the colours from our previous values
  Adesk::Int8 *ptr =
   reinterpret_cast<Adesk::Int8 *> (&nValue);
  // now reconstruct
  *(ptr)   = blue;
  *(ptr+1) = green;
  *(ptr+2) = red;
    // now we can try setColor
  es = colors.setColor(nValue);
}
 // all works
}

## 评论

**内容**: Owen Wengerd said...
Is there some reason why your sample avoids the use of AcCmColor::setRGB() or other member functions intended to set color values?
Reply
01/15/2013 at 07:10 PM

---
**内容**: Gopinath Taget said...
Hi Owen,
We do show the usage of setRGB in the code above along with the setColor method.
Cheers
Gopinath
Reply
01/16/2013 at 08:42 PM

---
**内容**: Owen Wengerd said in reply to Gopinath Taget...
I see. I think the call to setRGB() sets the color method to byColor, so the prior call to setColorMethod() is not needed.
Reply
01/16/2013 at 10:12 PM

---
**内容**: Veli Väisänen said...
Just update that AcCmColor::setColorMethod is deprecated on ObjectARX 2021.
Reply
10/14/2020 at 03:42 AM

---
