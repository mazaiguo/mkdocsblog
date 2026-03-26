---
title: "Translating between drawing point and geographic location using ObjectARX"
date: 2015-02-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C++
  - Database
  - ObjectARX
description: "Here is a code snippet to convert drawing point to a geo-location and vice-versa in a geo-located drawing. If you are looking for a .Net code sampl..."
author: Autodesk
---
# Translating between drawing point and geographic location using ObjectARX

发布日期: 2015-02-01

原始链接: https://adndevblog.typepad.com/autocad/2015/02/translating-between-drawing-point-and-geographic-location-using-objectarx.html

## 文章内容

By Balaji Ramamoorthy
Here is a code snippet to convert drawing point to a geo-location and vice-versa in a geo-located drawing. If you are looking for a .Net code sample, please refer to this blog post.
 Acad::ErrorStatus es;
   AcDbDatabase *pDb = 
 acdbHostApplicationServices()->workingDatabase();
   AcDbObjectId geodataId = AcDbObjectId::kNull;
 acdbGetGeoDataObjId(pDb, geodataId);
   if (geodataId.isNull() == Adesk::kFalse)
 {
     AcDbTransactionManager *pTM 
                     = pDb->transactionManager();
    AcTransaction *pTransaction 
                         = pTM->startTransaction(); 
      AcDbObject *pObj = NULL;
  pTransaction->getObject(pObj, 
                             geodataId, 
                             AcDb::kForRead);
    AcDbGeoData *pGeoData = AcDbGeoData::cast(pObj);
  if (pGeoData != NULL)
  {
      pGeoData->upgradeOpen();
           // convert from drawing point to Geolocation 
         AcGePoint3d geoPoint(dblLongitude, 
                              dblLatitude, 
                              dblAltitude);
           AcGePoint3d drawingPt = AcGePoint3d::kOrigin; 
         es = pGeoData->transformFromLonLatAlt(
                             geoPoint, drawingPt);
           // convert from Geolocation to drawing point 
         es = pGeoData->transformToLonLatAlt(
                 dblDwgX, dblDwgY, dblDwgZ, 
                 dblLongitude, dblLatitude, dblAltitude);
     pTM->endTransaction();
  }
  else 
   pTM->abortTransaction();
 }

## 评论

**内容**: sandesh said...
Thanks for posting this code. I was just looking for some training material like this.
Reply
02/11/2015 at 08:25 PM

---
**内容**: Neyton Luiz Dalle Molle said...
Hi,
I'm a Civil 3D user and I'm trying to implement this code to convert local coordinates (x,y) to UTM grid coordinates (north, east):
Dim gd As GeoLocationData = DB.GeoDataObject.GetObject(OpenMode.ForRead)
Dim m As Matrix3d = Matrix3d.Displacement(gd.DesignPoint.GetVectorTo(gd.ReferencePoint))
m = m * Matrix3d.Rotation(gd.NorthDirection, gd.UpDirection, gd.DesignPoint)
m = m * Matrix3d.Scaling(gd.ScaleFactor, gd.DesignPoint)
Dim ptUTM as Point3d = ptLOCAL.TransformBy(m)
But, gd.ScaleFactor always return 1, even if gd.ScaleEstimationMethod = ScaleEstimationMethod.ScaleEstMethodReferencePoint
Note: Civil 3D return correct value:
Autodesk.Civil.ApplicationServices.CivilApplication.ActiveDocument.Settings.DrawingSettings.TransformationSettings.GridScaleFactor
What is wrong? Did I miss something?
Reply
09/26/2015 at 05:24 AM

---
