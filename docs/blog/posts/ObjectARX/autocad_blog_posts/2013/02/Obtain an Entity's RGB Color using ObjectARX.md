---
title: "Obtain an Entity's RGB Color using ObjectARX"
date: 2013-02-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Layer
  - ObjectARX
description: "Is there a way to get an entity's RGB color? The color() function returns an AcCmColor object. How do you get the RGB values from this?"
author: Autodesk
---
# Obtain an Entity's RGB Color using ObjectARX

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/obtain-an-entitys-rgb-color-using-objectarx.html

## 文章内容

by Fenton Webb
Issue
Is there a way to get an entity's RGB color? The color() function returns an AcCmColor object. How do you get the RGB values from this?
Solution
There are several ways colors can be applied to entities. If the entity is using the color index (ACI) then you can use acedGetRgb() to get RGB vaules. Below is an example that gets the color method and displays the RGB values for entities using ACI or True Color. If the entity was using byLayer then you would have to access the layer to get the color information.
static void ASDKwb_test(void)
{
  ads_name eName;
  ads_point pnt1;
  // select the entity to extract the color
  int res = acedEntSel(_T("\nselect an entity"), eName, pnt1);
  // if ok
  if (res == RTNORM)
  {
    AcDbObjectId oId;
    // convert the ename to an object id
    acdbGetObjectId(oId, eName);
    // open for read
    AcDbObjectPointer<AcDbEntity> pEnt(oId, AcDb::kForRead);
    // if ok
    if (pEnt.openStatus() == Acad::eOk)
    {
      // get the color
      AcCmColor color = pEnt->color();
        Adesk::UInt8 blue, green, red;
      Adesk::UInt16 ACIindex;
      long acirgb, r,g,b;
        // get the RGB value as an Adesk::Int32
      Adesk::Int32 nValue = color.color();
        // now extract the values
      AcCmEntityColor::ColorMethod cMethod;
      cMethod = color.colorMethod();
      switch(cMethod)
      {
      case AcCmEntityColor::kByColor :
        // now convert back to the original values, first 8 bits blue
        acutPrintf(_T("\nEntity using True Color"));
        blue = nValue;
        acutPrintf(_T("\nblue value = %i"), blue);
        // now move nValue right 8 bits, green
        nValue = nValue>>8;
        // now get the green
        green = nValue;
        acutPrintf(_T("\ngreen value = %i"), green);
        // move right to the next 8 bits red
        nValue = nValue>>8;
        red = nValue;
        acutPrintf(_T("\nred value = %i"), red);
        break;
          case AcCmEntityColor::kByACI :
        ACIindex = color.colorIndex();
        acutPrintf(_T("\nEntity using ACI, number: %i", ACIindex));
        acirgb = acedGetRGB ( ACIindex );
        r = ( acirgb & 0xffL );
        acutPrintf(_T("\nred value = %i"), r);
        g = ( acirgb & 0xff00L ) >> 8;
        acutPrintf(L"\ngreen value = %i"), g);
        b = acirgb >> 16;
        acutPrintf(L"\nblue value = %i"), b);
        break;
          case AcCmEntityColor::kByLayer :
        acutPrintf(_T("\nEntity Color is by layer"));
        break;
          default :
        acutPrintf(_T("\nEntity not using ACI, byLayer or ByColor"));
        break;
      }
    }
  }
}

## 评论

**内容**: James Wang said...
Hi, I have a question here.
When I change the background color from black to other colour, the RGB values change. For example, ACI 134 is (0,153,153) when the backgroud is black, but its RGB value become (0,127,127) when I change the background colour to blue. The code above always return RGB as (0, 153, 153). So how to get the actual RGB whatever the background colour?
Thanks in advance.
Reply
07/09/2013 at 01:36 AM

---
