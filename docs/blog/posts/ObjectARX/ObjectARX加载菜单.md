---
title: ObjectARX加载菜单
date: 2024-07-03
categories:
  - CAD开发
  - ObjectARX
  - CPP
tags:
  - ObjectARX
  - AutoCAD
  - 菜单
  - cpp
description: ObjectARX开发中动态加载和创建菜单的实现方法和代码示例
author: JerryMa
---

# ObjectARX加载菜单

## 使用ObjectARX有几种加载菜单的方式

### 使用aced函数加载

`LocadMenu.h`

```cpp
#pragma once
#include "stdafx.h"

class Menu
{
public:
	Menu();
	~Menu();
	static bool    IsFileExists(LPCTSTR szPath);
	static CString GetFolder(LPCTSTR szPath);
	static CString GetCurDir();
	static CString FindConPath(CString FileName);
	static void    CLoadMenu(CString sName, CString szPath);
	static void    CUnLoadMenu(CString sName, CString szPath);
	static void    RemoveMenuCache(CString sName, CString szPath);
};
```

`LocadMenu.cpp`

```cpp
#include "stdafx.h"
#include "LoadMenu.h"

Menu::Menu() {}

Menu::~Menu() {}

bool Menu::IsFileExists(LPCTSTR szPath)
{
	CFileStatus st;
	return CFile::GetStatus(szPath, st);
}

CString Menu::GetFolder(LPCTSTR szPath)
{
	CString strPath(szPath);
	strPath.TrimRight(_T("\\/"));

	int pos = strPath.ReverseFind(_T('\\'));
	int pos2 = strPath.ReverseFind(_T('/'));
	pos = max(pos, pos2);

	if (pos < 0)
	{
		return _T("");
	}

	return strPath.Left(pos + 1);
}

CString Menu::GetCurDir()
{
	TCHAR szPath[_MAX_PATH];
	::GetModuleFileName(_hdllInstance, szPath, _MAX_PATH);

	TCHAR szDrive[_MAX_DRIVE];
	TCHAR szDir[_MAX_DIR];
	TCHAR szFname[_MAX_FNAME];
	TCHAR szExt[_MAX_EXT];
	_tsplitpath_s(szPath, szDrive, szDir, szFname, szExt);

	return CString(szDrive) + szDir;
}

CString Menu::FindConPath(CString FileName)
{
	CString sDir = GetCurDir();

	CString sPath = sDir + FileName;
	while (!IsFileExists(sPath))
	{
		sDir = GetFolder(sDir);
		if (sDir.IsEmpty())
		{
			return _T("");
		}

		sPath = sDir + FileName;
	}
	return sPath;
}

void Menu::CLoadMenu(CString sName, CString szPath)
{
	//加载菜单
	if (!acedIsMenuGroupLoaded(sName))
	{
		CString str;

		str = FindConPath(szPath + _T(".cuix"));
		if (str.IsEmpty())
		{
			str = FindConPath(szPath + _T(".mnu"));
		}

		acedLoadPartialMenu(str);
	}
}

void Menu::CUnLoadMenu(CString sName, CString szPath)
{
	//卸载菜单
	if (acedIsMenuGroupLoaded(sName))
	{
		CString str;

		str = FindConPath(szPath + _T(".cuix"));
		if (str.IsEmpty())
		{
			str = FindConPath(szPath + _T(".mnu"));
		}

		acedUnloadPartialMenu(str);
	}
}

void Menu::RemoveMenuCache(CString sName, CString szPath)
{
	if (acedIsMenuGroupLoaded(sName))
	{
		CString str;

		str = FindConPath(szPath + _T(".cuix"));
		if (str.IsEmpty())
		{
			return;
		}
		int   len = WideCharToMultiByte(CP_ACP, 0, str, -1, NULL, 0, NULL, NULL);
		char* ptxtTemp = new char[len + 1];
		WideCharToMultiByte(CP_ACP, 0, str, -1, ptxtTemp, len, NULL, NULL);
		remove(ptxtTemp);
		delete[] ptxtTemp;
	}
}
```

`使用方式`

```cpp
virtual AcRx::AppRetCode On_kInitAppMsg(void *pkt)
{
	// You *must* call On_kInitAppMsg here
	AcRx::AppRetCode retCode = AcRxArxApp::On_kInitAppMsg(pkt);
	Menu::CUnLoadMenu(_T("SHRoad"), _T("Library\\Menu\\SHGLJTDZKFXM"));
	Menu::CLoadMenu(_T("SHRoad"), _T("Library\\Menu\\SHGLJTDZKFXM"));

	return (retCode);
}

virtual AcRx::AppRetCode On_kUnloadAppMsg(void *pkt)
{
	AcRx::AppRetCode retCode = AcRxArxApp::On_kUnloadAppMsg(pkt);
	Menu::CUnLoadMenu(_T("SHGLJTDZKFXM"), _T("Library\\Menu\\SHGLJTDZKFXM"));
	return (retCode);
}
```

### 第二种方式使用com加载

```cpp
#include "CAcadApplication.h"
#include "CAcadDocument.h"
#include "CAcadMenuBar.h"
#include "CAcadMenuGroup.h"
#include "CAcadMenuGroups.h"
#include "CAcadPopupMenu.h"
#include "CAcadPopupMenus.h"
//加载cui文件
bool LoadPartialMenu(
	const TCHAR* filePath //局部菜单文件名
	,
	const TCHAR* menuGroupName)

{
	//如果有的话先卸载

	long menuGroupNum; //菜单组数目

	VARIANT index;

	VariantInit(&index);

	index.vt = VT_I4;

	CString strGroupName(menuGroupName);

	CAcadApplication acadApp(acedGetAcadWinApp()->GetIDispatch(TRUE));

	CAcadMenuGroups menuGroups(acadApp.get_MenuGroups());

	CAcadMenuGroup menuGroup;

	menuGroupNum = menuGroups.get_Count();

	for (long i = 0; i < menuGroupNum; i++)
	{
		index.lVal = i;

		menuGroup = menuGroups.Item(index);
		CString strName = menuGroup.get_Name();
		if (strName.CompareNoCase(strGroupName) == 0)
		{
			menuGroup.Unload();

			break;
			//return false;
		}
	}

	//加载菜单

	VARIANT BaseMenu; //是否加载为基础菜单

	VariantInit(&BaseMenu);

	BaseMenu.vt = VT_BOOL;

	BaseMenu.boolVal = FALSE;

	menuGroups.Load(CString(filePath), BaseMenu);
	// 把菜单在菜单条上显示出来

	//CAcadMenuBar menuBar(acadApp.get_MenuBar());  //当前菜单条

	//CAcadPopupMenus popupMenus(menuGroup.get_Menus()); //要加入的菜单条

	//CAcadPopupMenu popupMenu;

	//long curPopupMenuNum = menuBar.get_Count();   //当前菜单条上菜单的数目

	//long n = popupMenus.get_Count();
	////bool beExit = false;
	//for (long i = 0; i < n; i++) {

	//	index.lVal = i;

	//	popupMenu = popupMenus.Item(index);

	//	index.lVal = i + curPopupMenuNum;

	//	popupMenu.InsertInMenuBar(index);
	//	CString strName = popupMenu.get_Name();
	//	if (strName.CompareNoCase(_T("TaiyuanBoilerElevation")) == 0)
	//	{
	//		//beExit = TRUE;
	//		break;
	//	}
	//}
	return true;
}
static void initLoadMenu()
{
	CString strPath = CUtility::GetAppPath();
	strPath = strPath.Left(strPath.ReverseFind('\\'));
	if (strPath != _T(""))
	{
		strPath += _T("\\xhhk.cuix");
	}
	LoadPartialMenu(strPath, _T("xhhk"));
}
```

在`On_kInitAppMsg`中

`initLoadMenu();`



推荐使用第一种方式，不需要加载那么多的头文件

![image-20250604151542564](http://image.jerryma.xyz//images/20250604-image-20250604151542564.png)