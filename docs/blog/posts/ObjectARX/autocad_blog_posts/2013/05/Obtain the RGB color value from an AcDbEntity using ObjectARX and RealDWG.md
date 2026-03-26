---
title: "Obtain the RGB color value from an AcDbEntity using ObjectARX and RealDWG"
date: 2013-05-01
categories:
  - AutoCAD C++
tags:
  - C++
  - DWG
  - ObjectARX
description: "Here’s how to obtain the RGB value from an already AcDb::kOpenForRead AcDbEntity."
author: Autodesk
---
# Obtain the RGB color value from an AcDbEntity using ObjectARX and RealDWG

发布日期: 2013-05-01

原始链接: https://adndevblog.typepad.com/autocad/2013/05/obtain-the-rgb-color-value-from-an-acdbentity-using-objectarx-and-realdwg.html

## 文章内容

by Fenton Webb
Here’s how to obtain the RGB value from an already AcDb::kOpenForRead AcDbEntity.
static COLORREF GetRGBFromEntity( AcDbEntity *ent )
{
  COLORREF colorRef = RGB(255, 255, 255);
  AcCmColor Color = ent->color();
  AcCmEntityColor::ColorMethod ColorMethod = Color.colorMethod();
    switch(ColorMethod)
  {
  case AcCmEntityColor::kByACI:
    {         
      long acirgb, r,g,b;
      acirgb = AcCmEntityColor::lookUpRGB(Color.colorIndex());
        b = ( acirgb & 0xff00L );
      g = ( acirgb & 0xff00L ) >> 8;
      r = acirgb >> 16;
        colorRef = RGB( r, g, b); 
      break;
      }
  }
  return colorRef;
}

