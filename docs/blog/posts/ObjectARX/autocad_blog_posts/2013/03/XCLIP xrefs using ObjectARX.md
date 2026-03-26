---
title: "XCLIP xrefs using ObjectARX"
date: 2013-03-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - Block
  - C++
  - ObjectARX
  - XREF
description: "The AcDbSpatialFilter class was designed to do this. This class is used to define a spatial filter that AutoCAD uses to define the clip volume of t..."
author: Autodesk
---
# XCLIP xrefs using ObjectARX

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/xclip-xrefs-using-objectarx.html

## 文章内容

By Xiaodong Liang
The AcDbSpatialFilter class was designed to do this. This class is used to define a spatial filter that AutoCAD uses to define the clip volume of the block reference to the xref in the host drawing.
AutoCAD uses this spatial filter to decide what object IDs will be processed during regen.
The sample below is a small demo. Note: the commands needs to be defined with the options ACRX_CMD_NOINTERNALLOCK:
ACED_ARXCOMMAND_ENTRY_AUTO(CMyTestApp,
                           MyTestApp,
                           _MyClip, MyClip,
                           ACRX_CMD_TRANSPARENT |
                           ACRX_CMD_NOINTERNALLOCK, 
                           NULL)
     static void MyTestApp_MyClip()
{
    ads_point pt1,pt2;
    ads_name ent;
    if (acedEntSel(_T("Select xref:"),ent,pt1)!=RTNORM)
        return;
    AcDbObjectId idXref;
    if (acdbGetObjectId(idXref,ent)!=Acad::eOk)
        return;
    AcDbObjectPointer<AcDbBlockReference> pRef(idXref,AcDb::kForRead);
    if (pRef.openStatus()!=Acad::eOk)
    {
        acutPrintf(_T("Not an xref!\n"));
        return;
    }
    AcGePoint2dArray pts;
    if (acedGetPoint(NULL,_T("First point:"),pt1)!=RTNORM)
        return;
    //the ECS of the vertices must be defined in the
    //coordinate system of the _block_ so let's calculate
    //transform all points to that coordinate system
      AcGeMatrix3d mat(pRef->blockTransform());
    mat.invert();
      AcGePoint3d pt3d(asPnt3d(pt1));
    pt3d.transformBy(mat);
    pts.append(AcGePoint2d(pt3d.x,pt3d.y));
    while (acedGetPoint(pt1,_T("Next point:"),pt2)==RTNORM)
    {
        acedGrDraw(pt1,pt2,1,1);
        pt3d = asPnt3d(pt2);
        pt3d.transformBy(mat);
        pts.append(AcGePoint2d(pt3d.x,pt3d.y));
        memcpy(pt1,pt2,sizeof(ads_point));
    }
    acedRedraw(NULL,0);
    AcDbDatabase* pDb = acdbHostApplicationServices()->workingDatabase();
    AcGeVector3d normal;
    double elev;
    if (pDb->tilemode())
    {
        normal = pDb->ucsxdir().crossProduct(pDb->ucsydir());
        elev = pDb->elevation();
    }
    else
    {
        normal = pDb->pucsxdir().crossProduct(pDb->pucsydir());
        elev = pDb->pelevation();
    }
    normal.normalize();
    Acad::ErrorStatus es = pRef.object()->upgradeOpen();
    if (es !=Acad::eOk)
        return;
    //create the filter
    AcDbSpatialFilter* pFilter = new AcDbSpatialFilter;
    if (pFilter->setDefinition(pts,normal,elev,
        ACDB_INFINITE_XCLIP_DEPTH,-ACDB_INFINITE_XCLIP_DEPTH,true)!=Acad::eOk)
    {
        delete pFilter;
        return;
    }
    //add it to the extension dictionary of the block reference
    //the AcDbIndexFilterManger class provides convenient utility functions
    if (AcDbIndexFilterManager::addFilter(pRef.object(),pFilter)!=Acad::eOk)
        delete pFilter;
    else
    {
        acutPrintf(_T("Filter has been succesfully added!\n"));
        pFilter->close();
    }
  }

## 评论

**内容**: Steve said...
This post is helpful. How does ACAD manage an inside mode XCLIP vs a default outside mode XCLIP? Looking through the API, all I can think of is it's in how the spatial filter is created.
Reply
03/25/2013 at 06:33 AM

---
