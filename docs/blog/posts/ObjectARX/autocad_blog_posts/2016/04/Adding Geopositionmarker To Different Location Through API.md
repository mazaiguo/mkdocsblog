---
title: "Adding Geopositionmarker To Different Location Through API"
date: 2016-04-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Database
  - Plugin
description: "Recently, I have received a query from an ADN partner about positioning Geomaps on AutoCAD, you can add GeoLocationData to AutoCAD drawing, this ge..."
author: Autodesk
---
# Adding Geopositionmarker To Different Location Through API

发布日期: 2016-04-01

原始链接: https://adndevblog.typepad.com/autocad/2016/04/adding-geopositionmarker-to-different-location-through-api.html

## 文章内容

By Madhukar Moogala
Recently, I have received a query from an ADN partner about positioning Geomaps on AutoCAD, you can add GeoLocationData to AutoCAD drawing, this geolocation data is stored under Modelspace’s extension dictionary.
To can create programmatically GeoLocationData, please find this helpful blog.
In the current blog we ‘ll see how we can add new position marker to different place in the drawing with Geolocationdata.
At the end of code, I have uploaded a screencast, which shows moving from Autodesk’s Hyderabad Office to Autodesk’s Bangalore Office.
void addMarker(ads_point wcsPoint)
  {
  AcDbDatabase *pDb = acdbHostApplicationServices()->workingDatabase();
  if (pDb == NULL)
    return;
    AcGePoint3d pt(wcsPoint[0], wcsPoint[1], wcsPoint[2]);
  struct resbuf buf;
  double geoPositionMarkerRaidus = 0.0;
    if(acedGetVar(_T("GEOMARKPOSITIONSIZE"), &buf) == RTNORM)
    {
    geoPositionMarkerRaidus = buf.resval.rreal > 0 ?  buf.resval.rreal : 1.0;
    }
  double radius = geoPositionMarkerRaidus;
    AcDbSmartObjectPointer<AcDbGeoPositionMarker> pGeoPositionMarker;
  AcDbGeoPositionMarker *tmpMarker = new AcDbGeoPositionMarker(pt, radius, radius/2);
    pGeoPositionMarker.acquire(tmpMarker);
  if (eOkVerify(pGeoPositionMarker.openStatus()))
    {
    //set to current layer
    pGeoPositionMarker->setLayer( pDb->clayer() );
    AcDbObjectId modelSpaceId = acdbSymUtil()->blockModelSpaceId(pDb);
        {
      AcDbSmartObjectPointer<AcDbBlockTableRecord> modelSpaceBTR(modelSpaceId, AcDb::kForWrite);
      if (!eOkVerify(modelSpaceBTR.openStatus())) return ;
        //add position marker into db
      Acad::ErrorStatus es = Acad::eOk;
      AcDbObjectId newPositionMarkerId;
      es = modelSpaceBTR->appendAcDbEntity( newPositionMarkerId, pGeoPositionMarker);
      if (!eOkVerify(es))
        {
        return;
        }
      }
        }
  }
void InsertMarker()
  {
    CString prompt[2];
  prompt[0] = _T("Latitude");
  prompt[1] = _T("Longitude");
  CString keyword = _T("eXit");
  int limits[] = {90,180};
  double latLon[2];
  TCHAR result[133];
  int i=0;
  /*Get Lat and Long from user*/
  while(i<2)
    {
    if(RTERROR == acedInitGet(RSG_OTHER, keyword))
      {   
      assert(false);
      return;
      }
    int status = acedGetKword(prompt[i], result);
    if(status  == RTNORM)
      {
      double radian;
    if(_tcsicmp(_T(/*MSG0*/"eXit"), result) == 0)
      {
      return;
      }
    else if(acdbRawAngToF(result, 0, &radian) == RTNORM)
      {
      double degree = 180*radian/M_PI;
        if(fabs(degree) > limits[i])
        {
        acutPrintf(_T("\nInvalidInput"));
        }
      else
        {
        latLon[i] = degree;
        i++;
        }
      }
    else
      {
      acutPrintf(_T("\nInvalidInput"));
      }
      }
    else
      {
      return;
      }
    }
  AcDbObjectId geoDataId;
  if(eOkTest(acdbGetGeoDataObjId(acdbHostApplicationServices()->workingDatabase(), geoDataId)))
    {
    AcDbSmartObjectPointer<AcDbGeoData> pGeoData(geoDataId, AcDb::kForRead);
    if(eOkTest(pGeoData.openStatus()))
      {
      AcGePoint3d location;
      if(eOkTest(pGeoData->transformFromLonLatAlt(latLon[1], latLon[0], 0, location.x, location.y, location.z)))
        {
        addMarker(asDblArray(location));
        return;
        }
      }
    }
  }

## 评论

**内容**: hamza said...
Very good it is powerful
////////////
thank you
Reply
05/14/2016 at 03:19 AM

---
**内容**: hamza said...
Very good it is powerful
//////////////
thank you
Reply
05/14/2016 at 03:20 AM

---
