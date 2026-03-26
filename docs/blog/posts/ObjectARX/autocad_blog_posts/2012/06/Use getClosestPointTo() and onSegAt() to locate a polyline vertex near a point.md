---
title: "Use getClosestPointTo() and onSegAt() to locate a polyline vertex near a point"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Polyline
description: "You can use getClosestPointTo() and onSegAt() to find a vertex of a polyline closest to a selected point. Here is an ObjectARX example that shows t..."
author: Autodesk
---
# Use getClosestPointTo() and onSegAt() to locate a polyline vertex near a point

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/use-getclosestpointto-and-onsegat-to-locate-a-polyline-vertex-near-a-point.html

## 文章内容

By Wayne Brill
You can use getClosestPointTo() and onSegAt() to find a vertex of a polyline closest to a selected point. Here is an ObjectARX example that shows this idea. To try this run a command that runs this function. If you select a polyline the command line will display the number of the segment of the polyline (where you selected the polyline).
 static void TEST_PointOnPoly(void)
{
    ads_name ename;
  ads_point pt, ptWcs;
  AcDbObjectId Id;
    if(acedEntSel(_T("Select Pline: "),
                      ename,pt)!=RTNORM)
   return;
    // Convert to WCS incase selection was made
  // while in a UCS.
  acdbUcs2Wcs(pt, ptWcs, Adesk::kFalse);
  acdbGetObjectId(Id,ename);
  AcDbEntity* pEnt;
  acdbOpenObject(pEnt,Id,AcDb::kForRead,false);
    AcDbPolyline* pLine=NULL;
  pLine=AcDbPolyline::cast(pEnt);
    if(!pLine)
  {
   acutPrintf(_T
    ("Selected Entity not a Polyline"));
   pEnt->close();
   return;
  }
    AcGePoint3d clickpt;
  // This will convert the pick point to a
  // point on the polyline
  pLine->getClosestPointTo(asPnt3d(ptWcs), clickpt);
  // Convert to 2d point, needed below...
  AcGePoint2d clickpt2d(clickpt.x, clickpt.y);
    for(unsigned int c=0; pLine->numVerts() > c ; c++)
  {
   double segParam;
   // This is the test filter here...it uses the
   // nifty API onSegAt
   if(pLine->onSegAt(c, clickpt2d, segParam)) 
   {
    acutPrintf(_T("Selected Segment: %d \n"),c+1);
    break;
   }
  }
  pLine->close();
}

