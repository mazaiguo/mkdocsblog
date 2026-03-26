---
title: "How to Implement Dynamic UCS for Custom Solids"
date: 2020-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Solid
  - UCS
description: "You need to derive  from this class(AcDbDynamicUCSPE) in order to enable Dynamic UCS switching for your custom objects or for other core objects."
author: Autodesk
---
# How to Implement Dynamic UCS for Custom Solids

发布日期: 2020-09-01

原始链接: https://adndevblog.typepad.com/autocad/2020/09/how-to-implement-dynamic-ucs-for-custom-solids.html

## 文章内容

By Madhukar Moogala
You need to derive  from this class(AcDbDynamicUCSPE) in order to enable Dynamic UCS switching for your custom objects or for other core objects.
By default, the core DUCS code will call this protocol extension on objects under the cursor during the initial point acquisition in DUCS-enabled command.
Derived classes must override and implement getCandidatePlanes().
And, also if you don’t implement AutoCAD Solid’s and it derived entities can participate in dynamic UCS using the default AcDb3dSolidDynamicUCSPE, this  protocol extension is always registered by AcDb during startup.  So, unless some other app has explicitly removed or replaced it, it will always be in place for AcDb3dSolids and classes derived from that.
There's also an AcDbEntityDynamicUCSPE protocol extension that's added at the AcDbEntity level to provide a default implementation for all classes.
Note:
getCandidatePlanes() is only called for entities that have subentities.  For such entities, it is called once for each subentity with the subentId argument being the id of the subent for which it is being called.
For entities that don't have subentities, the AcDbNonSubEntDynamicUCSPE protocol extension base class should be used, and its getCandidatePlane() method will be called.

Acad::ErrorStatus AsdkUCSPE::getCandidatePlanes(
 AcArray& results,
 double& distToEdge,
 double& objWidth,
 double& objHeight,
 AcDbEntity* pEnt,
 const AcDbSubentId& subentId,
 const AcGePlane& viewplane,
 AcDbDynamicUCSPE::Flags flags) const
{
 Acad::ErrorStatus es = Acad::eInvalidInput;
 if (!pEnt)
  return es;

 // Check if User selected custom Solid plane, we are not doing anything here, just to make sure 
    //Debugger hits us, ideally we are expected to populate the result array 
    // with one or more AcGePlane objects and return Acad::eOk if successful.

 CMyBox* pSolid = CMyBox::cast(pEnt);
 if (!VERIFY(pSolid != NULL))
  return Acad::eInvalidInput;

 AcDb::SubentType seType = subentId.type();
 if (seType != AcDb::kFaceSubentType)
  return Acad::eWrongSubentityType;

 AcDbFullSubentPath facePath(pEnt->objectId(), subentId);
 std::auto_ptr pFaceSubEnt;
 pFaceSubEnt.reset(pEnt->subentPtr(facePath));
 
 if (pFaceSubEnt.get() && 
 pFaceSubEnt->isKindOf(AcDbRegion::desc()))
 {
  AcDbRegion* reg = AcDbRegion::cast(pFaceSubEnt.get());
  assert(reg != NULL);
  if (!reg)
   return (Acad::eWrongObjectType);
  AcGePlane entPlane;
  AcDb::Planarity kPanarity;
  es = reg->getPlane(entPlane, kPanarity);

  //- Test for intersection 
  // between the circle's plane and Zaxis of viewplane
  AcGeLine3d line;
  line.set(viewplane.pointOnPlane(),
  viewplane.normal());

  AcGePoint3d intersectPnt;
  if (entPlane.intersectWith(line, intersectPnt) == Adesk::kTrue)
  {
   AcDbExtents extents;
   if (reg->getGeomExtents(extents) != Acad::eOk)
    return (Acad::eInvalidInput);

   const double diagonal = extents.minPoint().
      distanceTo(extents.maxPoint());
   objWidth = diagonal;
   objHeight = diagonal;

   //- now calculate closest edge to the intersection point
   //- and set the origin and X axis accordingly

   AcGePoint3d origin;
   AcGeVector3d xAxis, yAxis;
   entPlane.getCoordSystem(origin, xAxis, yAxis);
   distToEdge = origin.distanceTo(intersectPnt);

   AcGePlane newPlane(entPlane);
   results.append(newPlane);
   return Acad::eOk;

  }
  return Acad::eNotApplicable;
 }
 return Acad::eNotApplicable;
}
Demo and source code

## 评论

**内容**: Gielle said...
Interesting topic
Reply
04/23/2021 at 05:22 AM

---
