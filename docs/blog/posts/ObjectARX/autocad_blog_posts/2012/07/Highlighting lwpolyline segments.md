---
title: "Highlighting lwpolyline segments"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Plot
  - Polyline
  - Selection
description: "Here is a sample ObjectARX code to highlight / unhighlight polyline segments. The GS marker of the selected segment is determined and the "getSuben..."
author: Autodesk
---
# Highlighting lwpolyline segments

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/highlighting-lwpolyline-segments.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample ObjectARX code to highlight / unhighlight polyline segments. The GS marker of the selected segment is determined and the "getSubentPathsAtGsMarker" is used to obtain the sub entity path. Using the sub entity path, the selected segment is then highlighted.
AcDbObjectId objId;
int marker;
  ads_name sset;
if(RTNORM != acedSSGet(L"_:S", NULL, NULL, NULL, sset))
{
    acutPrintf(L"\nSelection failed :(");
    return;
}
  resbuf *rb = NULL;
if (RTNORM != acedSSNameX(&rb, sset, 0))
{
    acedSSFree(sset);
    return;
}
  struct resbuf *pTemp;
int i;
for (i=1, pTemp = rb;i<3;i++, pTemp = pTemp->rbnext)
    { ; }
  ads_name ename;
ads_name_set(pTemp->resval.rlname, ename);
  // Move on to the 4th list element which is the GsMarker
//
pTemp = pTemp->rbnext;
marker = pTemp->resval.rint;
  acutRelRb(rb);
  Acad::ErrorStatus es;
  es = acdbGetObjectId(objId, ename);
if(es != Acad::eOk)
    return;
  AcDbEntity *pEnt;
es = acdbOpenAcDbEntity(pEnt, objId, AcDb::kForRead);
if(es != Acad::eOk)
    return;
  // Get the subentity ID for the edge picked
//
AcGePoint3d pickpnt;
AcGeMatrix3d xform;
int numIds;
AcDbFullSubentPath *subentIds;
es = pEnt->getSubentPathsAtGsMarker(
                                        AcDb::kEdgeSubentType,
                                        marker,
                                        pickpnt,
                                        xform,
                                        numIds,
                                        subentIds
                                    );
if(es != Acad::eOk)
    return;
  // At this point the subentIds variable contains the
// address of an array of AcDbFullSubentPath objects.
// The array should be one element long, so the picked
  // edge's AcDbFullSubentPath is in subentIds[0]
  // For objects with no edges (such as a sphere) the
// code to highlight an edge is meaningless and must
// be skipped.
//
if (numIds > 0)
{
    // Highlight the picked edge.
    pEnt->highlight(subentIds[0]);
    // OR
    // Unhighlight the picked edge.
    //pEnt->unhighlight(subentIds[0]);
  }
delete []subentIds;
  pEnt->close();

