---
title: CXTPPropertyGrid控件使用
date: 2024-06-12
categories:
  - CPP
  - MFC
  - UI控件
tags:
  - MFC
  - CXTPPropertyGrid
  - Codejock
  - UI控件
description: Codejock Toolkit中CXTPPropertyGrid属性网格控件的使用方法和实例
author: JerryMa
---
# CXTPPropertyGrid控件使用
## xtp配置

```cpp
inc 默认安装目录
C:\Program Files (x86)\Codejock Software\MFC\Xtreme ToolkitPro v20.3.0\Source
lib 默认安装目录
C:\Program Files (x86)\Codejock Software\MFC\Xtreme ToolkitPro v20.3.0\Lib\vc150x64
在stdafx.h中添加

#include <XTToolkitPro.h>

//#include "arxHeaders.h"

```

![image-20240401160031481](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2024/04/1_16_0_32_20240401-image-20240401160031481.png)

## 在对话框中拉一个picture control控件

client Edge设置为true
visible 设置为false


DDX_Control(pDX, IDC_PLACEHOLDER, m_wndPlaceHolder);

## 加载控件

``` cpp
CString strVal;
//map<pair<int, int>, CString> mp = GetXrecord();
vector<CString> vec{ _T("类型"), _T("长"), _T("宽"), _T("高"), _T("其它"), _T("其它1"), _T("其它2"), _T("其它3"), _T("其它4"), _T("其它5"), _T("其它6"), _T("其它7"), _T("其它8") };
CRect rc;
m_wndPlaceHolder.GetWindowRect(&rc);
ScreenToClient(&rc);

if (m_wndPropertyGrid.Create(rc, this, IDC_PROPERTY_GRID))
{
    m_wndPropertyGrid.SetVariableItemsHeight(TRUE);

    LOGFONT lf;
    GetFont()->GetLogFont(&lf);

    CXTPPropertyGridItem* pStandard = m_wndPropertyGrid.AddCategory(_T("属性数据"));
    pStandard->AddChildItem(new CXTPPropertyGridItem(_T("String item"), _T("测试")));
    pStandard->AddChildItem(new CXTPPropertyGridItemNumber(_T("Integer item")));
    pStandard->AddChildItem(new CXTPPropertyGridItemDouble(_T("Double item")));

    //下拉框
    CXTPPropertyGridItem* pItem = pStandard->AddChildItem(
        new CXTPPropertyGridItemEnum(_T("Enum item"), 2));
    pItem->GetConstraints()->AddConstraint(_T("一型"), 1);
    pItem->GetConstraints()->AddConstraint(_T("L型"), 2);
    pItem->GetConstraints()->AddConstraint(_T("R型"), 3);
    //////////////////////////////////////////////////////////////////////////


    //下拉形式
    //CXTPPropertyGridItem* pItemLanguage = pStandard->AddChildItem(new CXTPPropertyGridItem(strLabel, strDeFault));
    //CXTPPropertyGridItemConstraints* pList = pItemLanguage->GetConstraints();
    //for (auto it : tmpVec)
    //{
    //    pList->AddConstraint(it);
    //}
    //pItemLanguage->SetFlags(xtpGridItemHasComboButton | xtpGridItemHasEdit);

    //pStandard->Expand();
}
```

* 隐藏Category

``` c++
m_wndPropertyGrid.SetPropertySort(xtpGridSortNoSort);//将Category隐藏
```

* 清空所有数据

``` c++
m_wndPropertyGrid.ResetContent();
```

* 读取数据

``` cpp
//读取数据
CString strItem;		
CXTPPropertyGridItem* pItems = m_wndPropertyGrid.GetItem(0);
if (pItems != NULL)
{
    int nCount = pItems->GetChilds()->GetCount();
    for (int i = 0; i < nCount; i++)
    {
        CXTPPropertyGridItem* pItem = pItems->GetChilds()->GetAt(i);
        strItem = pItem->GetCaption();
        strVal = pItem->GetValue();
        acutPrintf(_T("\nitem:%s,val:%s"), strItem, strVal);
    }
}
```

* 消息响应

``` cpp
ON_MESSAGE(XTPWM_PROPERTYGRID_NOTIFY, OnGridNotify)
```

```cpp
LRESULT CDlgShowTk::OnGridNotify(WPARAM wParam, LPARAM lParam)
{
	if (wParam == XTP_PGN_ITEMVALUE_CHANGED)
	{
		CXTPPropertyGridItem* pItem = (CXTPPropertyGridItem*)lParam;
		TRACE(_T("Value Changed. Caption = %s, ID = %i, Value = %s\n"), pItem->GetCaption(),
			pItem->GetID(), pItem->GetValue());

		if (DYNAMIC_DOWNCAST(CXTPPropertyGridItemEnum, pItem))
		{
			if (pItem->GetMetrics(TRUE, FALSE))
			{
				pItem->GetMetrics(TRUE, FALSE)->m_nImage =
					((CXTPPropertyGridItemEnum*)pItem)->GetEnum();
			}
		}

		if (pItem->GetID() == 501) // Dynamic Options
		{
			CXTPPropertyGridItems* pSiblingItems = pItem->GetParentItem()->GetChilds();

			for (int i = 0; i < pSiblingItems->GetCount(); i++)
			{
				if (pSiblingItems->GetAt(i) != pItem)
				{
					pSiblingItems->GetAt(i)->SetHidden(
						!((CXTPPropertyGridItemBool*)pItem)->GetBool());
				}
			}
		}
	}
	if (wParam == XTP_PGN_EDIT_CHANGED)
	{
		CXTPPropertyGridInplaceEdit* pEdit = DYNAMIC_DOWNCAST(CXTPPropertyGridInplaceEdit,
			(CWnd*)lParam);
		if (pEdit && pEdit->GetItem())
		{
			// Custom Validation
			if (pEdit->GetItem()->GetID() == ID_ITEM_VERSION_LANGUAGE)
			{
				CString str;
				pEdit->CEdit::GetWindowText(str);

				if (str.GetLength() > 30)
				{
					MessageBeep((UINT)-1);
					pEdit->SetSel(0, -1);
					pEdit->ReplaceSel(str.Left(30));
				}
			}
			// Custom Validation
			if (pEdit->GetItem()->GetCaption() == _T("ItemsInMRUList"))
			{
				CString str;
				pEdit->CEdit::GetWindowText(str);

				int i = _ttoi(str);
				if (i > 20)
				{
					MessageBeep((UINT)-1);
					pEdit->SetSel(0, -1);
					pEdit->ReplaceSel(_T("20"));
				}
			}
		}
	}
	return 0;
}
```


## 联动修改

<b>ID_ITEM_CORNER
ID_ITEM_CONFIG</b> 在resource.h中定义

``` cpp
LRESULT CDlgCategory::OnGridNotify(WPARAM wParam, LPARAM lParam)
{
	if (wParam == XTP_PGN_ITEMVALUE_CHANGED)
	{
		CXTPPropertyGridItem* pItem = (CXTPPropertyGridItem*)lParam;
		if (pItem->GetID() == ID_ITEM_CONFIG) // Dynamic Options
		{
			CString strConfig = pItem->GetValue();
			CXTPPropertyGridItems* pSiblingItems = pItem->GetParentItem()->GetChilds();

			for (int i = 0; i < pSiblingItems->GetCount(); i++)
			{
				if (pSiblingItems->GetAt(i)->GetID() == ID_ITEM_CORNER)
				{
					//我们在选择了“一型”就自动关联选择下面转角的”否“；选择其余配置就是自动关联选择“是”。
					//The Cognitive Complexity of this function is 16 which is greater than 15 authorized.
					pSiblingItems->GetAt(i)->SetValue(
						(strConfig.CompareNoCase(_T("一型")) == 0) ? _T("否") : _T("是"));
				}
			}
		}
	}
	return 0;
}
```

* <font size = 5 color="red">参考<b>C:\Program Files (x86)\Codejock Software\MFC\Xtreme ToolkitPro v20.3.0\Samples\PropertyGrid\GridSample\PropertyGrid_vc150.sln</b>里的<b>PropertyGrid</b></font>