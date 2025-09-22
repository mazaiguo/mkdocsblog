---
title: ARX获取CAD背景色的两种方法
date: 2024-03-08
categories:
  - windows程序
tags:
  - ObjectARX
  - acedGetRGB

description: ObjectARX中获取AutoCAD背景颜色的两种实现方法和代码示例
author: JerryMa
---

# 获取ACAD背景色的两种方案：

* 在这种情况下，我们可以使用函数**unsigned long acedGetRGB(int color);** 使用参数 0 来获取背景颜色。
* 另一种选择是使用 acedGetCurrentColors 函数，您可以从中获取 dwGfxModelBkColor 和 dwGfxLayoutBkColor 并（取决于tilemode值）使用您需要的。

## ==acedGetRGB==

```cpp
void CWHASSET::drawWipeOut(AcDbExtents exts, AcGiWorldDraw *mode)
{
	if (showFramFlag())
	{
		AcGePoint3d minPt, maxPt;
		minPt = exts.minPoint();
		maxPt = exts.maxPoint();
		AcGePoint3dArray wipePnts;
		wipePnts.append(minPt);
		wipePnts.append(AcGePoint3d(minPt.x, maxPt.y, minPt.z));
		wipePnts.append(maxPt);
		wipePnts.append(AcGePoint3d(maxPt.x, minPt.y, maxPt.z));
		wipePnts.append(minPt);
		Adesk::UInt32 lColor = acedGetRGB(0);
		//UInt32需要转化成rgb数据
		int R = 0xFF & lColor;
		int G = 0xFF00 & lColor;
		G >>= 8;
		int B = 0xFF0000 & lColor;
		B >>= 16;AcCmEntityColor cmColor;
        cmColor.setRGB(R, G, B);
        mode->subEntityTraits().setTrueColor(cmColor);
        mode->subEntityTraits().setFillType(kAcGiFillAlways);
        mode->geometry().polygon(wipePnts.length(), wipePnts.asArrayPtr());
	}
}
```


## acedGetCurrentColors 

```cpp
void CWHASSET::drawWipeOut(AcDbExtents exts, AcGiWorldDraw *mode)
{
	if (showFramFlag())
	{
		AcGePoint3d minPt, maxPt;
		minPt = exts.minPoint();
		maxPt = exts.maxPoint();
		AcGePoint3dArray wipePnts;
		wipePnts.append(minPt);
		wipePnts.append(AcGePoint3d(minPt.x, maxPt.y, minPt.z));
		wipePnts.append(maxPt);
		wipePnts.append(AcGePoint3d(maxPt.x, minPt.y, maxPt.z));
		wipePnts.append(minPt);
		AcColorSettings colorSetings; 
		acedGetCurrentColors(&colorSetings);
		AcCmEntityColor bgColor;
		if (!mode->context()->isPlotGeneration())
		{
			COLORREF rgbColor = (COLORREF)colorSetings.dwGfxModelBkColor;
			int red = rgbColor & 255;
			int green = rgbColor >> 8 & 255;
			int blue = rgbColor >> 16 & 255;
			bgColor.setRed(red);
			bgColor.setBlue(blue);
			bgColor.setGreen(green);
			mode->subEntityTraits().setTrueColor(bgColor);
		}
		else
		{
			COLORREF rgbColor = (COLORREF)colorSetings.dwGfxLayoutBkColor;
			int red = rgbColor & 255;
			int green = rgbColor >> 8 & 255;
			int blue = rgbColor >> 16 & 255;
			bgColor.setRed(red);
			bgColor.setBlue(blue);
			bgColor.setGreen(green);
			mode->subEntityTraits().setTrueColor(bgColor);
		}

		mode->subEntityTraits().setFillType(kAcGiFillAlways);
		mode->geometry().polygon(wipePnts.length(), wipePnts.asArrayPtr());
	}
}
```

