---
title: "Setting polygonal clip boundary for a raster image"
date: 2012-09-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Polyline
description: "Here is a sample ObjectARX code to set the clip boundary of a raster image based on a selected polyline."
author: Autodesk
---
# Setting polygonal clip boundary for a raster image

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/setting-polygonal-clip-boundary-for-a-raster-image.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample ObjectARX code to set the clip boundary of a raster image based on a selected polyline.
// Select a closed polyline that defines the clip boundary
ads_name name2;
ads_point pt2;
  int nReturn = acedEntSel(_T("\nSelect a closed polyline\n"), name2, pt2);
  if(nReturn != RTNORM)
    return;
  //get the object Id of the entity
AcDbObjectId Id2;
if(acdbGetObjectId(Id2, name2) != Acad::eOk)
    return;
  //open the selected entity
AcDbEntity *pEntity2 = NULL;
if(acdbOpenAcDbEntity(pEntity2, Id2, AcDb::kForRead) != Acad::eOk)
    return;
  AcDbPolyline *pPline = AcDbPolyline::cast(pEntity2);
if(pPline == NULL)
    return;
    AcDbExtents exts;
pPline->bounds(exts);
AcGePoint3d minPt = exts.minPoint();
AcGePoint3d maxPt = exts.maxPoint();
AcGeVector3d vecx = (maxPt.x - minPt.x) * AcGeVector3d::kXAxis;
AcGeVector3d vecy = (maxPt.y - minPt.y) * AcGeVector3d::kYAxis;
  AcGePoint2dArray ptRect;
int numVerts = pPline->numVerts();
for(int i = 0; i < numVerts; i++)
{
    AcGePoint2d pt;
    pPline->getPointAt(i, pt);
    ptRect.append( pt);
}
AcGePoint2d ptBase( ptRect[0] );
ptRect.append( ptBase );
  // Select a raster image
ads_name name1;
ads_point pt3;
  nReturn = acedEntSel(_T("\nSelect a raster image\n"), name1, pt3);
  if(nReturn != RTNORM)
    return;
  //get the object Id of the entity
AcDbObjectId Id1;
if(acdbGetObjectId(Id1, name1) != Acad::eOk)
    return;
  //open the selected entity
AcDbEntity *pEntity1 = NULL;
if(acdbOpenAcDbEntity(pEntity1, Id1, AcDb::kForWrite) != Acad::eOk)
    return;
  AcDbRasterImage *pImage = AcDbRasterImage::cast(pEntity1);
if(pImage == NULL)
    return;
  // Set the clip boundary of the raster image
AcGeMatrix3d mat;
pImage->getPixelToModelTransform(mat);
mat = mat.inverse();
  for(int i=0;i < ptRect.length();i++ )
{
        AcGePoint3d pt = AcGePoint3d( ptRect[i].x, ptRect[i].y,0.0 );
        pt = mat*pt;     
        ptRect.setAt(i, AcGePoint2d(pt.x, pt.y));
}
  pImage->setClipBoundary( AcDbRasterImage::kPoly, ptRect );
pImage->setDisplayOpt( AcDbRasterImage::kShow, Adesk::kTrue );
pImage->setDisplayOpt( AcDbRasterImage::kClip, Adesk::kTrue );
pImage->setDisplayOpt( AcDbRasterImage::kShowUnAligned, Adesk::kTrue );
pImage->setDisplayOpt( AcDbRasterImage::kTransparent, Adesk::kTrue );
pImage->close();

