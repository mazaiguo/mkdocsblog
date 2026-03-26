---
title: "Attaching geo-location data using ObjectARX"
date: 2015-02-01
categories:
  - AutoCAD .NET
tags:
  - C++
  - ObjectARX
description: "Here is a code snippet to create geo-location data in an AutoCAD drawing. If you are looking for a .Net code sample, please refer to this blog post."
author: Autodesk
---
# Attaching geo-location data using ObjectARX

发布日期: 2015-02-01

原始链接: https://adndevblog.typepad.com/autocad/2015/02/attaching-geo-location-data-using-objectarx.html

## 文章内容

By Balaji Ramamoorthy
Here is a code snippet to create geo-location data in an AutoCAD drawing. If you are looking for a .Net code sample, please refer to this blog post.
To try this code, you will need to be signed-in using Autodesk 360 login credentials inside AutoCAD.
 AcDbDatabase *pDb 
     = acdbHostApplicationServices()->workingDatabase();
   AcDbBlockTable *pBlockTable;
 pDb->getSymbolTable(pBlockTable, AcDb::kForRead);
   AcDbObjectId msId = AcDbObjectId::kNull;
 pBlockTable->getAt(ACDB_MODEL_SPACE, msId);
 pBlockTable->close();
   AcDbGeoData *pGeoData = new  AcDbGeoData();
 pGeoData->setBlockTableRecordId(msId);
 AcDbObjectId geodataId = AcDbObjectId::kNull;
 pGeoData->postToDb(geodataId);
   //coordinate system 
 pGeoData->setCoordinateSystem(ACRX_T("WORLD-MERCATOR" ));
 pGeoData->setCoordinateType(AcDbGeoData::kCoordTypGrid);
   //Get the model space point for  
 // LATITUDE = 37.8109 & LONGITUDE = -122.4776 
 AcGePoint3d geoPoint(-122.4776, 37.8109, 0);
 AcGePoint3d drawingPt = AcGePoint3d::kOrigin; 
 pGeoData->transformFromLonLatAlt(geoPoint, drawingPt);
 pGeoData->setHorizontalUnits(AcDb::UnitsValue::kUnitsMeters);
 pGeoData->setVerticalUnits(AcDb::UnitsValue::kUnitsMeters);
   //set the model space point; 
 pGeoData->setDesignPoint(drawingPt);
   //set the geo point. 
 pGeoData->setReferencePoint(geoPoint);
 pGeoData->close();
   AcApDocument *pDoc = acDocManager->document(
            acdbHostApplicationServices()->workingDatabase());
   ACHAR zoomWcommand[200];
 AcGePoint3d pt1 = drawingPt + AcGeVector3d(-5000.0, 5000.0, 0.0);
 AcGePoint3d pt2 = drawingPt + AcGeVector3d(5000.0, -5000.0, 0.0);
   acutSPrintf(zoomWcommand, 
 ACRX_T("_.Zoom W %lf,%lf %lf,%lf " ), pt1.x, pt1.y, pt2.x, pt2.y); 
   acDocManager->sendStringToExecute(pDoc, zoomWcommand, 
                                   false , true , false ); 
 acDocManager->sendStringToExecute(pDoc, 
                 L"_geomap Road " , 
                 false , true , false );
  The Latitude and longitude values in the code snippet are for geo-locating the drawing origin to the Golden Gate bridge.
Here is a screenshot :

