---
title: "Finding the entities that intersect a polyline"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plot
  - Polyline
  - Selection
description: "To find the entities that intersect a selected polyline (LWPOLYLINE in this case), use a selection set containing the entities that cross the polyl..."
author: Autodesk
---
# Finding the entities that intersect a polyline

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/finding-the-entities-that-intersect-a-polyline.html

## 文章内容

By Gopinath Taget
To find the entities that intersect a selected polyline (LWPOLYLINE in this case), use a selection set containing the entities that cross the polyline using the acedSSGet() function coupled with the 'F' (Fence) options. (See code below.)
In the application listed below, the user is asked to select a polyline (LWPOLYLINE) entity. Having selected the polyline entity and verified that the selection is an AcDbPolyline entity, proceed and retrieve the entities bounding box.
I will explain the purpose of these later and possible alternatives to getting the bounding box of the entity. Next we iterate through the polyline and place all the vertices of the polyline in an AcGePoint3dArray. In order to use the function acedSSGet() with the 'F' option, we need to pass in as the second argument to acedSSGet() a resbuf linked list that contains all the points that make up our "Fence" point which is essentially the vertices that make up our selected LWPOLYLINE entity. Using a 'for' loop we step through our AcGePoint3dArray and build a linked list of result buffers (of type RT3DPOINT). The variable 'pPointList' is that list of result buffers. This list of point is passed to the acedSSGet() function as the second argument. The resulting selection set is returned in 'interSS'.
In this case the selection set 'interSS' will contain one entity which is our selected AcDbPolyline entity. After all it is part of the 'Fence'. In the final 'for' loop I walk through the selection set and get the objectId of each entity and compare it to the objectId of the current entity to that of our selected LWPOLYLINE, if they are the same I simply 'continue' at that point. Here I just inform the user how many entities intersect our AcDbPolyline and print out to the command prompt the kinds of entity found.
Here is the code for the first part, I will explain the bounding box next:
// Here are your new AutoCAD functions. Add your code.
//////////////////////////////////////////////////////
void fencepoly ()
{
AcDbObject *pObj;
AcDbPolyline *pPolyEnt;
AcDbObjectId polyId, objId;
AcGePoint3dArray arPolyPoints;
AcGePoint3d polyPoint;
AcGeBoundBlock2d polyBox;
AcGePoint2d minPolyBox, maxPolyBox;
 struct resbuf *pPointList, *pTemp;
ads_name ename;
ads_name interSS;
ads_point pickpt, curPoint;
 int rc; long len; long count;
   // Select the Window entity to get its handle
rc = acedEntSel(L"\nSelect LWPOLYLINE entity ", ename, pickpt);
 if(rc != RTNORM)
{
  acutPrintf(L"\nError selecting LWPOLYLINE entity ");
  return;
}
 // Get the entity object ID
acdbGetObjectId(polyId, ename);
 // Open the entity for a read operation
acdbOpenObject(pObj, polyId, AcDb::kForRead);
 // Is pObj an AcDbPolyline object ?
pPolyEnt = AcDbPolyline::cast(pObj);
 if(!pPolyEnt)
{
  acutPrintf(L"\nEntity selected is not a LWPOLYLINE ");
  pObj->close();
  return;
}
polyBox = getPolylineBoundBox(pPolyEnt);
polyBox.getMinMaxPoints(minPolyBox, maxPolyBox); 
acedCommand(RTSTR, L"_ZOOM", RTSTR, L"_W",
  RTPOINT, asDblArray(minPolyBox),
  RTPOINT, asDblArray(maxPolyBox), RTNONE);
   for(count = 0; count < pPolyEnt->numVerts(); count++)
{
  pPolyEnt->getPointAt(count, polyPoint);
  arPolyPoints.append(polyPoint);
}
pPolyEnt->close();
   for(count = 0; count < arPolyPoints.length(); count++)
{
  polyPoint = arPolyPoints.at(count);
  acdbPointSet(asDblArray(polyPoint), curPoint);
  if(count == 0)
  {
   pPointList = acutNewRb(RT3DPOINT);
   acdbPointSet(curPoint, pPointList->resval.rpoint);
   pTemp = pPointList;
  }
  else
  {
   pTemp->rbnext = acutNewRb(RT3DPOINT);
   pTemp = pTemp->rbnext;
   acdbPointSet(curPoint, pTemp->resval.rpoint);
  }
}
   // pPointList is now a linked list of resbuf
 // containing points
rc = acedSSGet(L"_F", pPointList, NULL, NULL, interSS);
acutRelRb(pPointList);
acedSSLength(interSS, &len);
acutPrintf(
L"\nThere are %d entities crossing your selected LWPOLYLINE entity.",
  len - 1);
   for(count = 0; count < len; count++)
{
  acedSSName(interSS, count, ename);
  acdbGetObjectId(objId, ename);
  acdbOpenObject(pObj, objId, AcDb::kForRead);
  if(objId == polyId)
  {
   pObj->close();
   continue;
  }
  const TCHAR *cstr = pObj->isA()->name();
  acutPrintf(
   L"\nThe entity crossing your LWPOLYLINE is a %s.",
   cstr);
  pObj->close();
}
}
Let's move on and discuss the user-defined function 'getPolylineBoundBox()', here is how its called from 'fencepoly':
polyBox = getPolylineBoundBox(pPolyEnt);
Refer to the code below. This function takes as a parameter the selected AcDbPolyline. You then step through all of the segments of the polyline in a 'for' loop and test to see if the segments are 'arc' or 'line' based. These are all added to an AcGeVoidPointerArray. If you are dealing with a single segment polyline, cast the first element of 'geCurves' to an AcGeCurve2d geometric entity, otherwise, create a single AcGeCompositeCurve2d, which is a single curve made up of a collection of sub curves. The 'orthoBoundBlock()' will give you the bounding box of the curve that is parallel to the coordinate axis. Having returned the bounding box, get the lower left and upper right point for the box. These are the points to which you execute 'acedCommand()' with the 'ZOOM' window option. Here is the 'getPolylineBoundBox()' function:
AcGeBoundBlock2d getPolylineBoundBox(AcDbPolyline* pPoly) {
AcGeVector3d normal;
 int nSegs;
AcGeLineSeg2d *pLine;
AcGeLineSeg2d line;
AcGeCircArc2d *pArc;
AcGeCircArc2d arc;
AcGeVoidPointerArray geCurves;
AcGeCurve2d *pPolyGeCurve;
AcGeBoundBlock2d polyBoundBox;
  nSegs = pPoly->numVerts() - 1;
 for(int i = 0; i < nSegs; i++)
{
  if(pPoly->segType(i) == AcDbPolyline::kLine)
  {
   pPoly->getLineSegAt(i, line);
   pLine = new AcGeLineSeg2d(line);
   geCurves.append(pLine);
  }
  else if(pPoly->segType(i) == AcDbPolyline::kArc)
  {
   pPoly->getArcSegAt(i, arc);
   pArc = new AcGeCircArc2d(arc);
   geCurves.append( pArc );
  }
}// for
   if(geCurves.length() == 1)
  pPolyGeCurve = (AcGeCurve2d*)(geCurves[0]);
 else
  pPolyGeCurve = new AcGeCompositeCurve2d(geCurves);
polyBoundBox = pPolyGeCurve->orthoBoundBlock();
 return polyBoundBox;
}
As an alternative to getting the bounding box of the polyline, you can simply execute a zoom extents. The reason a zoom extents or zoom to the extents of the polyline is required is that if you are zoomed in on the polyline and some entities cross the polyline but are not in the view screen (display screen), they will not be reported even though all the vertices of the polyline for the point list as the second argument of acedSSGet() can be extracted.

## 评论

**内容**: Luis Sant Ana said...
Thank you, very much!
Reply
06/18/2014 at 10:28 AM

---
**内容**: hisham said...
hi
my polyline has arcs
how to build the "pTemp"
thanks
pTemp->rbnext = acutNewRb(RT3DPOINT);
pTemp = pTemp->rbnext;
acdbPointSet(curPoint, pTemp->resval.rpoint);
Reply
12/02/2014 at 09:39 AM

---
**内容**: Francisco Silva said...
hi who if i have a polyline in ucs.
how do I get these coordinates?
thank you
Reply
06/09/2020 at 12:04 AM

---
**内容**: Aniket said...
I have versioned up the Realdwg from Realdwg 2015 to Realdwg 2020.
When I tried to build the source code using Realdwg, In function AcDbJoinEntityPE::joinEntities.
Even though I am providing correct arguments, While compiling it gives me error mentioned below.
Error C2061 syntax error: identifier 'AcGeIntArray' KmDumpDwgc c:\program files\autodesk\realdwg 2020\inc\dbjoinentitype.h
Error C2660 'AcDbJoinEntityPE::joinEntities': function does not take 3 arguments KmDumpDwg d:\releases\during gikiban\temp repo\dumpdwg\kmdumpdwg\src\plateutility.cpp
It works fine with Realdwg 2015, Please let know if something needs to be change.
Thanks in advance.

Reply
08/18/2020 at 06:06 AM

---
