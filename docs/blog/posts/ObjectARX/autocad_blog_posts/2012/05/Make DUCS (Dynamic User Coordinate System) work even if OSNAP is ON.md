---
title: "Make DUCS (Dynamic User Coordinate System) work even if OSNAP is ON"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Dimension
  - Polyline
  - Solid
  - UCS
description: "I have a custom entity (a polygon) and I enabled DUCS on it, which works fine when OSNAP is switched off. I can see that in case of e.g. a face of ..."
author: Autodesk
---
# Make DUCS (Dynamic User Coordinate System) work even if OSNAP is ON

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/make-ducs-dynamic-user-coordinate-system-work-even-if-osnap-is-on.html

## 文章内容

By Adam Nagy
I have a custom entity (a polygon) and I enabled DUCS on it, which works fine when OSNAP is switched off. I can see that in case of e.g. a face of a solid entity the DUCS works even if OSNAP is on. How could I make DUCS work like that for my custom entity?
Solution
If OSNAP succeeds at a certain cursor position, then AcDbDynamicUCSPE::getCandidatePlanes() will not be called so DUCS will not work.
As you said, in case of a face DUCS works even if OSNAP is on - but please note, that it only does so when the cursor moves off the edges and goes towards the center of the face. In other words DUCS works on a face even if OSNAP is on, when the cursor is at a position where OSNAP fails. The problem is that a polyline (or a polygon, i.e. closed polyline) does not have an area where OSNAP could fail, because it only consists of the lines but not the enclosed area.
So, the simplest solution is to draw your lines plus draw the enclosed area as well that OSNAP would be called on and could fail, so that getCandidatePlanes() would be called.
In the attached sample I have a custom entity derived from AcDbCircle - first it draws an empty circle and then a filled one:
Adesk::Boolean AsdkEntity::subWorldDraw (AcGiWorldDraw *mode)
{
  assertReadEnabled () ;
    mode->subEntityTraits().setSelectionMarker (1) ;
  AcDbCircle::subWorldDraw (mode);
    mode->subEntityTraits ().setSelectionMarker (2) ;
  mode->subEntityTraits ().setColor (1) ;
  mode->subEntityTraits ().setFillType (kAcGiFillAlways) ;
  mode->geometry().circle (center (), radius (), normal()) ;
    return Acad::eOk;
}
Then I make sure that if OSNAP is called on the filled circle (face/enclosed area) then it will fail:
Acad::ErrorStatus AsdkEntity::subGetOsnapPoints (
  AcDb::OsnapMode osnapMode,
  int gsSelectionMark,
  const AcGePoint3d &pickPoint,
  const AcGePoint3d &lastPoint,
  const AcGeMatrix3d &viewXform,
  AcGePoint3dArray &snapPoints,
  AcDbIntArray &geomIds) const
{
  assertReadEnabled () ;
  // do not allow snapping on the internal circle/face
  if (gsSelectionMark == 2)
    return Acad::eOk;
    return (AcDbCircle::subGetOsnapPoints (osnapMode, gsSelectionMark,
    pickPoint, lastPoint, viewXform, snapPoints, geomIds)) ;
}
Download Ducs

## 评论

**内容**: GlacierXie said...
however，this sample do not work in cad2014？It never call AcDbDynamicUCSPE::getCandidatePlanes()，Is not the mechanism has changed in 2014？
Reply
10/30/2016 at 09:59 PM

---
**内容**: Madhukar Moogala said...
Hi,
The said blog is a workaround to fix the behavior of retrieving Candidate planes on Non-Solid custom entities, but for custom-solids too we have seen the same behavior of not reporting Candidate planes, this behavior is under analysis with Engineering, do let me know. You can raise a ticket through ADN portal.
Reply
10/31/2016 at 03:22 AM

---
**内容**: jordan said...
How is this AcDbDynamicUCSPE implemented?
I have an existing Entity derived from AcDbEntity and I now want to implement the dynamic UCS behavior on my custom entities.
I cannot switch the base class of my existing entities (already in existing drawings).
So how do I do this/
Reply
09/09/2020 at 05:40 AM

---
