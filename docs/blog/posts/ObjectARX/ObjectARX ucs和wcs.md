---
title: ObjectARX UCS和WCS
date: 2024-06-18
categories:
  - CAD开发
  - ObjectARX
  - 坐标系统
tags:
  - ObjectARX
  - UCS
  - WCS
  - 坐标转换
description: ObjectARX中用户坐标系（UCS）和世界坐标系（WCS）之间的转换方法
author: JerryMa
---

# ObjectARX ucs和wcs

## ucs和wcs转换

| No   | Description                                                  |
| ---- | ------------------------------------------------------------ |
| 0    | World (WCS)                                                  |
| 1    | User (current UCS)                                           |
| 2    | Display:DCS of current viewport when used with code 0 or  1DCS of current model space viewport when used with code 3 |
| 3    | Paper space DCS (PSDCS; used only with code 2)               |

```cpp
//0表示wcs 1表示ucs 2 DCS, 3 PSDCS
AcGePoint3d CGlobalHelper::TransformPoint(const AcGePoint3d &point, int nFromType, int nToType)
{
	AcGePoint3d pt;
	//从ucs转到wcs
	struct resbuf rbFrom, rbTo;
	rbFrom.restype = RTSHORT;
	rbFrom.resval.rint = nFromType; // from wcs
	rbTo.restype = RTSHORT;
	rbTo.resval.rint = nToType;     // from ucs
	acedTrans(asDblArray(point), &rbFrom, &rbTo, Adesk::kFalse, asDblArray(pt));
	return pt;
}

```

## 常见的wcs

### AcDbEntity中存储和返回的都是wcs，比如

```cpp
//直线 点都必须在WCS坐标中
AcDbLine(const AcGePoint3d& start, const AcGePoint3d& end);
 
//圆 中心和法向量必须是WCS坐标
AcDbCircle(const AcGePoint3d& cntr, const AcGeVector3d& nrm, double radius);
 
//圆弧 中心必须位于WCS坐标中
AcDbArc(const AcGePoint3d& center, const AcGeVector3d& normal, double radius, double startAngle, double endAngle);
 
//多段线 注意！！！点必须位于ECS坐标中
AcDbPolyline::addVertexAt(unsigned int index,  const AcGePoint2d& pt, double bulge = 0., double startWidth = -1.,  double endWidth = -1., Adesk::Int32 vertexIdentifier = 0);
 
//椭圆 中心必须位于WCS坐标中
AcDbEllipse( const AcGePoint3d& center, const AcGeVector3d& unitNormal, const AcGeVector3d& majorAxis, double radiusRatio, double startAngle = 0.0, double endAngle = 2*PI);
 
//引线 点必须位于WCS坐标中
AcDbLeader::appendVertex(const AcGePoint3d&);


```

#### view相关的点也是wcs

```cpp
void CGlobalHelper::ZOOMWINDOW(AcGePoint3d minPt, AcGePoint3d maxPt)
{
	// get the extents of the drawing
	AcDbViewTableRecord view;

	AcGePoint2d max_2d(maxPt[X], maxPt[Y]);
	AcGePoint2d min_2d(minPt[X], minPt[Y]);
	// now set the view centre point
	view.setCenterPoint(min_2d + (max_2d - min_2d) / 2.0);
	// now height and width of view
	view.setHeight(max_2d[Y] - min_2d[Y]);
	view.setWidth(max_2d[X] - min_2d[X]);
	// set the view
	acedSetCurrentView(&view, NULL);
	// updates the extents
	acdbHostApplicationServices()->workingDatabase()->updateExt(TRUE);
}
```


### jig中交互的点都是wcs

```cpp
//WCS 
//JIG获取点，即传入的basePnt、返回的resPnt 均为WCS中的点
AcEdJig::acquirePoint(AcGePoint3d& resPnt , const AcGePoint3d& basePnt);
 
//JIG获取角度，即传入的basePnt为WCS中的点
AcEdJig::acquireAngle( double & ang, const AcGePoint3d& basePnt);
 
//JIG获取距离，即传入的basePnt为WCS中的点
AcEdJig::acquireDist( double & dist, const AcGePoint3d& basePnt);
```

## 常见的UCS

### 常用API接口返回参数

```cpp
//UCS
//获取点，即传入的pt、返回的result均为UCS中的点
int acedGetPoint(const ads_point pt, const ACHAR * prompt, ads_point result);
 
//获取实体，返回的ptres均为UCS中的点
int acedEntSel(const ACHAR * str, ads_name entres, ads_point ptres);
 
//获取角度，传入的pt为UCS中的点
int acedGetAngle(const ads_point pt, const ACHAR * prompt, ads_real * result);
 
//获取距离，传入的pt为UCS中的点
int acedGetDist(const ads_point pt, const ACHAR * prompt, ads_real * result);
 
//动态拖拽移动 ，即传入的pmt、回调函数中的pt、返回的p均为UCS中的点
int acedDragGen(const ads_name ss, const ACHAR * pmt, int cursor, int (*scnf) (ads_point pt, ads_matrix mt), ads_point p);

AcDbMText::rotation 
```

//传入的点是ucs，这个比较`重要`

```cpp
int nRet = acedSSGet(_T("C"), asDblArray(minPt), asDblArray(maxPt), rb, ssname);
```

AcDbMText::rotation  `setRotation`  这里的角度是相对于UCS的x轴，所以需要处理，特别注意

## DCS

目前已知的dcs就是plot中的点坐标

```cpp
struct resbuf rbFrom, rbTo;
rbFrom.restype = RTSHORT;
rbFrom.resval.rint = 0; // from WCS
rbTo.restype = RTSHORT;
if (m_bISModelType)
{
    rbTo.resval.rint = 2; // to dcs
}
else
{
    rbTo.resval.rint = 2; // to pdcs
    acedTrans(asDblArray(maxPt), &rbFrom, &rbTo, Adesk::kFalse, asDblArray(maxPt));
    acedTrans(asDblArray(minPt), &rbFrom, &rbTo, Adesk::kFalse, asDblArray(minPt));
    rbFrom.resval.rint = 2; // from UCS
    rbTo.resval.rint = 3;
}
int nCvport = 2;
utils.GetVar(_T("CVPORT"), &nCvport);
if (nCvport >= 2)
{
    acedTrans(asDblArray(maxPt), &rbFrom, &rbTo, Adesk::kFalse, asDblArray(maxPt));
    acedTrans(asDblArray(minPt), &rbFrom, &rbTo, Adesk::kFalse, asDblArray(minPt));
}

es = pPSV->setPlotWindowArea(pPlotSettings, minPt.x, minPt.y, maxPt.x, maxPt.y);
```

## 未完待补充

其它的wcs和ucs的待补充

### GetClosestPointTo() on a BlockReference returns which coordinate system in AutoCAD using ObjectARX

#### **Issue**

`Why are the coordinates of a closest point (using GetClosestPointTo()) obtained from a block reference relative to neither WCS nor UCS?`

#### **Solution**

```html
The points that you receive are relative to the coordinate system of the owning
AcDbBlockTableRecord. If you want to convert them to coordinate system of the
AcDbBlockTableRecord in which you have the AcDbBlockReference, you must
transform them by the AcDbBlockReference::blockTransform().

You probably first want to transform the "specified point" by the inverse of
AcDbBlockReference::blockTransform(), do the closest point calculation, then
convert the resulting point back to the original space.
```
