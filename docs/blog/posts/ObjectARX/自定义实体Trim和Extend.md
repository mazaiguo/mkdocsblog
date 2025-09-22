---
title: 自定义实体Trim和Extend
date: 2024-03-12
categories:
  - windows程序
tags:
  - ObjectARX
  - Trim
  - Extend
description: ObjectARX中自定义实体支持Trim和Extend操作的实现方法
author: JerryMa
---

# 自定义实体Trim和Extend

## Derive from AcDbCurve and implement AcDbCurve virtual members.

## Extend

```cpp
	virtual Acad::ErrorStatus subGetStretchPoints(
		AcGePoint3dArray& stretchPoints) const;
	virtual Acad::ErrorStatus subMoveStretchPointsAt(
		const AcDbIntArray & indices,
		const AcGeVector3d& offset
```

实现以上两个函数

## Trim

```cpp
virtual Acad::ErrorStatus subIntersectWith(const AcDbEntity * ent,
		AcDb::Intersect intType,
		AcGePoint3dArray & points,
		Adesk::GsMarker thisGsMarker,
		Adesk::GsMarker otherGsMarker) const;
	virtual Acad::ErrorStatus subIntersectWith(
		const AcDbEntity* pEnt,
		AcDb::Intersect intType,
		const AcGePlane& projPlane,
		AcGePoint3dArray& points,
		Adesk::GsMarker thisGsMarker = 0,
		Adesk::GsMarker otherGsMarker = 0
	) const;
```

实现以上两个函数




