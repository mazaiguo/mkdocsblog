---
title: "Extending AssociativeDimension To CustomSolid"
date: 2017-03-01
categories:
  - AutoCAD
tags:
  - Dimension
  - Solid
description: "This is a continuation of the post written by my colleague."
author: Autodesk
---
# Extending AssociativeDimension To CustomSolid

发布日期: 2017-03-01

原始链接: https://adndevblog.typepad.com/autocad/2017/03/extending-associativedimension-to-customsolid.html

## 文章内容

By Madhukar Moogala
This is a continuation of the post written by my colleague.
In this blog we will explore the Associative mechanism applied to custom solid, previous blog solution may not be applicable when Dimensions are applied using snap points on the sub-entities of a solid. I have created a Frustum solid with Axis of revolution.
To exploit Associative framework, we need to reveal the our subEntities by implementing associative protocol extension AcDbAssocPersSubentIdPE.
The Associative Framework queries this protocol extension when creating new associative dimensions based on AcDbAssocAnnotationActionBody.
Below is only a partial code that exposes sub-entities by implementing persistent protocol.
AcDbEntity* MyEnt1::subSubentPtr(const AcDbFullSubentPath& path) const
{
const AcDbSubentId subEntId = path.subentId();

if (isCustomSubentId(subEntId))
{
AcDbEntity* pSubEntity = nullptr;
const Adesk::GsMarker subentIndex = subEntId.index();

switch (subEntId.type())
 {
 case AcDb::kEdgeSubentType:
 {
 if (subentIndex == kCustomEdgeSubentIndex)
  {
  pSubEntity = new AcDbLine(m_ptSP, m_ptEP); 
  }
 }
 break;
 case AcDb::kVertexSubentType:
 {
 if (subentIndex == kCustomVertex1SubentIndex)
  {
  pSubEntity = new AcDbPoint(m_ptSP); 
  }
 else if (subentIndex == kCustomVertex2SubentIndex)
  {
  pSubEntity = new AcDbPoint(m_ptEP);
  }
 }
 break;
 }
ASSERT(pSubEntity != nullptr);
return pSubEntity;
}

// If not data of the derived class, use the base class implementation
//
return AcDb3dSolid::subSubentPtr(path);
}

Acad::ErrorStatus MyEnt1::subGetSubentPathsAtGsMarker(AcDb::SubentType type,
            Adesk::GsMarker gsMark,
            const AcGePoint3d & pickPoint, 
            const AcGeMatrix3d & viewXform,
            int & numPaths, 
            AcDbFullSubentPath *& subentPaths,
            int numInserts, 
            AcDbObjectId * entAndInsertStack) const
{
assertReadEnabled();

numPaths = 0;
subentPaths = NULL;

if (gsMark == 0)
return Acad::eInvalidInput;

if (isCustomGsMarker(gsMark))
{
switch (type)
 {
 case AcDb::kEdgeSubentType:
 {
 if (gsMark == kCustomEdgeGsMarker)
  {
  numPaths = 1;
  subentPaths = new AcDbFullSubentPath[1];
  subentPaths[0] = AcDbFullSubentPath(objectId(),
     AcDb::kEdgeSubentType,
     kCustomEdgeSubentIndex);
  }
 }
 break;
 case AcDb::kVertexSubentType:
 {
 if (gsMark == kCustomEdgeGsMarker)
  {
  numPaths = 2;
  subentPaths = new AcDbFullSubentPath[2];
  subentPaths[0] = AcDbFullSubentPath(objectId(),
     AcDb::kVertexSubentType,
     kCustomVertex1SubentIndex);
  subentPaths[1] = AcDbFullSubentPath(objectId(),
     AcDb::kVertexSubentType,
     kCustomVertex2SubentIndex);
  }
 }
 break;
 }
ASSERT(numPaths != 0);
return Acad::eOk;
}

// If not data of the derived class, use the base class implementation
//
return AcDb3dSolid::subGetSubentPathsAtGsMarker(type,
    gsMark, 
    pickPoint,
    viewXform,
    numPaths,
    subentPaths,
    numInserts, 
    entAndInsertStack);
}

Acad::ErrorStatus MyEnt1::subGetGsMarkersAtSubentPath(const AcDbFullSubentPath& path, 
    AcDbIntPtrArray&  gsMarkers) const
{
const AcDbSubentId subEntId = path.subentId();

if (isCustomSubentId(subEntId))
{
gsMarkers.removeAll();

const Adesk::GsMarker subentIndex = subEntId.index();

switch (subEntId.type())
 {
 case AcDb::kEdgeSubentType:
 {
 if (subentIndex == kCustomEdgeSubentIndex)
  {
  gsMarkers.append(kCustomEdgeGsMarker);
  }
 }
 break;
 case AcDb::kVertexSubentType:
 {
 if (subentIndex == kCustomVertex1SubentIndex || 
  subentIndex == kCustomVertex2SubentIndex)
  {
  gsMarkers.append(kCustomEdgeGsMarker);
  }
 }
 break;
 }
ASSERT(!gsMarkers.isEmpty());
return Acad::eOk;
}

// If not data of the derived class, use the base class implementation
//
return AcDb3dSolid::subGetGsMarkersAtSubentPath(path, gsMarkers);
}

Adesk::UInt32 MyEnt1::subSetAttributes(AcGiDrawableTraits *traits)
{
assertReadEnabled();
return AcDb3dSolid::subSetAttributes(traits);
}

Acad::ErrorStatus MyEnt1::subGetOsnapPoints(AcDb::OsnapMode osnapMode,
Adesk::GsMarker gsSelectionMark,
const AcGePoint3d& pickPoint,
const AcGePoint3d& lastPoint,
const AcGeMatrix3d& viewXform,
AcGePoint3dArray& snapPoints,
AcDbIntArray& geomIds) const
{
assertReadEnabled();

if (MyEnt1::isCustomGsMarker(gsSelectionMark))
{
switch (osnapMode)
 {
 case AcDb::kOsModeEnd:
 {
 snapPoints.append(m_ptSP);
 snapPoints.append(m_ptEP);
 }
 break;
 case AcDb::kOsModeNear:
 {
 AcGeVector3d viewDir(viewXform(Z, 0), viewXform(Z, 1), viewXform(Z, 2));
 AcGeLine3d line3d(m_ptSP, m_ptEP);
 snapPoints.append(line3d.projClosestPointTo(pickPoint, viewDir));
 }
 break;
 }
return Acad::eOk;
}

// If not data of the derived class, use the base class implementation
//
return AcDb3dSolid::subGetOsnapPoints(osnapMode,
   gsSelectionMark,
   pickPoint, 
   lastPoint, 
   viewXform,
   snapPoints,
   geomIds);
}

Acad::ErrorStatus MyEnt1::subTransformBy(const AcGeMatrix3d& xform)
{
assertWriteEnabled();

m_ptSP.transformBy(xform);
m_ptEP.transformBy(xform);

return AcDb3dSolid::subTransformBy(xform);
}


//Always check iff 100000 <= gsMarker <= 1000002
bool MyEnt1::isCustomGsMarker(Adesk::GsMarker gsMarker)
{
return kCustomGsMarkerMin <= gsMarker &&
 gsMarker <= kCustomGsMarkerMax;
}


bool MyEnt1::isCustomSubentId(const AcDbSubentId& subentId)
{
const Adesk::GsMarker index = subentId.index();
return kCustomSubentIdIndexMin <= index &&
 index <= kCustomSubentIdIndexMax;
}
  Here is a screencast and source project is available at GitHub.

## 评论

**内容**: Himanshu K said...
1) Why do you need to create additional edge/vertices to dimension a solid(frustum)?
2) How this approach of adding edge/vertices will work for a complex solid created using boolean operations?
3) Is it possible to reassign the gsMarkers of AcDb3dSolid to identify the subentities(face, edge, vertex) of it?
4) Can you provide APIs with additional input parameter "AcDbEntity* entity"?. e.g.
- subSubentPtr(AcDbEntity* entity, const AcDbFullSubentPath& id);
- subGetSubentPathsAtGsMarker(AcDbEntity* entity,...);
- subGetGsMarkersAtSubentPath(AcDbEntity* entity,...);
These APIs will be useful in identifying entities embedded within a custom entity.
Himanshu K
Reply
04/20/2017 at 04:20 AM

---
**内容**: Madhukar Moogala said in reply to Himanshu K...

Typepad HTML Email

Thanks for stopping by,
1)    
This is only for representation and simplicity I created an edge in frustum, so I can attach a dimension.
2)    
You can apply associative mechanism for all solids and Booleans too, however you may encounter difficulties which should be addressed by
case by case.
3)    
I didn’t understand your query.
 
  Thanks,
Madhu.
  Reply
04/20/2017 at 04:55 AM

---
**内容**: Himanshu K said in reply to Madhukar Moogala...
Hi Madhu,
Thanks! for reply.
Regarding question 3.
When you create a frustum solid(AcDb3dSolid). All its subentities(faces, edges, vertices) will have an integer marker(Adesk::GsMarker) assigned to it by system. e.g. circle(1, 2).
I would like to change these numbers to say circle(1001, 1002).
Best Regards,
Himanshu K
Reply
04/20/2017 at 06:52 AM

---
