---
title: "Positioning GeographicMarker Using ObjectARX"
date: 2016-04-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
  - Dimension
  - ObjectARX
  - Surface
description: "In addition to previous blog post we saw how we can add a GeoPositionMarker to a drawing with already GeographicMarker enabled."
author: Autodesk
---
# Positioning GeographicMarker Using ObjectARX

发布日期: 2016-04-01

原始链接: https://adndevblog.typepad.com/autocad/2016/04/positioning-geographicmarker-using-objectarxx.html

## 文章内容

By Madhukar Moogala
In addition to previous blog post we saw how we can add a GeoPositionMarker to a drawing with already GeographicMarker enabled.
In current blog we will see how we can leverage ObjectARX API to create GeoCoordinate system and place it in the drawing with user defined Latitudes and Longtitudes.
For this sample, I’m creating an UTM84-43N GIS coordinate system, Universal Transverse Mercator is not a single map projection, but divided in to sixty zones.
Here is an excerpt from Wikipedia about UTM.
The Universal Transverse Mercator (UTM) conformal projection uses a 2-dimensional Cartesian coordinate system to give locations on the surface of the Earth. Like the traditional method of latitude and longitude, it is ahorizontal position representation, i.e. it is used to identify locations on the Earth independently of vertical position. However, it differs from that method in several respects.
The UTM system is not a single map projection. The system instead divides the Earth into sixty zones, each being a six-degree band of longitude, and uses a secant transverse Mercator projection in each zone.
I’m using Latitude and Longitude values of our Autodesk’ Hyderabad office. : 17.434586,78.384402
Thanks to Tat-Lee for helping with suggestion while I was struggling to generate a Live map programmatically.
Do make note :
AcGePoint3d is expected to be (long, lat) and not (lat, long)
Reference point is in the coordinates of the projected coordinate system and not in geodetic.
Design point is in model-space coordinates
C++ code:
void GeographicLocationMarker( )
{
      /*Map Projection type*/
    const AcString csId(L"UTM84-43N");
  /*Creating the projected Coordinate Sytem */
  Acad::ErrorStatus es;
    AcDbGeoCoordinateSystem* pGeoCS;
    AcDbGeoCoordinateSystem::create(csId, pGeoCS);
     if (NULL == pGeoCS)
        return;
     AcString xmlStr;
   /*Get XML type*/
   es = pGeoCS->getXmlRepresentation(xmlStr);
  /*Checking the output of CRS*/
  acutPrintf(_T("\ncrsName: %s"),xmlStr.kACharPtr());
      if(xmlStr.isEmpty()) return;
      AcDbObjectId geoId;
    AcDbObjectPointer<AcDbGeoData> pGeoData;
    AcDbDatabase* pDb = acdbHostApplicationServices()->workingDatabase();
    acdbGetGeoDataObjId(pDb, geoId);
    /*Post our Geodata to Database,
  AcDbGeoData is not an Entity, it is stored in Model-Space's Extension Dictionary*/
    if (geoId.isNull())
    {
        pGeoData.create();
        pGeoData->setBlockTableRecordId(acdbSymUtil()->blockModelSpaceId(pDb));
        pGeoData->postToDb(geoId);
    }
    else
    {
        pGeoData.open(geoId, AcDb::kForWrite);
    }
      if (NULL == pGeoData.object())
        return;
  /* The spatial coordinate system string.
  It can be the id of the coordinate system or the XML/WKT representation*/
     es = pGeoData->setCoordinateSystem(xmlStr);
  /* The design coordinate system is considered to be local, aka
     an engineering coordinate system.*/
  es = pGeoData->setCoordinateType(AcDbGeoData::kCoordTypLocal);
    es = pGeoData->setHorizontalUnits(AcDb::kUnitsMillimeters);
    es = pGeoData->setVerticalUnits(AcDb::kUnitsMillimeters);
    es = pGeoData->setDesignPoint(AcGePoint3d::kOrigin);
    es = pGeoData->setUpDirection(AcGeVector3d::kZAxis);
    /*Lat and Long of Hyderabad : 17.434586,78.384402*/
  /*Note: AcGePoint3d expected to be Long,Lat,alt*/
  AcGePoint3d refPtInUTM84, refPtInLatLong(78.384402,17.434586,0.0);
    /*Get WCS point*/
  pGeoData->transformFromLonLatAlt(refPtInLatLong,refPtInUTM84);
  pGeoData->setReferencePoint(refPtInUTM84);
  pGeoData->setNorthDirectionVector(AcGeVector2d::kYAxis);
        /*clean up*/
    delete pGeoCS;
    pGeoData.close();
      }
  After the code,  turn on GEOMAP from ribbon or command, set type to Aerial view.
If you find difficult in loading Maps, make sure if you have logged in A360.
Here are few troubleshooting tips to generate Maps perfectly.
Log out of A360.
Quit AutoCAD.
Right-click the Autodesk 360 icon in the Windows system tray and choose  Exit.
Run  Windows Task manager and terminate the processes AcSettingsSync.exe and AdSync.exe if they are running.
Open a Windows File Explorer window and navigate to the following folder:
%localappdata%\Autodesk
Note: You can also paste "%localappdata%" into the address bar of a Windows File Explorer.
Delete the folder C:\Users\....\AppData\Local\Autodesk\Web Services.
Restart AutoCAD.

