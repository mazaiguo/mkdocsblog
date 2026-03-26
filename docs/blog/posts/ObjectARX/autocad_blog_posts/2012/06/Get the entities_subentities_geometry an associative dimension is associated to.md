---
title: "Get the entities/subentities/geometry an associative dimension is associated to"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Dimension
  - Solid
description: "I would like to find out programmatically what geometry a specific dimension is associated to. How could I do it?"
author: Autodesk
---
# Get the entities/subentities/geometry an associative dimension is associated to

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/get-the-entitiessubentitiesgeometry-an-associative-dimension-is-associated-to.html

## 文章内容

By Adam Nagy
I would like to find out programmatically what geometry a specific dimension is associated to. How could I do it?
Solution
You can use acdbGetDimAssocId to find the AcDbDimAssoc object that holds the information you're looking for.
You need to include these header files in your project:
#include "dbdimassoc.h"
#include "dbdimptref.h"
The following function highlights the geometry that the selected dimension is associated to. I tested it with an associative dimension created on a solid box and the below function highlighted the edges nicely.
static void MyArxProject_HighlightAssociatedSubentities(void)
{
  ads_name name;
  ads_point pt;
  if (acedEntSel(L"Select associative dimension", name, pt) != RTNORM)
    return;
    AcDbObjectId dimId;
  acdbGetObjectId(dimId, name);
    AcDbObjectId assocId;
  acdbGetDimAssocId(dimId, assocId);
    if (assocId.isNull())
    return;
    AcDbObjectPointer<AcDbDimAssoc> ptrAssoc(assocId, AcDb::kForRead);
  for (int i = 0; i < 2; i++)
  {
    const AcDbPointRef* pt = ptrAssoc->pointRef(i);
      AcDbFullSubentPathArray subs;
    pt->getEntities(subs);
      for (int j = 0; j < subs.logicalLength(); j++)
    {
      AcDbEntityPointer ptrEnt(subs[j].objectIds().first(), AcDb::kForRead);
      ptrEnt->highlight(subs[j]);
    }
  }
}

## 评论

**内容**: ahlzl said...
thanks!
and how to create associative dimension by AcDbDimAssoc?
Reply
06/28/2012 at 03:49 AM

---
**内容**: converlisp said...
This routine has bugs.
in autocad2013 (CPU 32 bytes) has bugs........
The function "acdbGetDimAssocId(dimId, assocId)" return error 16 in drawing 2D and 3D
Reply
12/01/2012 at 02:51 PM

---
**内容**: Adam Nagy said...
Hi,
It seems to work in my AutoCAD MEP 2013.
See video: http://www.screencast.com/t/TTqnEIMEzg
Cheers,
Adam
Reply
12/07/2012 at 08:16 AM

---
