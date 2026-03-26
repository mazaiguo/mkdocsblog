---
title: "Ensuring that two custom entities are copied together"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I have two custom entities: mywall and mydoor, and I would like to make sure that if mywall is copied then mydoor is copied with it when using CTRL..."
author: Autodesk
---
# Ensuring that two custom entities are copied together

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/ensuring-that-two-custom-entities-are-copied-together.html

## 文章内容

By Adam Nagy
I have two custom entities: mywall and mydoor, and I would like to make sure that if mywall is copied then mydoor is copied with it when using CTRL+C/CTRL+V.
Solution
In this case you just need to add an AcDbHardPointerId member to mywall entity, which would reference mydoor:
class DLLIMPEXP MyWall : public AcDbEntity
{
public: AcDbHardPointerId m_doorId;
  //...
You also need to make sure that this id is filed properly both in dwgOutFields and dwgInFields of MyWall.
Acad::ErrorStatus MyWall::dwgOutFields(AcDbDwgFiler *pFiler) const
{
  assertReadEnabled();
  Acad::ErrorStatus es = AcDbEntity::dwgOutFields(pFiler);
  if (es != Acad::eOk)
    return (es);
  if ((es =pFiler->writeUInt32(MyWall::kCurrentVersionNumber))
    != Acad::eOk)
    return (es);
  pFiler->writeHardPointerId(m_doorId); // HERE
    return (pFiler->filerStatus());
}
  Acad::ErrorStatus MyWall::dwgInFields(AcDbDwgFiler *pFiler)
{
  assertWriteEnabled();
  Acad::ErrorStatus es =AcDbEntity::dwgInFields(pFiler);
  if (es != Acad::eOk)
    return (es);
  Adesk::UInt32 version = 0;
  if ((es =pFiler->readUInt32 (&version)) != Acad::eOk)
    return (es) ;
  if (version > MyWall::kCurrentVersionNumber)
    return (Acad::eMakeMeProxy);
  pFiler->readHardPointerId(&m_doorId); // HERE
    return (pFiler->filerStatus());
}

