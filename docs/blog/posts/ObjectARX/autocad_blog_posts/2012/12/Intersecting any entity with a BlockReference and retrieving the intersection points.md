---
title: "Intersecting any entity with a BlockReference and retrieving the intersection points"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Block
description: "Intersecting a block reference with your entity is tricky. Every time you try to get the intersection points, it will return the intersection of yo..."
author: Autodesk
---
# Intersecting any entity with a BlockReference and retrieving the intersection points

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/intersecting-any-entity-with-a-blockreference-and-retrieving-the-intersection-points.html

## 文章内容

By Gopinath Taget
Intersecting a block reference with your entity is tricky. Every time you try to get the intersection points, it will return the intersection of your entity with the bounding box of the block reference. e.g. pLine.->intersectWith( pBlock...) and pBlock->intersectWith( pLine...), just return the intersection of the line entity with the block reference bounding box.
How do you find the real intersection points of an entity with the entities in the block reference?
There are two ways to do this:

1) The first method involves opening the AcDbBlockReference, finding its AcDbBlockTableRecord and then iterating through the entities within the block definition, calling AcDbEntity::intersectWith() on each. This method is fine, except that the code is quite tricky to write. Also you will be checking the entities in the actual block definition so the positions of the entities would then have to be temporarily transformed by the AcDbBlockReference's transformation matrix for the intersectWith to work correctly. 
2) The second way, which is far simpler, is to explode the AcDbBlockReference using the explode() method. This returns an array of entities that would be the exploded version of the AcDbBlockReference. They are even correctly transformed by the blockTransform matrix. All we have to do is iterate through these entities, call intersectWith(), get the results and then delete them.
Here is the relevant code:
//*********************************************************
// get the intersection point of 2 entities and return the
// result in interSectionPoint
// static int GetIntersectionPointsOf (
//      ads_name ename1, ads_name ename2,
//      AcGePoint3dArray &intersectionPoints);
  // get the intersection point of 2 AcDbEntity's and return
// the result in interSectionPoint
// static int GetIntersectionPointsOf (
//      AcDbEntity *pEnt1, AcDbEntity *pEnt2,
//      AcGePoint3dArray &intersectionPoints);
  // get intersection points from a block
//static int GetIntersectionPointsFromBlockEntities (
//      AcDbEntity *pEnt1,
//      AcDbEntity *pEnt2,
//      AcGePoint3dArray &intersectionPoints);
  // draws a little cross at the pnt specified
// static void blip (AcGePoint3d pnt, int colour=4);
//**********************************************************
// This is command 'TEST'
void asdktest()
{
ads_name ename1;
ads_point pnt;
 // pick first entity to check
 int res = acedEntSel (
  L"\nPick first entity : ", ename1, pnt);
 // if the user wants to carry on
 if (res == RTNORM)
{
  // hightlight the entity picked
  acedRedraw (ename1, 3);
    ads_name ename2;
  // now pick the second entity
  res = acedEntSel (
   L"\nPick second entity : ", ename2, pnt);
  // if the user wants to carry on
  if (res == RTNORM)
  {
   // hightlight the entity picked
   acedRedraw (ename2, 3);
     AcGePoint3dArray intersectionPoints;
   // get the intersection point of 2
   // entities and return the result in
   // interSectionPoint
   if (GetIntersectionPointsOf (
    ename1,
    ename2,
    intersectionPoints) == RTNORM)
   {
    // see how many points we've got
    int length = intersectionPoints.length ();
    // loop them and create a linked
    // list containing all of the points
    for (int i=0; i<length; ++i)
    {
     // show the intersection
     blip (intersectionPoints[i]);
    }
   }
     // un-hightlight the entity picked
   acedRedraw (ename2, 4);
  }
    // un-hightlight the entity picked
  acedRedraw (ename1, 4);
}
}
//*********************************************
// get the intersection point of 2 enames and
// return the result in interSectionPoint
static int GetIntersectionPointsOf (
ads_name ename1,
ads_name ename2,
AcGePoint3dArray &intersectionPoints)
{
AcDbObjectId objectId1, objectId2;
 // get an object id from the first
 // ename supplied, test to see if valid
 if (acdbGetObjectId (
  objectId1, ename1) != Acad::eOk)
  return (RTERROR);
 // get an object id from the second
 // ename supplied, test to see if valid
 if (acdbGetObjectId (
  objectId2, ename2) != Acad::eOk)
  return (RTERROR);
  AcDbEntity *pEnt1 = NULL;
 // open the object because we want to extract
 // some info out of it like the start
 // and end points etc
Acad::ErrorStatus es = acdbOpenObject (
  pEnt1, objectId1, AcDb::kForRead);
 // if it opened ok
 if (es == Acad::eOk)
{
  // take extra care and make sure
  // we have a valid pointer
  if (pEnt1 != NULL)
  {
   AcDbEntity *pEnt2 = NULL;
   // open the object because we want to
   // extract some info out of it like
   // the start and end points etc
   Acad::ErrorStatus es = acdbOpenObject (
    pEnt2, objectId2, AcDb::kForRead);
   // if it opened ok
   if (es == Acad::eOk)
   {
    // take extra care and make sure
    // we have a valid pointer
    if (pEnt2 != NULL)
    {
     // get intersection points of the
     //2 AcDbEntity's and return the
     // result in interSectionPoint
     int res = GetIntersectionPointsOf (
      pEnt1, pEnt2, intersectionPoints);
       // close the entities after we've finished
     pEnt1->close ();
     pEnt2->close ();
       return (res);
    }
   }
  }
}
   return (RTERROR);
}
//*********************************************
// get the intersection point of 2 AcDbEntity's
// and return the result in interSectionPoint
static int GetIntersectionPointsOf (
AcDbEntity *pEnt1,
AcDbEntity *pEnt2,
AcGePoint3dArray &intersectionPoints)
{
 // if the first entity is a block reference
 if (pEnt1->isA() == AcDbBlockReference::desc ())
{
  // get intersection points from a block
  GetIntersectionPointsFromBlockEntities (
   pEnt1, pEnt2, intersectionPoints);
}
 // if the first entity is a block reference
 else if (
  pEnt2->isA() == AcDbBlockReference::desc ())
{
  // get intersection points from a block
  GetIntersectionPointsFromBlockEntities (
   pEnt2, pEnt1, intersectionPoints);
}
 else
{
  // found out where they intersect with each other
  pEnt1->intersectWith (
   pEnt2, AcDb::kOnBothOperands, intersectionPoints);
}
   return (RTNORM);
}
//*********************************************
// get intersection points from a block
static int GetIntersectionPointsFromBlockEntities (
AcDbEntity *pEnt1, AcDbEntity *pEnt2,
AcGePoint3dArray &intersectionPoints)
{
 // can't handle 2 blocks
 if (pEnt2->isA() == AcDbBlockReference::desc ())
{
  acutPrintf (
  L"\nError - this routine can't handle 2 blocks, sorry");
  return (RTERROR);
}
   // dynamic cast to BlockReference
AcDbBlockReference *pBlockRef =
  AcDbBlockReference::cast (pEnt1);
 if (pBlockRef != NULL)
{
  AcDbVoidPtrArray entitySet;
  // explode the block, this will return a
  // load of pre-transfromed entities for our perusal
  Acad::ErrorStatus es = pBlockRef->explode (entitySet);
  // if it worked ok
  if (es == Acad::eOk)
  {
   // loop round getting the intersection points
   for (long i=0l; i<entitySet.length (); ++i)
   {
    // get a pointer to the entity object
    AcDbEntity *pNewEnt = (AcDbEntity *)entitySet.at (i);
      // recall this function to check the entities
    if (GetIntersectionPointsOf (
     pNewEnt, pEnt2, intersectionPoints) != RTNORM)
    {
     acutPrintf (L"\nError getting objects");
    }
      // clean it up as we don't need it anymore
    delete pNewEnt;
   }
  }
}
 return (RTNORM);
}
// draws a little blip at the specified point
//*********************************************
#define pi 3.1415926535897932384626433832795
// draws a little cross at the pnt specified
static void blip (AcGePoint3d pnt, int colour=4)
{
 struct resbuf view;
memset (&view, 0, sizeof (struct resbuf));
 // get the size of the screen in units
  acedGetVar (L"VIEWSIZE", &view);
  ads_point p2, p3, p4, p5;
  acutPolar (asDblArray (pnt),      0.0,
   view.resval.rreal/60.0, p2);
  acutPolar (asDblArray (pnt),   pi/2.0,
   view.resval.rreal/60.0, p3);
  acutPolar (asDblArray (pnt),       pi,
   view.resval.rreal/60.0, p4);
  acutPolar (asDblArray (pnt),pi+pi/2.0,
   view.resval.rreal/60.0, p5);
    acedGrDraw(p2, p4, colour, 0);
  acedGrDraw(p3, p5, colour, 0);
}

## 评论

**内容**: Heriniaina said...
code equivalence in vb.net, please
Reply
05/11/2017 at 06:13 AM

---
