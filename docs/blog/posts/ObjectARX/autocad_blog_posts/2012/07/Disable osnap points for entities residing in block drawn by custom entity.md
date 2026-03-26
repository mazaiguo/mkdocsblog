---
title: "Disable osnap points for entities residing in block drawn by custom entity"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Block
description: "We have a custom entity derived from AcDbEntity that draws a given block table record:"
author: Autodesk
---
# Disable osnap points for entities residing in block drawn by custom entity

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/disable-osnap-points-for-entities-residing-in-block-drawn-by-custom-entity.html

## 文章内容

By Adam Nagy
We have a custom entity derived from AcDbEntity that draws a given block table record:
Adesk::Boolean MyBlockEnt::subWorldDraw (AcGiWorldDraw *mode)
{
  assertReadEnabled();
    if (!m_blockId.isNull())
  {
    AcDbBlockTableRecordPointer ptrMB(m_blockId, AcDb::kForRead);
    mode->geometry().draw(ptrMB);
  }
    return (Adesk::kTrue);
}
We also implement the subGetOsnapPoints function to provide our own snap points:
Acad::ErrorStatus MyBlockEnt::subGetOsnapPoints(
  AcDb::OsnapMode osnapMode, Adesk::GsMarker gsSelectionMark,
  const AcGePoint3d& pickPoint, const AcGePoint3d& lastPoint,
  const AcGeMatrix3d& viewXform, AcGePoint3dArray& snapPoints,
  AcDbIntArray& geomIds, const AcGeMatrix3d& insertionMat) const
{
  snapPoints.append(m_snapPoint);
    return Acad::eOk;
}
In 2d Wireframe mode only the point we provide can be snapped to, which is the behaviour we'd like to see in the other modes like Shaded view as well. However, there the osnap points of the entities residing in the block our entity is drawing can also be snapped to. How could we avoid that?
Solution
Your entity should also implement the AcDbEntity::subIsContentSnappable like so:
bool MyBlockEnt::subIsContentSnappable() const
{
  return false;
}

## 评论

**内容**: Eric said...
Great job Adam.
I have a question, how to insert the entity in right position? Because by default the position always origin.
Thank you.
Reply
03/29/2014 at 07:45 AM

---
**内容**: Adam Nagy said...
Hi Eric,
Have a look at this:
http://adndevblog.typepad.com/autocad/2012/07/drawing-graphics-from-block-table-record-in-a-custom-entitys-worlddraw.html
Cheers,
Adam
Reply
03/29/2014 at 02:27 PM

---
**内容**: Eric said in reply to Adam Nagy...
Great, that's works,thank you Adam.
Reply
03/31/2014 at 05:18 PM

---
