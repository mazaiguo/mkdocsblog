---
title: OverRule相关demo
date: 2024-11-05
categories:
  - windows程序
tags:
  - ObjectARX
  - OverRule
  - AutoCAD
  - 实体控制
description: ObjectARX中OverRule功能的详细实现demo，包含实体锁定和交互控制
author: JerryMa
---

# OverRule相关demo

![image-20241105105959744](http://image.jerryma.xyz//images/20241105-image-20241105105959744.png)

## 参考ADNblogdemo

[Locking an Entity in AutoCAD using ObjectARX](https://adndevblog.typepad.com/autocad/2012/06/locking-an-entity-in-autocad-using-objectarx.html)

`CGripOverrule.h`

```cpp
#pragma once
#include "dbentityoverrule.h"
class CGripOverrule : public AcDbGripOverrule
{
public:
	static CGripOverrule *_pTheOverrule;

	ACRX_DECLARE_MEMBERS(CGripOverrule);

	bool isApplicable(const AcRxObject *pOverruledSubject) const
	{

		return true;
	}

	// Add the overrule.

	// Take care about calling "CGripOverrule::rxInit();"

	// in "On_kInitAppMsg" of the arx that uses this overrule.

	static void CGripOverrule::AddOverrule()
	{
		if (_pTheOverrule != NULL)

			return;
		_pTheOverrule = new CGripOverrule();
		AcRxOverrule::addOverrule(AcDbCircle::desc(), _pTheOverrule, true);
		CGripOverrule::setIsOverruling(true);
	}

	static void CGripOverrule::RemoveOverrule()
	{
		if (_pTheOverrule == NULL)
			return;

		CGripOverrule::setIsOverruling(false);
		AcRxOverrule::removeOverrule(AcDbCircle::desc(), _pTheOverrule);
		delete _pTheOverrule;
		_pTheOverrule = NULL;
	}

	Acad::ErrorStatus CGripOverrule::getGripPoints(const AcDbEntity *pSubject,
												   AcGePoint3dArray &gripPoints,
												   AcDbIntArray &osnapModes,
												   AcDbIntArray &geomIds)
	{
		AcDbCircle *pCircle = AcDbCircle::cast(pSubject);
		if (pCircle != NULL)
		{ // Remove the grip points, for a circle

			gripPoints.removeAll();
			return Acad::eNotApplicable;
		}

		return AcDbGripOverrule::getGripPoints(pSubject, gripPoints, osnapModes, geomIds);
	}

	Acad::ErrorStatus CGripOverrule::getGripPoints(
		const AcDbEntity *pSubject,
		AcDbGripDataPtrArray &grips,
		const double curViewUnitSize,
		const int gripSize,
		const AcGeVector3d &curViewDir,
		const int bitflags)
	{
		AcDbCircle *pCircle = AcDbCircle::cast(pSubject);
		if (pCircle != NULL)
		{ // Remove the grip points, for a circle
			grips.removeAll();
			return Acad::eNotApplicable;
		}

		return AcDbGripOverrule::getGripPoints(
			pSubject,
			grips,
			curViewUnitSize,
			gripSize,
			curViewDir,
			bitflags);
	}
};

CGripOverrule *CGripOverrule::_pTheOverrule = NULL;
ACRX_NO_CONS_DEFINE_MEMBERS(CGripOverrule, AcDbGripOverrule);
```



`CTransformOverrule.h`

```cpp
#pragma once
#include "dbentityoverrule.h"
class CTransformOverrule :
	public AcDbTransformOverrule
{
public:
	static CTransformOverrule* _pTheOverrule;
	ACRX_DECLARE_MEMBERS(CTransformOverrule);
	bool isApplicable(const AcRxObject* pOverruledSubject) const
	{
		return true;
	}
	Acad::ErrorStatus transformBy(
		AcDbEntity* pSubject,
		const AcGeMatrix3d& xform)
	{
		if (pSubject->isA() != AcDbCircle::desc())
			return Acad::eOk;
		AcDbCircle* pCircle = AcDbCircle::cast(pSubject);
		if (pCircle != NULL)
			return Acad::eNotApplicable;
		return AcDbTransformOverrule::transformBy(pSubject, xform);
	}
	// Take care about calling "CTransformOverrule::rxInit();"
	// in "On_kInitAppMsg" of the arx that uses this overrule.
	static void CTransformOverrule::AddOverrule()
	{
		if (_pTheOverrule != NULL)
			return;
		_pTheOverrule = new CTransformOverrule();
		AcRxOverrule::addOverrule(
			AcDbCircle::desc(),
			_pTheOverrule,
			true
		);
		CTransformOverrule::setIsOverruling(true);
	}
	static void CTransformOverrule::RemoveOverrule()
	{
		if (_pTheOverrule == NULL)
			return;
		CTransformOverrule::setIsOverruling(false);
		AcRxOverrule::removeOverrule(
			AcDbCircle::desc(),
			_pTheOverrule);
		delete _pTheOverrule;
		_pTheOverrule = NULL;
	}
};
CTransformOverrule* CTransformOverrule::_pTheOverrule = NULL;
ACRX_NO_CONS_DEFINE_MEMBERS(CTransformOverrule, AcDbTransformOverrule);
```

`On_kInitAppMsg`

```cpp
virtual AcRx::AppRetCode On_kInitAppMsg (void *pkt)
{
    AcRx::AppRetCode retCode = AcRxArxApp::On_kInitAppMsg (pkt) ;
    CGripOverrule::rxInit();
    CTransformOverrule::rxInit();
    acrxBuildClassHierarchy();
    return (retCode) ;
}
```

`AddCommand`

```cpp
// Command to enable overruling
static void asdkOverrule_Start(void)
{
    CTransformOverrule::AddOverrule();
    CGripOverrule::AddOverrule();
}
// Command to disable overruling
static void asdkOverrule_Stop(void)
{
    CTransformOverrule::RemoveOverrule();
    CGripOverrule::RemoveOverrule();
}
```

## 增加CDrawCircleOverRule

`CDrawCircleOverRule.h`

```cpp
class CDrawCircleOverRule: public AcGiDrawableOverrule
{
public:
	CDrawCircleOverRule();
	~CDrawCircleOverRule();
	//ACRX_DECLARE_MEMBERS(CDrawCircleOverRule);
	virtual bool isApplicable(const AcRxObject* pOverruledSubject)  const;
	virtual Adesk::Boolean  worldDraw(AcGiDrawable* pSubject, AcGiWorldDraw * wd);
};
```

`CDrawCircleOverRule.cpp`

```cpp
#include "stdafx.h"
#include "CDrawCircleOverRule.h"
CDrawCircleOverRule::CDrawCircleOverRule()
{
}

CDrawCircleOverRule::~CDrawCircleOverRule()
{
}

bool CDrawCircleOverRule::isApplicable(const AcRxObject* pOverruledSubject)  const
{
	return true;
}

Adesk::Boolean CDrawCircleOverRule::worldDraw(AcGiDrawable* pSubject, AcGiWorldDraw * wd)
{
	AcDbCircle* pCircle = AcDbCircle::cast(pSubject);
	if (pCircle != nullptr)
	{
		AcGePoint3d cenPt = pCircle->center();
		double dRadius = pCircle->radius();

		AcDbLine pline;
		AcGePoint3d startPt, endPt;
		acutPolar(asDblArray(cenPt), PI, 1.5*dRadius, asDblArray(startPt));
		acutPolar(asDblArray(cenPt), 0, 1.5*dRadius, asDblArray(endPt));
		
		wd->geometry().circle(cenPt, dRadius, AcGeVector3d::kZAxis);
		wd->subEntityTraits().setColor(1);
		pline.setStartPoint(startPt);
		pline.setEndPoint(endPt);
		pline.worldDraw(wd);

		acutPolar(asDblArray(cenPt), PI/2, 1.5*dRadius, asDblArray(startPt));
		acutPolar(asDblArray(cenPt), 3*PI/2, 1.5*dRadius, asDblArray(endPt));
		pline.setStartPoint(startPt);
		pline.setEndPoint(endPt);
		pline.worldDraw(wd);

	}

	return Adesk::kTrue;
}
```

`AddCommand`

```cpp
CDrawCircleOverRule*  theOverrule = nullptr;

static void MyGroupStart() {
    // Put your command code here
    CTransformOverrule::AddOverrule();
    CGripOverrule::AddOverrule();
    if (theOverrule == nullptr)
    {
        theOverrule = new CDrawCircleOverRule();
        AcRxOverrule::addOverrule(AcDbCircle::desc(), theOverrule, true);
    }
    CDrawCircleOverRule::setIsOverruling(true);
}
static void MyGroupStop() {
    // Put your command code here
    CTransformOverrule::RemoveOverrule();
    CGripOverrule::RemoveOverrule();
    if (theOverrule != nullptr)
    {
        AcRxOverrule::removeOverrule(AcDbCircle::desc(), theOverrule);
        theOverrule = nullptr;
    }
}
```

