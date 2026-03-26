---
title: "Getting visual style properties used by the viewport"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Unicode
description: "I have a custom entity which implements subViewportDraw() and depending on the visual style, e.g. if it's using materials, my entity would draw its..."
author: Autodesk
---
# Getting visual style properties used by the viewport

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/getting-visual-style-properties-used-by-the-viewport.html

## 文章内容

By Adam Nagy
I have a custom entity which implements subViewportDraw() and depending on the visual style, e.g. if it's using materials, my entity would draw itself different. How could I get the visual style properties inside subViewportDraw()?
Solution
Using AcGiViewportDraw::viewportObjectId() you can get to the viewport/viewport record where your entity is drawing itself. And from there you can find out the visual style being used. Once you got the visual style you can reach all the properties you are interested in.
In the following sample my entity (AEN1MyEntity) is derived from AcDbEntity and in its subViewportDraw() it simply draws a text with some information about the visual style being used.
Note that kDrawableRegenDraw is returned in subSetAttributes(), so that our subViewportDraw() is called whenever there is some change in the viewport, inc. Visual Style change. Without this, if you changed between 3D visual styles, then subViewportDraw() would not be called and so the cached version of your entity would be used.
void AEN1MyEntity::subViewportDraw (AcGiViewportDraw *mode)
{
  AcString text = _T("default");
  switch (mode->regenType())
  {
  case eAcGiRegenTypeInvalid:
    text = _T("eAcGiRegenTypeInvalid");
    break;
  case kAcGiForExplode:
    text = _T("kAcGiForExplode");
    break;
  case kAcGiHideOrShadeCommand:
    text = _T("kAcGiHideOrShadeCommand");
    break;
  case kAcGiRenderCommand: /* = kAcGiShadedDisplay */
    text = _T("kAcGiRenderCommand");
    break;
  case kAcGiSaveWorldDrawForProxy:
    text = _T("kAcGiSaveWorldDrawForProxy");
    break;
  case kAcGiStandardDisplay:
    text = _T("kAcGiStandardDisplay");
    break;
  }
    AcDbObjectId idVp = mode->viewportObjectId();
  // If it's null then it must be a 2d view
  if (idVp.isNull())
  {
    text.append(_T(", 2D"));
  }
  else
  {
    text.append(_T(", "));
      AcDbObjectPointer ptrObj(idVp, AcDb::kForRead);
      AcDbObjectId id;
      if (ptrObj->isA() == AcDbViewport::desc())
    {
      AcDbViewport* pVp = AcDbViewport::cast(ptrObj);
        id = pVp->visualStyle();
    }
    else if (ptrObj->isA() == AcDbViewportTableRecord::desc())
    {
      AcDbViewportTableRecord* pVp =
        AcDbViewportTableRecord::cast(ptrObj);
        id = pVp->visualStyle();
    }
      AcDbObjectPointer ptrVS(id, AcDb::kForRead);
      text.append(ptrVS->description());
  }
    AcGeVector3d vecUp;
  mode->viewport().getCameraUpVector(vecUp);
    AcGeVector3d vecFlow =
    vecUp.crossProduct(mode->viewport().viewDir());
  AcGiTextStyle style;
  Acad::ErrorStatus err = fromAcDbTextStyle(style, _T("STANDARD"));
  Adesk::Boolean ret = mode->geometry().text(AcGePoint3d(0, 0, 0),
    mode->viewport().viewDir(), vecFlow, text, -1,
    Adesk::kTrue, style); 
}
  Adesk::UInt32 AEN1MyEntity::subSetAttributes (
  AcGiDrawableTraits *traits)
{
  assertReadEnabled () ;
  // kDrawableViewIndependentViewportDraw - get the
  // correct mode->regenType()
  // kDrawableRegenDraw - call our viewport in case of any change
  // - even if a property of the current visual style changed
  return (AcDbEntity::subSetAttributes (traits) |
    kDrawableViewIndependentViewportDraw | kDrawableRegenDraw);
}

## 评论

**内容**: Jorge Lopez said...
kDrawableRegenDraw is a performance issue as it regen's the object on every frame. It would be better to have a reactor watch for the modified visual style and then update the affected entities accordingly.
Reply
03/10/2022 at 10:47 AM

---
