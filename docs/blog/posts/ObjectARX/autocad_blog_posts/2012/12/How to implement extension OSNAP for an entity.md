---
title: "How to implement extension OSNAP for an entity"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - API
description: "You can define a custom osnap like this:"
author: Autodesk
---
# How to implement extension OSNAP for an entity

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-implement-extension-osnap-for-an-entity.html

## 文章内容

By Gopinath Taget
You can define a custom osnap like this:
//-------------------------------------------------------------------
// Osnap classes
  class MkrInfo : public AcDbCustomOsnapInfo
{
public:
    ACRX_DECLARE_MEMBERS(MkrInfo);
      Acad::ErrorStatus   getOsnapInfo(
     AcDbEntity*           pickedObject,
     Adesk::GsMarker       gsSelectionMark,
     const AcGePoint3d&    pickPoint,
     const AcGePoint3d&    lastPoint,
     const AcGeMatrix3d&   viewXform,
     AcArray<AcGePoint3d>& snapPoints,
     AcDbIntArray &     geomIdsForPts,
     AcArray<AcGeCurve3d*>& snapCurves,
     AcDbIntArray &     geomIdsForLines);
};
      ACRX_CONS_DEFINE_MEMBERS(MkrInfo, AcDbCustomOsnapInfo, 1);
    Acad::ErrorStatus
MkrInfo::getOsnapInfo(
AcDbEntity*           pickedObject,
Adesk::GsMarker       gsSelectionMark,
 const AcGePoint3d&    pickPoint,
 const AcGePoint3d&    lastPoint,
 const AcGeMatrix3d&   viewXform,
AcArray<AcGePoint3d>& snapPoints,
AcDbIntArray &     geomIdsForPts,
AcArray<AcGeCurve3d*>& snapCurves,
AcDbIntArray &     geomIdsForLines
)
{
    AsDkCurve *p = AsDkCurve::cast(pickedObject);
    if (NULL != p)
    {
        AcGeLineSeg3d *pls1 = new AcGeLineSeg3d;
  AcGePoint3d startP, endP;
  p->startPoint(startP);
  p->m_endPoint(endP);
        pls1->set(startP, (endP - startP));
        snapCurves.append(pls1);
          AcGeLineSeg3d *pls2 = new AcGeLineSeg3d;
        pls2->set(endP, (endP - startP));
        snapCurves.append(pls2);
    }
    return Acad::eOk;
}
    //static
MkrInfo _mkrInfo;
    class MkrMode : public AcDbCustomOsnapMode
{
public:
    const TCHAR* localModeString() const;
    const TCHAR* globalModeString() const;
    const AcRxClass* entityOsnapClass() const;
    AcGiGlyph* glyph() const;
    const TCHAR*               tooltipString() const;
};
  const TCHAR*
MkrMode::localModeString() const
{
    return _T("XTNd");
}
  const TCHAR*
MkrMode::globalModeString() const
{
    return _T("_XTNd");
}
  const AcRxClass*
MkrMode::entityOsnapClass() const
{
    return MkrInfo::desc();
}
  class MyGlyph : public AcGiGlyph
{
public:
    Acad::ErrorStatus setLocation(const AcGePoint3d& dcsPoint);
    void subViewportDraw(AcGiViewportDraw* vportDrawContext);
private:
    AcGePoint3d m_point;
};
  Acad::ErrorStatus
MyGlyph::setLocation(const AcGePoint3d& dcsPoint)
{
    m_point = dcsPoint;
    return Acad::eOk;
}
    void
MyGlyph::subViewportDraw(AcGiViewportDraw* p)
{
    // not needed for ext-like snaps
}
  AcGiGlyph*
MkrMode::glyph() const
{
    static MyGlyph mg;
    return &mg;
}
  const TCHAR*
MkrMode::tooltipString() const
{
    return _T("Custom Extend");
}
  MkrMode _mkrMode;
And you can register a custom osnap to associate with with an entity as follows:
//Register protocol extension object (customOsnapInfo)
MkrInfo::rxInit();
acrxBuildClassHierarchy();
AcDbEntity::desc()->addX(MkrInfo::desc(), &_mkrInfo);
acdbCustomOsnapManager()->addCustomOsnapMode(&_mkrMode);
And unregister as follows:
//Remove protocol extension object
acdbCustomOsnapManager()->removeCustomOsnapMode(&_mkrMode);
AcDbEntity::desc()->delX(MkrInfo::desc());
deleteAcRxClass(MkrInfo::desc());

