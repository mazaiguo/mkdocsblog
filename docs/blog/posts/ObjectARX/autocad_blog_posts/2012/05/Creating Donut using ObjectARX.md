---
title: "Creating Donut using ObjectARX"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Polyline
  - Unicode
description: "In AutoCAD we have the "DONUT" command, however there is no such entity as a donut. A donut is simply a LWPOLYLINE (AcDbPolyline) with two segments..."
author: Autodesk
---
# Creating Donut using ObjectARX

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/creating-donut-using-objectarx.html

## 文章内容

By Balaji Ramamoorthy
In AutoCAD we have the "DONUT" command, however there is no such entity as a donut. A donut is simply a LWPOLYLINE (AcDbPolyline) with two segments. Each segment has a bulge of 1.0 and the start point of one segment is the end point of the other segment. In addition the AcDbPolyline will have with and is also a close polyline. The following code fragment demonstrates a single 'donut', please note error checking is minimal: Note the arguments to 'addVertextAt()' which are the index, vertex location, bulge factor, starting width and ending width.
static void ADSProjectDonut(void)
{
    // Using fixed values to simplify the code sample.
    // Accept input for these values if required.
    ads_real innerDiameter = 5.0;
    ads_real outerDiameter = 15.0;
    AcGePoint2d centerPoint(20.0, 20.0);
      // Donut thickness
    double width = (outerDiameter - innerDiameter) / 2.0;
      // Start point of the polyline
    AcGePoint2d sp
        = centerPoint -
          AcGeVector2d::kXAxis * (innerDiameter + width) / 2.0;
      // End point of the polyline
    AcGePoint2d ep
        = centerPoint +
          AcGeVector2d::kXAxis * (innerDiameter + width) / 2.0;
      AcDbDatabase *pDb
        = acdbHostApplicationServices()->workingDatabase();
      AcDbBlockTableRecordPointer pMS
                    (
                        acdbSymUtil()->blockModelSpaceId(pDb),
                        AcDb::kForWrite
                    );
      AcDbPolyline *pDNut = new AcDbPolyline();
      double bulge = 1.0;
    Acad::ErrorStatus es;
    es = pDNut->addVertexAt(0, sp, bulge, width, width);
    es = pDNut->addVertexAt(1, ep, bulge, width, width);
    pDNut->setClosed(Adesk::kTrue);
      es = pMS->appendAcDbEntity(pDNut);
    if(es != Acad::eOk)
    {
        delete pDNut;
    }
    pDNut->close();
}

