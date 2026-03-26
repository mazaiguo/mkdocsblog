---
title: "Copy of AcDbRegion or AcDb3dSolid is NULL during dragging"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Solid
description: "If I derive a new class from AcDbRegion or AcDb3dSolid, the"
author: Autodesk
---
# Copy of AcDbRegion or AcDb3dSolid is NULL during dragging

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/copy-of-acdbregion-or-acdb3dsolid-is-null-during-dragging.html

## 文章内容

By Xiaodong Liang
Issue
If I derive a new class from AcDbRegion or AcDb3dSolid, the
isNull() member function returns True while the instance is being dragged. How can I work around this?
Solution
During dragging, AutoCAD creates a new copy of the entity each time the mouse moves to preserve accuracy. This poses a problem in the case of entities whose copy operation is time-intensive. AcDb3dSolid and AcDbRegion are two such entities and their copy operations are optimized during dragging to copy only the graphical cache they encapsulate and not the underlying ACIS data.
If you need the underlying ACIS data, the entity must detect if it is being copied because of dragging and the back pointer must be stored to the original entity to access the ACIS data.
For example if your object is derived from AcDbRegion, then you could have a member variable as follows:
   AcDbRegion* m_pDraggedInstance;

And then implement your copyFrom method as follows:
Acad::ErrorStatus MyEntity::copyFrom(const AcRxObject* pOther){
      assertWriteEnabled();
    Acad::ErrorStatus es = AcDbRegion::copyFrom(pOther);
    if( es!=Acad::eOk ){
        return es;
    }
    //detect that we lost our representation
    AcDbRegion* pSheet = AcDbRegion::cast(pOther);
    if (pSheet && isNull() && !pSheet->isNull())
        m_pDraggedInstance = pSheet;
    }
    return Acad::eOk;
}
You can now use the m_pDraggedInstance pointer to access the original region in the copy made for dragging.

