---
title: ObjectARX.net学习2-CLR托管C++类
date: 2024-08-20
categories:
  - windows程序
tags:
  - ObjectARX.net
  - CSharp
description: ObjectARX.net学习第二部分，CLR托管C++类的创建和使用方法
author: JerryMa
---

# ObjectARX.net学习（2）-CLR 托管C++ 类库

## 正常cpp项目

类代码如下所示：

```cpp
#pragma once
#ifndef LX_DLL_CLASS_EXPORTS
#define LX_DLL_CLASS __declspec(dllexport)
#else
#define LX_DLL_CLASS __declspec(dllimport)
#endif
#include <afx.h>
class LX_DLL_CLASS CSelCircleInfo
{
public:
	CSelCircleInfo();
	~CSelCircleInfo();
	CString sel();
	void test();
};
```

* 类库需要导出
* CString需要引入头文件

## 正常的clr项目

### 创建clr类库项目

### 加载cpp的头文件和库文件

### 设置信息

![image-20240425105414082](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2024/04/25_10_54_17_20240425-image-20240425105414082.png)

* 注意.net版本
* 由于cpp项目是MFC的dll，这里需要使用`在共享DLL中使用MFC`

代码如下所示：

```csharp
#pragma once
#include "CSelCircleInfo.h"

using namespace System;
namespace ClassLibrary1 {
	public ref class MgCSelCircleInfo
	{
	public:
		MgCSelCircleInfo() : nativeCSelCircleInfo(new CSelCircleInfo()) {}
		~MgCSelCircleInfo() { this->!MgCSelCircleInfo(); }
		!MgCSelCircleInfo() { delete nativeCSelCircleInfo; }

		System::String^ Sel()
		{
			CString str = nativeCSelCircleInfo->sel();
			return gcnew System::String(str.GetString());
			/*std::string str = nativeCSelCircleInfo->sel();
			String^ managedString = gcnew String(str.c_str());
			return managedString;*/
		}

		void Test()
		{
			nativeCSelCircleInfo->test();
		}

	private:
		CSelCircleInfo* nativeCSelCircleInfo; // 原生CSelCircleInfo类的实例指针
	};
}
```



## 正常的.net项目

### 引入clr创建的dll

### 代码中使用

* 先using导入类库

```csharp
ClassLibrary1.MgCSelCircleInfo mgCSelCircleInfo = new MgCSelCircleInfo();
            string strResult = mgCSelCircleInfo.Sel();
```



