---
title: "Get the layout an entity belongs to"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - AutoLISP
  - Block
  - C++
description: "I'm migrating my LISP project to ARX. In LISP I can use (entget) to find the layout name at group code 410. How can I do the same in ARX?"
author: Autodesk
---
# Get the layout an entity belongs to

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/get-the-layout-an-entity-belongs-to.html

## 文章内容

By Adam Nagy
I'm migrating my LISP project to ARX. In LISP I can use (entget) to find the layout name at group code 410. How can I do the same in ARX?
Solution
You need to get the owner block of the entity and from there you can get to the layout object.
static void ArxProject_GetLayout(void)
{
  ads_name name;
  ads_point pt;
  if (acedEntSel(L"Select an entity\n", name, pt) != RTNORM)
    return;
    AcDbObjectId id;
  acdbGetObjectId(id, name);
    AcDbEntityPointer ptrEnt(id, AcDb::kForRead);
  if (ptrEnt.openStatus() != Acad::eOk)
    return;
    AcDbBlockTableRecordPointer ptrBTR(ptrEnt->ownerId(), AcDb::kForRead);
  if (ptrBTR.openStatus() != Acad::eOk)
    return;
    AcDbObjectPointer<AcDbLayout> ptrLayout(ptrBTR->getLayoutId(), AcDb::kForRead);
  if (ptrLayout.openStatus() != Acad::eOk)
    return;
    const ACHAR* layoutName;
  ptrLayout->getLayoutName(layoutName);
    acutPrintf(L"The layout the selected entity belongs to is %s", layoutName);
}

## 评论

**内容**: Darrin Maidlow said...
Thanks for yet another helpful post!
Reply
08/05/2012 at 12:36 PM

---
