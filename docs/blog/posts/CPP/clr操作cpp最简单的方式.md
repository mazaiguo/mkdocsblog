---
title: CLR操作CPP最简单的方式
date: 2024-07-25
categories:
  - windows程序
tags:
  - CLR
  - CPP
  - CSharp
description: CLR与CPP混合编程的简单实现方式，包含DLL封装和调用方法
author: JerryMa
---

# clr操作cpp最简单的方式

## 创建cpp代码

`导出需要使用的代码`

在cpp中先封装一次

`CFuncHelper.h`

```cpp
#pragma once
#ifdef ZWWHFORJTSERIALNOLABEL_MODULE
#define DLLIMPEXP __declspec(dllexport)
#else
#define DLLIMPEXP
#endif
class DLLIMPEXP CFuncHelper
{
public:
	CFuncHelper();
	~CFuncHelper();

	bool generateNo();
};


```

`CFuncHelper.cpp`

```cpp
#include "stdafx.h"
#include "CFuncHelper.h"
#include "CGenerateSerialNo.h"
#include "CGlobalHelper.h"
#include "CSelCSerialNo.h"
#include "CCoordinateInfoJig.h"


CFuncHelper::CFuncHelper()
{
}


CFuncHelper::~CFuncHelper()
{
}

bool CFuncHelper::generateNo()
{
	CGenerateSerialNo gen;
	if (!gen.doIt())
	{
		return false;
	}
	gen.drawSerialNoByInfo();
	AcGePoint3d basePt = gen.basePt();

	AcDbExtents exts = CGlobalHelper::getFrameExtsbyPoint(basePt);
	CGlobalHelper::ZOOMWINDOW(exts.minPoint(), exts.maxPoint());
	AcGePoint3d minPt, maxPt;
	minPt = CGlobalHelper::TransformPoint(exts.minPoint(), 0, 1);
	maxPt = CGlobalHelper::TransformPoint(exts.maxPoint(), 0, 1);
	exts.set(minPt, maxPt);
	CSelCSerialNo sel;
	sel.setExtents(exts);
	resbuf *rb = acutBuildList(
		-4, _T("<and"), RTDXF0, CBaseConstant::SERIAL_NO, -4, _T("and>"),
		RTNONE); // Simplification for apparent list
	if (!sel.selEnt(rb))
	{
		return false;
	}

	vector<CDimInfo> vecInfo = sel.data();
	if (vecInfo.size() < 1)
	{
		return false;
	}

	CCoordinateInfoJig *jig = new CCoordinateInfoJig();
	jig->startJig(vecInfo);
	return true;
}
```

## 创建Clr代码

![image-20241202083011439](http://image.jerryma.xyz//images/20241202-image-20241202083011439.png)

`clrDemo.h`

```cpp
#pragma once
#include "CFuncHelper.h"
using namespace System;

namespace clrDemo {
	public ref class ManageExport
	{
	public:
		ManageExport() : nativeCSelCircleInfo(new CFuncHelper()) {}
		~ManageExport() { this->!ManageExport(); }
		!ManageExport() { delete nativeCSelCircleInfo; }
		bool Test()
		{
			return nativeCSelCircleInfo->generateNo();
		}

	private:
		CFuncHelper* nativeCSelCircleInfo; // 原生CSelCircleInfo类的实例指针

	};
}
```

## Csharp中引入clr生成的dll