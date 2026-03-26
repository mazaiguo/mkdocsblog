---
title: "Intersection between a Face and a Line using ARX"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Solid
description: "How can I compute the intersection point, if any, between an AcDbFace entity and an AcDbLine?"
author: Autodesk
---
# Intersection between a Face and a Line using ARX

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/intersection-between-a-face-and-a-line-using-arx.html

## 文章内容

By Philippe Leefsma
How can I compute the intersection point, if any, between an AcDbFace entity and an AcDbLine?
Solution
There are mainly two ways you can do that using arx, the following DevNote exposes both:
1 - First technique create an infinite plane and infinite line, then uses a ray to check if the intersection point of these two infinite entities is inside the face.
2 - Second technique uses 3D solids. It creates a thin extruded solid from the face and another to represent the line, then uses checkInterferences method to find out the intersection point.
Below are the samples for these functions, along with a test function:
/////////////////////////////////////////////////////////////////////
//Use: Intersection between Face and Line using Ray
//
/////////////////////////////////////////////////////////////////////
void FindIntersection(AcDbFace* pFace, AcDbLine* pLine)
{
 AcGePoint3d vertex1, vertex2, vertex3, vertex4;
   pFace->getVertexAt(0, vertex1);
 pFace->getVertexAt(1, vertex2);
 pFace->getVertexAt(2, vertex3);
 pFace->getVertexAt(3, vertex4);
   AcGeVector3d vecU(vertex2.asVector()-vertex1.asVector());
 AcGeVector3d vecV(vertex3.asVector()-vertex1.asVector());
   //Create temp plane
 AcGePlane plane(vertex1, vecU, vecV);
   //Create temp line
 AcGeLineSeg3d line (pLine->startPoint(), pLine->endPoint());
   //Check intersection
 AcGePoint3d resultPoint;
   if (plane.intersectWith(line, resultPoint) == Adesk::kTrue)
 {
  AcGeRay3d ray(resultPoint, vertex1.asVector() - vertex2.asVector());
    int intNum = 0;
    //check if intersection point is inside the face
  AcGePoint3d intPoint;
    if (ray.intersectWith(AcGeLineSeg3d(vertex1, vertex2), intPoint)
       == Adesk::kTrue) ++intNum;
  if (ray.intersectWith(AcGeLineSeg3d(vertex2, vertex3), intPoint)
       == Adesk::kTrue) ++intNum;
  if (ray.intersectWith(AcGeLineSeg3d(vertex3, vertex4), intPoint)
      == Adesk::kTrue) ++intNum;
  if (ray.intersectWith(AcGeLineSeg3d(vertex4, vertex1), intPoint)
      == Adesk::kTrue) ++intNum;
    //if intNum is 'odd' then point is inside
  if((intNum%2) != 0)
  {
   acutPrintf (L"\nIntersection point: [%f, %f, %f]",
       resultPoint.x, resultPoint.y, resultPoint.z);
  }
 }
}
  /////////////////////////////////////////////////////////////////////
//Use: Intersection between Face and Line using 3D Solids
//
/////////////////////////////////////////////////////////////////////
void FindIntersection2(AcDbFace* pFace, AcDbLine* pLine)
{
 //Line direction
 AcGeVector3d direction (pLine->endPoint()-pLine->startPoint());
   //Create temp circle
 AcDbCircle* pcircle =
     new AcDbCircle(pLine->startPoint(), direction, 0.01);
   //Create temp solid line
 AcDb3dSolid* pSolidLine = new AcDb3dSolid ();
   AcDbSweepOptions sweepOptions;
   pSolidLine->createExtrudedSolid(pcircle, direction, sweepOptions);
   //Create temp solid Face
 AcDb3dSolid  *pSolidFace = new AcDb3dSolid ();
   AcGePoint3d vertex1, vertex2, vertex3;
   pFace->getVertexAt(0, vertex1);
 pFace->getVertexAt(1, vertex2);
 pFace->getVertexAt(2, vertex3);
   AcGeVector3d vec1(vertex2.asVector()-vertex1.asVector());
 AcGeVector3d vec2(vertex3.asVector()-vertex1.asVector());
   //Compute face's normal
 AcGeVector3d faceNormal = vec2.crossProduct(vec1);
   faceNormal *= 0.01 / faceNormal.length();
   //Create a very thin extruded solid
 pSolidFace->createExtrudedSolid(pFace, faceNormal, sweepOptions);
   //Check interference between the two solids
 Adesk::Boolean IsIntersec;
 AcDb3dSolid* commonVolumeSolid;
   Acad::ErrorStatus es =
        pSolidFace->checkInterference(
              pSolidLine,
              Adesk::kTrue,
              IsIntersec,
              commonVolumeSolid); 
   if (IsIntersec == Adesk::kTrue)
 {
  double volume;
  AcGePoint3d centroid;
    double momInertia[3], prodInertia[3], prinMoments[3],
      radiiGyration[3];
    AcGeVector3d prinAxes[3];
    AcDbExtents extents;
    commonVolumeSolid->getMassProp(
         volume,
         centroid,
         momInertia,
         prodInertia,
         prinMoments,
         prinAxes,
         radiiGyration,
         extents);
    acutPrintf (L"\nIntersection point: [%f, %f, %f]",
         centroid.x, centroid.y, centroid.z);
    delete commonVolumeSolid;
 }
   delete pcircle;
 delete pSolidLine;
 delete pSolidFace;
}
  //The test method
void FindIntersectionTest(void)
{
 ads_name ename; 
 ads_point pickpt; 
   AcDbObjectId objId;
 AcDbObject *pObj;
   int rc;
   rc= acedEntSel(L"\nSelect Face: ", ename, pickpt);
   if(rc != RTNORM)
 {
  if (rc != RTCAN) acutPrintf(L"\nError selecting entity ");
  return;
 }
   acdbGetObjectId(objId, ename);
 acdbOpenObject(pObj, objId, AcDb::kForRead);
   AcDbFace* pEntity1 = AcDbFace::cast(pObj);
   if(!pEntity1)
 {
  acutPrintf(L"\nSelection Invalid...");
  pObj->close();
  return;
 }
   rc= acedEntSel(L"\nSelect line: ", ename, pickpt);
   if(rc != RTNORM)
 {
  if (rc != RTCAN) acutPrintf(L"\nError selecting entity ");
  return;
 }
   acdbGetObjectId(objId, ename);
 acdbOpenObject(pObj, objId, AcDb::kForRead);
   AcDbLine* pEntity2 = AcDbLine::cast(pObj);
   if(!pEntity2)
 {
  acutPrintf(L"\nSelection Invalid...");
  pObj->close();
  return;
 }
   FindIntersection (pEntity1, pEntity2);
 FindIntersection2(pEntity1, pEntity2);
   pEntity1->close();
 pEntity2->close();
}

## 评论

**内容**: Sandip Korde said...
Hi Philippe,
I am using VBA in AutoCAD 2011, can you provide me same code for VBA. I am intersecting a line with all available 3D faces and extending to to the 3D face against which it intersects. Hope you got my point.
Thanks,
Sandip Korde
Reply
10/24/2013 at 07:45 AM

---
**内容**: Philippe said...
Hi Sandip,
Sorry, it's hard for us to write code on an on-demand basis. I don't have a VBA sample for the same. As you may know the ActiveX API is significantly less powerful than ARX, so what's doable in ARX is not always in VBA. For example ActiveX API has no AcGe transient entities, so it would make the first approach impossible. You may want to try the second approach by creating solids, but you will have to add entities to the database in order to be able to invoke methods on it, I'm thinking you could try AcadSolid.IntersectWith...
Good luck!
Reply
10/30/2013 at 01:50 AM

---
