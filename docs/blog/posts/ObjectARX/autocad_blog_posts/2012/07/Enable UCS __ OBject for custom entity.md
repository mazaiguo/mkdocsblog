---
title: "Enable UCS >> OBject for custom entity"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Dimension
  - UCS
description: "Depending on what your entity is derived from, UCS >> OBject tries to get the UCS from the entity in different ways. If your entity is derived from..."
author: Autodesk
---
# Enable UCS >> OBject for custom entity

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/enable-ucs-object-for-custom-entity.html

## 文章内容

By Adam Nagy
Depending on what your entity is derived from, UCS >> OBject tries to get the UCS from the entity in different ways. If your entity is derived from AcDbEntity and it does not provide a NEAR snap point through getOsnapPoints(), then getEcs() will be called.
One thing to note is that the origin will be further transformed, which we can counter act so that if _ecs in the below example contains the exact coordinate system that we want, we can transform it before passing it back:
void MyEnt::getEcs(AcGeMatrix3d& retVal) const
{
  assertReadEnabled();
    // UCS >> OBject will do an
  // orig.transformBy(AcGeMatrix3d::worldToPlane(normal));
  // so we'll do here the reverse
  AcGeVector3d x, y, z;
  AcGePoint3d orig;
    _ecs.getCoordSystem(orig, x, y, z);

  orig = orig.transformBy(AcGeMatrix3d::worldToPlane(z).invert());  
    AcGeMatrix3d mx;
  retVal = mx.setCoordSystem(orig, x, y, z);
}

