---
title: ARX动态块相关操作
date: 2024-03-08
categories:
  - CAD开发
  - ObjectARX
  - CPP
tags:
  - ObjectARX
  - AcDbDynBlockReference
  - AutoCAD
description: ObjectARX中获取AutoCAD背景颜色的两种实现方法和代码示例
author: JerryMa
---


# ARX动态块相关操作
![image-20240322164856228](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2024/03/22_16_48_57_20240322-image-20240322164856228.png)

第一个直接传入块参照的id即可创建AcDbDynBlockReference对象，便可对该块参照进行数据获取和修改。
第二个传入的是块参照的指针，如果该指针是以读打开的，该AcDbDynBlockReference对象只能进行数据读取，不能修改该块参照。

---

## 得到动态块参照的自定义属性

``` cpp
std::map<CString, CString>  GetCustomParam(const AcDbObjectId& idBlkRef)
{
	std::map<CString, CString> mapName;
	
	AcDbDynBlockReferencePropertyArray DynBlkRefPropArray;	//动态块参照属性数组
	AcDbDynBlockReference DynBlkRef(idBlkRef);			//动态块参照对象
	DynBlkRef.getBlockProperties(DynBlkRefPropArray);
	AcDbDynBlockReferenceProperty DynBlockReferenceProp;	//动态块参照属性
	
	for (int i = 0; i < DynBlkRefPropArray.length(); i++)
	{
		DynBlockReferenceProp = DynBlkRefPropArray.at(i);

		bool bShow = DynBlockReferenceProp.show();			//是否在面板中显示
		auto type = DynBlockReferenceProp.propertyType();	//属性类型
		CString strName = DynBlockReferenceProp.propertyName().kwszPtr();	//属性名
		if (true == bShow)
		{
			
			CString strValue;
			AcDbEvalVariant value = DynBlockReferenceProp.value();//值
			if (DwgDataType::kDwgText == type)
			{
				strValue = value.resval.rstring;
			}
			else if (DwgDataType::kDwgReal == type)
			{
				strValue.Format(_T("%.2f"), value.resval.rreal);
			}
			mapName[strName] = strValue;
		}
	}
	return mapName;
}

```

其中，AcDbDynBlockReferenceProperty::value函数只能得到该属性当前设置的值。
对于多种数据这种情况，可以使用AcDbDynBlockReferenceProperty::getAllowedValues函数。

---

## 设置块参照的自定义属性

``` cpp
bool SetCustomParam(const AcDbObjectId& idBlkRef,const std::map<CString, CString>& mapParam)
{
	AcDbDynBlockReferencePropertyArray DynBlkRefPropArray;	//动态块参照属性数组
	AcDbDynBlockReference DynBlkRef(idBlkRef);			//动态块参照对象
	DynBlkRef.getBlockProperties(DynBlkRefPropArray);
	AcDbDynBlockReferenceProperty DynBlockReferenceProp;	//动态块参照属性

	std::map<CString, CString>::const_iterator iter;
	for (iter = mapParam.begin(); iter != mapParam.end(); ++iter)
	{
		CString strKey = iter->first;
		CString strValue = iter->second;
		for (int i = 0; i < DynBlkRefPropArray.length(); i++)
		{
			DynBlockReferenceProp = DynBlkRefPropArray.at(i);

			bool bShow = DynBlockReferenceProp.show();			//是否在面板中显示
			if (false == bShow && DynBlockReferenceProp.readOnly() == true)
				continue;
			CString strName = DynBlockReferenceProp.propertyName().kwszPtr();	//属性名
			if (strName != strKey)
				continue;
			auto type = DynBlockReferenceProp.propertyType();	//属性类型
			if (DwgDataType::kDwgText == type)
			{
				AcDbEvalVariant value(strValue);
				DynBlockReferenceProp.setValue(value);
			}
			else if (DwgDataType::kDwgReal == type)
			{
				AcDbEvalVariant value(_wtof(strValue));
				DynBlockReferenceProp.setValue(value);
			}
		}
	}

	return true;
}
```


