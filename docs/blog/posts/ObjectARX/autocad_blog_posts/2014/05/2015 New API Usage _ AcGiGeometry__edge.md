---
title: "2015 New API Usage : AcGiGeometry::edge"
date: 2014-05-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Database
  - Hatch
  - Polyline
description: "In this blog post , I will illustrate a simple usage of our new AutoCAD2015 API AcGiGeometry::edge(const AcArray<AcGeCurve2d>& edges) this API esse..."
author: Autodesk
---
# 2015 New API Usage : AcGiGeometry::edge

发布日期: 2014-05-01

原始链接: https://adndevblog.typepad.com/autocad/2014/05/2015-new-api-usage-acgigeometryedge.html

## 文章内容

By Madhukar Moogala
In this blog post , I will illustrate a simple usage of our new AutoCAD2015 API AcGiGeometry::edge(const AcArray<AcGeCurve2d*>& edges) this API essentially defines a boundary of a fill ,can be used to display hatch – either pattern based , or solid hatches or gradients.
In my example ,I have created a custom entity deriving from AcDbPolyline and drawing a hatch in my graphics database, to define the boundary of my hatch. I have extracted line segments from my custom entity and passing those to edge API.
Code Snippet:
Adesk::Boolean ADSKMyEntity::subWorldDraw (AcGiWorldDraw *pWd)
{
assertReadEnabled () ;
/*Purpose is to diplay the hatch using new API AcGiGeometry::edge
on the my entity[ADSKMyEntity] deriving from polyline */
Adesk::Boolean result = Adesk::kFalse;
AcArray<AcGeCurve2d*> geCurves;
double hatchDev = 0.0;
hatchDev =
pWd->deviation(kAcGiMaxDevForCurve, AcGePoint3d::kOrigin);
AcGiFill acgiSolidFill;
acgiSolidFill.setDeviation(hatchDev);
int nSegs = -1;
AcGeLineSeg2d line;
AcGeLineSeg2d *pLine;
nSegs = this->numVerts() ;
for(int i = 0; i < nSegs; i++)
{
if(this->segType(i) == AcDbPolyline::kLine)
{
    this->getLineSegAt(i, line);
    pLine = new AcGeLineSeg2d(line);
    geCurves.append(pLine);
  }
}
  pWd->subEntityTraits().setFill(&acgiSolidFill);
/* geCurves represents boundary of hatch*/
result = pWd->geometry().edge(geCurves);
return result;
}
You can download full sample project ADSKEntity

