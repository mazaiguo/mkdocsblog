---
title: "Calculate extents of text with True Type fonts"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Unicode
description: "It is possible to manually obtain the extents of a AcDbText, which is shown below. This can be also used to get the space a text will occupy. This ..."
author: Autodesk
---
# Calculate extents of text with True Type fonts

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/calculate-extents-of-text-with-true-type-fonts.html

## 文章内容

By Augusto Goncalves
It is possible to manually obtain the extents of a AcDbText, which is shown below. This can be also used to get the space a text will occupy. This sample code uses a existing text style and call the extents method.
Acad::ErrorStatus getTTFTextGeomExtents(
                    AcDbText *pText,
                    AcDbExtents& extents)
{
  Acad::ErrorStatus es;
    if(!pText)
    return Acad::eInvalidInput;
    // Create an AcGiTextStyle based on the text's style.
  AcDbObjectId textStyleId=pText->textStyle();
  AcGiTextStyle *pTextStyle=new AcGiTextStyle;
  if((es=fromAcDbTextStyle(*pTextStyle,textStyleId))!=Acad::eOk)
    return es;
  pTextStyle->setTextSize(pText->height());
    // Get the 2d Extents of the text string
  // (using the applied style), and convert it to a 3d point.
  AcGePoint2d extentsPoint2d=pTextStyle->extents(
    pText->textString(),false,_tcslen(pText->textString()),
    false,NULL);
  AcGePoint3d extentsPointA(0,0,0),extentsPointB(
    extentsPoint2d[0],extentsPoint2d[1],0);
    // AcDbText::getEcs() returns an Identity matrix,
  // so we must create the transform matrix ourselves.
  AcGeMatrix3d coordSysMat;
  AcGeVector3d xAxis = pText->normal().perpVector();
  AcGeVector3d yAxis = pText->normal().crossProduct(xAxis);
  xAxis.rotateBy(pText->rotation(),pText->normal());
  yAxis.rotateBy(pText->rotation(),pText->normal());
  coordSysMat.setCoordSystem(pText->position(), xAxis,
    yAxis, pText->normal());
    // Use the matrix to transform our extents to WCS.
  extentsPointA.transformBy(coordSysMat);
  extentsPointB.transformBy(coordSysMat);
    extents.addPoint(extentsPointA);
  extents.addPoint(extentsPointB);
    delete pTextStyle;
  return Acad::eOk;
}

