---
title: "Toggling highlight state of an entity"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "Here is a sample ObjectARX code to toggle the highlight state of an entity."
author: Autodesk
---
# Toggling highlight state of an entity

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/toggling-highlight-state-of-an-entity.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample ObjectARX code to toggle the highlight state of an entity.
static void ToggleHighlight(void)
{
    ads_point pick;
    ads_name ename;
      int ret = acedEntSel(
                        ACRX_T("Select an entity :"),
                        ename,
                        pick
                    );
    if ( RTNORM != ret)
        return;
      Acad::ErrorStatus es;
    AcDbObjectId entId = AcDbObjectId::kNull;
    es = acdbGetObjectId( entId, ename );
    if ( Acad::eOk != es)
        return;
      AcDbEntity *pEnt = NULL;
    es = acdbOpenAcDbEntity (    pEnt,
                                entId,
                                AcDb::kForRead
                            );
      if ( Acad::eOk != es)
        return;
      AcDbFullSubentPath subPath;
    AcGiHighlightStyle hs = pEnt->highlightState(subPath);
      if(hs == AcGiHighlightStyle::kAcGiHighlightNone)
    {// Entity is not highlighted, lets highlight
        pEnt->highlight();
    }
    else
    {// Entity is already highlighted, lets unhighlight
        pEnt->unhighlight();
    }
    pEnt->close();
}

## 评论

**内容**: petcon said...
what these code for?
Reply
05/16/2012 at 09:54 PM

---
