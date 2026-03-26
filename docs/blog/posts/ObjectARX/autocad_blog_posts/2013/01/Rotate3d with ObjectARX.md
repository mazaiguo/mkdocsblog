---
title: "Rotate3d with ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "We suggest two possibilities to use ROTATE3D in an ARX program: call the build-in command or implement using transformBy."
author: Autodesk
---
# Rotate3d with ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/rotate3d-with-objectarx.html

## 文章内容

By Augusto Goncalves
We suggest two possibilities to use ROTATE3D in an ARX program: call the build-in command or implement using transformBy.
Method #1
Call the AutoCAD ROTATE3D command using acedInvoke(). As ROTATE3D is located in geom3d.arx in AutoCAD, and is registered with acedDefun, we cannot use acedCommand, but must use acedInvoke. In addition, you have to make sure that the geom3d module is loaded and your function which calls acedInvoke() is registered with acedDefun() and not with acedRegCmds->addCommand().
The following is sample code:
int testfunc()
{
  // make sure that geom3d.arx is loaded
  acedArxLoad(_T("geom3d.arx"));
  ads_name pieces;
  ads_point Point1, Point2;
  Point1[X] =  1.0;
  Point1[Y] =  1.0;
  Point1[Z] =  0.0;
  Point1[X] = 10.0;
  Point1[Y] = 10.0;
  Point1[Z] = 10.0;
  ads_real  Angle = 32;
    //Select the entities you want to rotate
  acedSSGet( NULL,NULL, NULL, NULL, pieces );
    resbuf* pBuf = acutBuildList(RTSTR,_T("c:rotate3d"),
    RTPICKS, pieces, RTSTR, _T(""), RT3DPOINT, Point1,
    RT3DPOINT, Point2, RTREAL, Angle, RTNONE);
    resbuf* result=NULL;
  acedInvoke(pBuf,&result);
  acutRelRb(pBuf);
  if (result!=NULL)
    acutRelRb(result);
    return RTNORM;
}
Method #2
With ObjectARX, it is recommended that AcDbEntity::transformBy() is used instead of invoking ROTATE3D. For example, for each entity (ename) with AcGePoint3d start (start) and end (end) points for the axis, and the rotation angle (angle), you can perform the following:
  double pi =  3.14159265359;
  AcDbObjectId objId;
  acdbGetObjectId(objId, ename); 
  AcDbEntity* pEnt = NULL;
  acdbOpenAcDbEntity(pEnt, objId, AcDb::kForWrite); 
  AcGeMatrix3d mat;
  mat.setToRotation(angle * pi / 180, end - start, start);
  pEnt->transformBy(mat);
  pEnt->close();

